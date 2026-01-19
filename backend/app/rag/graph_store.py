"""
Graph Store para Graph RAG usando NetworkX
Enhanced with: LLM-based entity extraction, similarity matching, graph persistence
"""
import networkx as nx
from typing import List, Dict, Optional
import json
import re
import os
from difflib import SequenceMatcher


class KnowledgeGraph: 
    """
    Enhanced Knowledge Graph for Graph RAG
    Features: LLM entity extraction, fuzzy matching, expanded domains
    """
    
    # Entity types supported
    ENTITY_TYPES = ["concept", "technology", "theory", "person", "organization", "method", "dataset"]
    
    # Relation types supported
    RELATION_TYPES = [
        "is_subfield_of", "enables", "based_on", "related_to", "is_type_of",
        "core_component_of", "discovers", "develops", "proves", "contradicts",
        "uses", "improves", "extends", "applies_to", "requires"
    ]
    
    def __init__(self, persist_path: Optional[str] = None):
        self.graph = nx.DiGraph()
        self.persist_path = persist_path
        
        # Load existing graph if available
        if persist_path and os.path.exists(persist_path):
            self.load(persist_path)
    
    def add_entity(self, entity_id: str, entity_type: str, properties: dict = None):
        """Añade una entidad al grafo"""
        # Normalize entity_id
        entity_id = self._normalize_id(entity_id)
        
        self.graph.add_node(
            entity_id,
            type=entity_type if entity_type in self.ENTITY_TYPES else "concept",
            properties=properties or {}
        )
        
        self._auto_persist()
    
    def add_relation(self, source: str, target: str, relation_type: str, properties: dict = None):
        """Añade una relación entre entidades"""
        source = self._normalize_id(source)
        target = self._normalize_id(target)
        
        # Ensure nodes exist
        if source not in self.graph:
            self.add_entity(source, "concept")
        if target not in self.graph:
            self.add_entity(target, "concept")
        
        self.graph.add_edge(
            source,
            target,
            relation=relation_type if relation_type in self.RELATION_TYPES else "related_to",
            properties=properties or {}
        )
        
        self._auto_persist()
    
    def _normalize_id(self, entity_id: str) -> str:
        """Normalize entity ID for consistent matching"""
        return entity_id.lower().strip().replace(" ", "_").replace("-", "_")
    
    def _auto_persist(self):
        """Auto-save graph if persist path is set"""
        if self.persist_path:
            self.save(self.persist_path)

    async def extract_entities_from_text(self, text: str, llm_service) -> Dict:
        """
        Extract entities and relations from text using LLM
        
        Args:
            text: Text to extract from
            llm_service: LLMService instance for extraction
            
        Returns:
            Dict with entities and relations
        """
        extraction_prompt = f"""Extract scientific entities and their relationships from this text.

TEXT:
{text[:2000]}

Respond ONLY with valid JSON in this exact format:
{{
    "entities": [
        {{"id": "entity_name_lowercase", "name": "Display Name", "type": "concept|technology|theory|person|method", "definition": "Brief definition"}}
    ],
    "relations": [
        {{"source": "entity_id_1", "target": "entity_id_2", "relation": "is_subfield_of|enables|based_on|uses|improves|extends"}}
    ]
}}

Focus on key scientific concepts, technologies, and their relationships.
Return at most 10 entities and 15 relations.
"""
        try:
            response = await llm_service.generate(extraction_prompt)
            
            # Parse JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                
                # Add extracted entities and relations to graph
                for entity in data.get("entities", []):
                    self.add_entity(
                        entity["id"],
                        entity.get("type", "concept"),
                        {"definition": entity.get("definition", ""), "name": entity.get("name", entity["id"])}
                    )
                
                for relation in data.get("relations", []):
                    self.add_relation(
                        relation["source"],
                        relation["target"],
                        relation.get("relation", "related_to")
                    )
                
                return data
        except Exception as e:
            print(f"Entity extraction error: {e}")
        
        return {"entities": [], "relations": []}
    
    def find_similar_entities(self, query: str, threshold: float = 0.6) -> List[str]:
        """
        Find entities similar to query using fuzzy matching
        
        Args:
            query: Search term
            threshold: Minimum similarity (0-1)
        """
        query_normalized = self._normalize_id(query)
        similar = []
        
        for node in self.graph.nodes():
            # Direct match
            if query_normalized in node or node in query_normalized:
                similar.append((node, 1.0))
                continue
            
            # Fuzzy match
            similarity = SequenceMatcher(None, query_normalized, node).ratio()
            if similarity >= threshold:
                similar.append((node, similarity))
            
            # Check properties for name match
            props = self.graph.nodes[node].get("properties", {})
            name = props.get("name", "").lower()
            if name and query_normalized in name:
                similar.append((node, 0.9))
        
        # Sort by similarity and return unique entities
        similar.sort(key=lambda x: x[1], reverse=True)
        seen = set()
        return [node for node, _ in similar if not (node in seen or seen.add(node))]
    
    def get_subgraph(self, entity_id: str, depth: int = 2) -> nx.DiGraph:
        """Obtiene un subgrafo centrado en una entidad"""
        entity_id = self._normalize_id(entity_id)
        
        if entity_id not in self.graph:
            # Try fuzzy match
            similar = self.find_similar_entities(entity_id)
            if similar:
                entity_id = similar[0]
            else:
                return nx.DiGraph()
        
        # BFS para obtener nodos hasta cierta profundidad
        nodes = {entity_id}
        current_level = {entity_id}
        
        for _ in range(depth):
            next_level = set()
            for node in current_level:
                next_level.update(self.graph.successors(node))
                next_level.update(self.graph.predecessors(node))
            nodes.update(next_level)
            current_level = next_level
        
        return self.graph.subgraph(nodes).copy()
    
    def get_context_for_query(self, query_entities: List[str], max_relations: int = 20) -> str:
        """Genera contexto textual a partir del grafo para una query"""
        context_parts = []
        relations_found = 0
        processed_entities = set()
        
        # Expand query entities with fuzzy matching
        expanded_entities = []
        for entity in query_entities:
            similar = self.find_similar_entities(entity, threshold=0.5)
            expanded_entities.extend(similar[:3])  # Top 3 matches per query term
        
        # Remove duplicates while preserving order
        seen = set()
        expanded_entities = [e for e in expanded_entities if not (e in seen or seen.add(e))]
        
        for entity in expanded_entities[:10]:  # Limit to avoid context overflow
            if entity in self.graph and entity not in processed_entities:
                processed_entities.add(entity)
                node_data = self.graph.nodes[entity]
                props = node_data.get('properties', {})
                
                # Format entity info
                entity_info = f"**{props.get('name', entity)}** ({node_data.get('type', 'unknown')})"
                if props.get('definition'):
                    entity_info += f": {props['definition']}"
                context_parts.append(entity_info)
                
                # Añadir relaciones salientes
                for _, target, data in self.graph.out_edges(entity, data=True):
                    if relations_found < max_relations:
                        target_name = self.graph.nodes[target].get('properties', {}).get('name', target)
                        context_parts.append(
                            f"  → {data.get('relation', 'related_to')} → {target_name}"
                        )
                        relations_found += 1
                
                # Añadir relaciones entrantes
                for source, _, data in self.graph.in_edges(entity, data=True):
                    if relations_found < max_relations:
                        source_name = self.graph.nodes[source].get('properties', {}).get('name', source)
                        context_parts.append(
                            f"  ← {data.get('relation', 'related_to')} ← {source_name}"
                        )
                        relations_found += 1
        
        return "\n".join(context_parts) if context_parts else ""
    
    def get_shortest_path(self, source: str, target: str) -> List[str]:
        """Find shortest path between two entities"""
        source = self._normalize_id(source)
        target = self._normalize_id(target)
        
        try:
            # Try undirected path
            undirected = self.graph.to_undirected()
            return nx.shortest_path(undirected, source, target)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []
    
    def get_stats(self) -> dict:
        """Get graph statistics"""
        return {
            "total_entities": self.graph.number_of_nodes(),
            "total_relations": self.graph.number_of_edges(),
            "entity_types": dict(nx.get_node_attributes(self.graph, 'type')),
            "connected_components": nx.number_weakly_connected_components(self.graph)
        }
    
    def to_dict(self) -> dict:
        """Serializa el grafo a diccionario"""
        return nx.node_link_data(self.graph)
    
    def from_dict(self, data: dict):
        """Carga el grafo desde diccionario"""
        self.graph = nx.node_link_graph(data)
    
    def save(self, filepath: str):
        """Guarda el grafo a archivo"""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def load(self, filepath: str):
        """Carga el grafo desde archivo"""
        try:
            with open(filepath, 'r') as f:
                self.from_dict(json.load(f))
        except Exception as e:
            print(f"Error loading graph: {e}")