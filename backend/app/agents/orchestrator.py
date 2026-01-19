"""
Enhanced Multi-Agent Orchestrator
Features:
- LLM-based intelligent routing
- Agent chaining and fallback
- Parallel execution support
- Caching and metrics
- Error handling with retries
- Post-processing pipeline
"""
from enum import Enum
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import time
import hashlib
import json
from functools import lru_cache

from app.agents.content_agent import ContentAgent
from app.agents.financial_agent import FinancialAgent
from app.agents.science_agent import ScienceAgent
from app.services.image_service import ImageService
from app.services.llm_service import LLMService


class AgentType(str, Enum):
    CONTENT = "content"
    FINANCIAL = "financial"
    SCIENCE = "science"


@dataclass
class AgentCapability:
    """Describes what an agent can do"""
    agent_type: AgentType
    name: str
    description: str
    keywords: List[str]
    strengths: List[str]
    priority: int = 1  # Higher = preferred when tied


@dataclass
class OrchestrationResult:
    """Result from orchestration with metadata"""
    content: str
    agent_used: AgentType
    agent_description: str
    topic: str
    platform: str
    confidence_score: float = 0.0
    processing_time_ms: float = 0.0
    routing_reason: str = ""
    fallback_used: bool = False
    image_url: Optional[str] = None
    sources: Optional[List[dict]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "agent_used": self.agent_used.value,
            "agent_description": self.agent_description,
            "topic": self.topic,
            "platform": self.platform,
            "confidence_score": self.confidence_score,
            "processing_time_ms": self.processing_time_ms,
            "routing_reason": self.routing_reason,
            "fallback_used": self.fallback_used,
            "image_url": self.image_url,
            "sources": self.sources,
            **self.metadata
        }


@dataclass 
class RoutingDecision:
    """Decision from the routing logic"""
    agent_type: AgentType
    confidence: float
    reason: str
    alternative_agents: List[AgentType] = field(default_factory=list)


class RequestCache:
    """Simple in-memory cache for request results"""
    
    def __init__(self, max_size: int = 100, ttl_seconds: int = 3600):
        self._cache: Dict[str, tuple] = {}  # hash -> (result, timestamp)
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
    
    def _hash_request(self, topic: str, platform: str, audience: str, language: str) -> str:
        key = f"{topic}:{platform}:{audience}:{language}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, topic: str, platform: str, audience: str, language: str) -> Optional[dict]:
        key = self._hash_request(topic, platform, audience, language)
        if key in self._cache:
            result, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                return result
            else:
                del self._cache[key]
        return None
    
    def set(self, topic: str, platform: str, audience: str, language: str, result: dict):
        # Evict old entries if cache is full
        if len(self._cache) >= self.max_size:
            oldest_key = min(self._cache, key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]
        
        key = self._hash_request(topic, platform, audience, language)
        self._cache[key] = (result, time.time())


class OrchestrationMetrics:
    """Track orchestration metrics"""
    
    def __init__(self):
        self.total_requests = 0
        self.agent_usage: Dict[str, int] = {}
        self.avg_processing_time_ms = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
        self.errors = 0
        self.fallbacks_used = 0
    
    def record_request(self, agent_type: AgentType, processing_time_ms: float, 
                       cache_hit: bool = False, fallback: bool = False, error: bool = False):
        self.total_requests += 1
        self.agent_usage[agent_type.value] = self.agent_usage.get(agent_type.value, 0) + 1
        
        # Update rolling average
        self.avg_processing_time_ms = (
            (self.avg_processing_time_ms * (self.total_requests - 1) + processing_time_ms) 
            / self.total_requests
        )
        
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        
        if fallback:
            self.fallbacks_used += 1
        
        if error:
            self.errors += 1
    
    def get_stats(self) -> dict:
        return {
            "total_requests": self.total_requests,
            "agent_usage": self.agent_usage,
            "avg_processing_time_ms": round(self.avg_processing_time_ms, 2),
            "cache_hit_rate": round(self.cache_hits / max(self.total_requests, 1) * 100, 2),
            "error_rate": round(self.errors / max(self.total_requests, 1) * 100, 2),
            "fallback_rate": round(self.fallbacks_used / max(self.total_requests, 1) * 100, 2)
        }


class AgentOrchestrator:
    """
    Enhanced Multi-Agent Orchestrator
    
    Features:
    - Smart LLM-based routing with confidence scores
    - Keyword-based fallback routing
    - Agent chaining for complex requests
    - Request caching
    - Metrics and monitoring
    - Retry logic with fallback agents
    - Post-processing pipeline
    """
    
    # Agent capabilities for smart routing
    AGENT_CAPABILITIES = {
        AgentType.FINANCIAL: AgentCapability(
            agent_type=AgentType.FINANCIAL,
            name="Financial Agent",
            description="Specialized in financial content with real-time market data, stock prices, and financial news",
            keywords=[
                "mercado", "bolsa", "acciones", "inversión", "finanzas", "trading",
                "stock", "market", "investment", "crypto", "bitcoin", "economía",
                "ibex", "nasdaq", "sp500", "dow jones", "dividendos", "forex",
                "portfolio", "hedge", "bonds", "etf", "ipo", "earnings", "wall street"
            ],
            strengths=["real-time data", "market analysis", "financial news", "stock prices"],
            priority=2
        ),
        AgentType.SCIENCE: AgentCapability(
            agent_type=AgentType.SCIENCE,
            name="Science Agent",
            description="Specialized in scientific content with RAG over arXiv papers and knowledge graph",
            keywords=[
                "científico", "investigación", "paper", "estudio", "arxiv",
                "física", "química", "biología", "medicina", "quantum", "cuántico",
                "inteligencia artificial", "machine learning", "neurociencia",
                "astrofísica", "genética", "climate", "cambio climático",
                "research", "algorithm", "neural network", "deep learning", "nlp",
                "computer vision", "robotics", "data science", "ai", "ml"
            ],
            strengths=["scientific papers", "technical explanations", "research synthesis", "citations"],
            priority=2
        ),
        AgentType.CONTENT: AgentCapability(
            agent_type=AgentType.CONTENT,
            name="General Content Agent", 
            description="General purpose content creation for social media and blogs",
            keywords=[],  # Catch-all agent
            strengths=["versatility", "social media optimization", "engagement"],
            priority=1
        )
    }
    
    ROUTING_PROMPT = """You are a request router for a content generation system. Analyze the user's topic and decide which specialized agent should handle it.

Available agents:
1. FINANCIAL - For financial markets, stocks, crypto, investment, economic news
2. SCIENCE - For scientific topics, research, AI/ML, physics, biology, technology papers
3. CONTENT - General content for social media (use when topic doesn't fit others)

User's topic: "{topic}"
Platform: {platform}
Additional context: {context}

Respond with ONLY a JSON object (no markdown, no explanation):
{{"agent": "FINANCIAL|SCIENCE|CONTENT", "confidence": 0.0-1.0, "reason": "brief explanation"}}"""

    def __init__(
        self, 
        llm_provider: str = "groq",
        enable_smart_routing: bool = True,
        enable_caching: bool = True,
        max_retries: int = 2
    ):
        self.llm_provider = llm_provider
        self.enable_smart_routing = enable_smart_routing
        self.enable_caching = enable_caching
        self.max_retries = max_retries
        
        # Initialize agents
        self.agents = {
            AgentType.CONTENT: ContentAgent(llm_provider),
            AgentType.FINANCIAL: FinancialAgent(llm_provider),
            AgentType.SCIENCE: ScienceAgent(llm_provider),
        }
        
        # LLM service for routing decisions
        self.router_llm = LLMService(provider=llm_provider)
        
        # Cache and metrics
        self.cache = RequestCache() if enable_caching else None
        self.metrics = OrchestrationMetrics()
        
        # Post-processing hooks
        self._post_processors: List[Callable] = []
    
    def add_post_processor(self, processor: Callable[[dict], dict]):
        """Add a post-processing function to the pipeline"""
        self._post_processors.append(processor)
    
    async def _smart_route(self, topic: str, platform: str, context: str = "") -> RoutingDecision:
        """Use LLM to intelligently route the request"""
        try:
            prompt = self.ROUTING_PROMPT.format(
                topic=topic,
                platform=platform,
                context=context or "None provided"
            )
            
            response = await self.router_llm.generate(prompt)
            
            # Parse JSON response
            import re
            json_match = re.search(r'\{.*?\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                agent_str = data.get("agent", "CONTENT").upper()
                
                agent_type = {
                    "FINANCIAL": AgentType.FINANCIAL,
                    "SCIENCE": AgentType.SCIENCE,
                    "CONTENT": AgentType.CONTENT
                }.get(agent_str, AgentType.CONTENT)
                
                return RoutingDecision(
                    agent_type=agent_type,
                    confidence=float(data.get("confidence", 0.7)),
                    reason=data.get("reason", "LLM routing decision"),
                    alternative_agents=self._get_fallback_agents(agent_type)
                )
        except Exception as e:
            print(f"Smart routing failed: {e}, falling back to keyword routing")
        
        # Fallback to keyword routing
        return self._keyword_route(topic)
    
    def _keyword_route(self, topic: str) -> RoutingDecision:
        """Fallback keyword-based routing"""
        topic_lower = topic.lower()
        
        scores = {}
        for agent_type, capability in self.AGENT_CAPABILITIES.items():
            score = sum(1 for kw in capability.keywords if kw in topic_lower)
            # Apply priority bonus
            score += capability.priority * 0.1
            scores[agent_type] = score
        
        # Find best match
        best_agent = max(scores, key=scores.get)
        best_score = scores[best_agent]
        
        # Calculate confidence based on keyword matches
        confidence = min(best_score / 5.0, 1.0) if best_score > 0 else 0.5
        
        if best_score == 0:
            best_agent = AgentType.CONTENT
            confidence = 0.6
        
        return RoutingDecision(
            agent_type=best_agent,
            confidence=confidence,
            reason=f"Keyword matching (score: {best_score:.1f})",
            alternative_agents=self._get_fallback_agents(best_agent)
        )
    
    def _get_fallback_agents(self, primary: AgentType) -> List[AgentType]:
        """Get ordered list of fallback agents"""
        all_agents = [AgentType.CONTENT, AgentType.FINANCIAL, AgentType.SCIENCE]
        return [a for a in all_agents if a != primary]
    
    async def _execute_with_retry(
        self, 
        agent_type: AgentType,
        topic: str,
        platform: str,
        audience: str,
        language: str,
        fallback_agents: List[AgentType],
        **kwargs
    ) -> tuple[dict, AgentType, bool]:
        """Execute agent with retry and fallback logic"""
        
        agents_to_try = [agent_type] + fallback_agents[:self.max_retries]
        last_error = None
        
        for i, current_agent_type in enumerate(agents_to_try):
            try:
                agent = self.agents[current_agent_type]
                result = await agent.generate(
                    topic=topic,
                    platform=platform,
                    audience=audience,
                    language=language,
                    **kwargs
                )
                
                fallback_used = i > 0
                return result, current_agent_type, fallback_used
                
            except Exception as e:
                last_error = e
                print(f"Agent {current_agent_type.value} failed: {e}")
                if i < len(agents_to_try) - 1:
                    print(f"Trying fallback agent...")
                continue
        
        # All agents failed
        raise Exception(f"All agents failed. Last error: {last_error}")
    
    async def _generate_image_async(self, topic: str, platform: str) -> Optional[str]:
        """Generate image asynchronously"""
        sizes = {
            "twitter": (1200, 675),
            "instagram": (1080, 1080),
            "linkedin": (1200, 627),
            "blog": (1200, 630)
        }
        width, height = sizes.get(platform, (1200, 630))
        
        try:
            return await ImageService.generate_image(
                prompt=topic,
                width=width,
                height=height
            )
        except Exception as e:
            print(f"Image generation failed: {e}")
            return None
    
    def _run_post_processors(self, result: dict) -> dict:
        """Run all post-processing hooks"""
        for processor in self._post_processors:
            try:
                result = processor(result)
            except Exception as e:
                print(f"Post-processor failed: {e}")
        return result
    
    async def process_request(
        self,
        topic: str,
        platform: str,
        audience: str,
        language: str = "Spanish",
        content_type: Optional[str] = None,
        use_cache: bool = True,
        generate_image: bool = True,
        **kwargs
    ) -> dict:
        """
        Process a content generation request
        
        Args:
            topic: The main topic for content
            platform: Target platform (twitter, linkedin, blog, instagram)
            audience: Target audience type
            language: Output language
            content_type: Explicit agent type (overrides routing)
            use_cache: Whether to use cached results
            generate_image: Whether to generate an image
            **kwargs: Additional arguments passed to agents
            
        Returns:
            Dict with generated content and metadata
        """
        start_time = time.time()
        cache_hit = False
        fallback_used = False
        
        try:
            # Check cache first
            if self.enable_caching and use_cache and self.cache:
                cached = self.cache.get(topic, platform, audience, language)
                if cached:
                    cache_hit = True
                    processing_time = (time.time() - start_time) * 1000
                    self.metrics.record_request(
                        AgentType(cached.get("agent_used", "content")),
                        processing_time,
                        cache_hit=True
                    )
                    cached["from_cache"] = True
                    cached["processing_time_ms"] = processing_time
                    return cached
            
            # Route the request
            if content_type:
                # Explicit routing
                try:
                    routing = RoutingDecision(
                        agent_type=AgentType(content_type),
                        confidence=1.0,
                        reason="Explicit content type specified",
                        alternative_agents=self._get_fallback_agents(AgentType(content_type))
                    )
                except ValueError:
                    routing = await self._smart_route(topic, platform, kwargs.get("additional_context", ""))
            elif self.enable_smart_routing:
                # Smart LLM-based routing
                routing = await self._smart_route(topic, platform, kwargs.get("additional_context", ""))
            else:
                # Keyword-based routing
                routing = self._keyword_route(topic)
            
            # Execute agent with retry logic
            agent_result, actual_agent, fallback_used = await self._execute_with_retry(
                agent_type=routing.agent_type,
                topic=topic,
                platform=platform,
                audience=audience,
                language=language,
                fallback_agents=routing.alternative_agents,
                **kwargs
            )
            
            # Generate image in parallel (if enabled)
            image_url = None
            if generate_image:
                image_url = await self._generate_image_async(topic, platform)
            
            # Build result
            processing_time = (time.time() - start_time) * 1000
            
            result = OrchestrationResult(
                content=agent_result.get("content", ""),
                agent_used=actual_agent,
                agent_description=self.agents[actual_agent].description,
                topic=topic,
                platform=platform,
                confidence_score=routing.confidence,
                processing_time_ms=processing_time,
                routing_reason=routing.reason,
                fallback_used=fallback_used,
                image_url=image_url,
                sources=agent_result.get("sources"),
                metadata={
                    k: v for k, v in agent_result.items() 
                    if k not in ["content", "sources"]
                }
            )
            
            result_dict = result.to_dict()
            
            # Run post-processors
            result_dict = self._run_post_processors(result_dict)
            
            # Cache result
            if self.enable_caching and self.cache:
                self.cache.set(topic, platform, audience, language, result_dict)
            
            # Record metrics
            self.metrics.record_request(
                actual_agent,
                processing_time,
                cache_hit=False,
                fallback=fallback_used
            )
            
            return result_dict
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            self.metrics.record_request(
                AgentType.CONTENT,
                processing_time,
                error=True
            )
            raise
    
    async def process_batch(
        self,
        requests: List[dict],
        max_concurrent: int = 3
    ) -> List[dict]:
        """
        Process multiple requests in parallel
        
        Args:
            requests: List of request dicts with topic, platform, audience, etc.
            max_concurrent: Maximum concurrent requests
            
        Returns:
            List of results in same order as requests
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(request: dict) -> dict:
            async with semaphore:
                try:
                    return await self.process_request(**request)
                except Exception as e:
                    return {"error": str(e), **request}
        
        tasks = [process_with_semaphore(req) for req in requests]
        return await asyncio.gather(*tasks)
    
    async def chain_agents(
        self,
        topic: str,
        platform: str,
        audience: str,
        language: str = "Spanish",
        agent_sequence: List[AgentType] = None,
        **kwargs
    ) -> dict:
        """
        Chain multiple agents for complex content generation
        
        Example: Science agent for research → Content agent for social optimization
        
        Args:
            topic: Main topic
            platform: Target platform
            audience: Target audience
            language: Output language
            agent_sequence: Ordered list of agents to chain
            
        Returns:
            Final combined result
        """
        if not agent_sequence:
            agent_sequence = [AgentType.SCIENCE, AgentType.CONTENT]
        
        accumulated_context = ""
        all_sources = []
        
        for i, agent_type in enumerate(agent_sequence):
            agent = self.agents[agent_type]
            
            # Add previous content as context for chaining
            enhanced_kwargs = {**kwargs}
            if accumulated_context:
                existing_context = enhanced_kwargs.get("additional_context", "")
                enhanced_kwargs["additional_context"] = (
                    f"{existing_context}\n\nPrevious research:\n{accumulated_context[:1000]}"
                )
            
            result = await agent.generate(
                topic=topic,
                platform=platform,
                audience=audience,
                language=language,
                **enhanced_kwargs
            )
            
            accumulated_context = result.get("content", "")
            if result.get("sources"):
                all_sources.extend(result["sources"])
        
        # Generate image for final content
        image_url = await self._generate_image_async(topic, platform)
        
        return {
            "content": accumulated_context,
            "topic": topic,
            "platform": platform,
            "agent_chain": [a.value for a in agent_sequence],
            "sources": all_sources,
            "image_url": image_url
        }
    
    def get_metrics(self) -> dict:
        """Get orchestration metrics"""
        return self.metrics.get_stats()
    
    def get_agent_info(self) -> List[dict]:
        """Get information about available agents"""
        return [
            {
                "type": cap.agent_type.value,
                "name": cap.name,
                "description": cap.description,
                "strengths": cap.strengths
            }
            for cap in self.AGENT_CAPABILITIES.values()
        ]