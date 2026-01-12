"""
Graph Store para Graph RAG usando NetworkX
"""
import networkx as nx
from typing import List, Dict, Tuple, Optional
import json
import re


class KnowledgeGraph: 
    """Grafo de conocimiento para Graph RAG"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def add_entity(self, entity_id: str, entity_type: str, properties: dict = None):
        """Añade una entidad al grafo"""
        self.graph.add_node(
            entity_id,
            type=entity_type,
            properties=properties or {}
        )
    
    def add_relation(self, source:  str, target: str, relation_type:  str, properties: dict = None):
        """Añade una relación entre entidades"""
        self.graph.add_edge(
            source,
            target,
            relation=relation_type,
            properties=properties or {}
        )
    
    def extract_entities_from_text(self, text: str, llm_service) -> List[Dict]: 
        """Extrae entidades y relaciones de un texto usando LLM"""
        extraction_prompt = f"""Extrae las entidades y relaciones científicas del siguiente texto. 

TEXTO:
{text}

Responde SOLO con JSON válido en este formato exacto:
{{
    "entities": [
        {{"id": "entity_1", "name": "Nombre", "type": "concept|person|organization|technology|theory"}},
    ],
    "relations": [
        {{"source": "entity_1", "target": "entity_2", "relation": "related_to|discovers|develops|proves|contradicts"}}
    ]
}}
"""
        # Nota: Esto requiere llamar al LLM de forma síncrona o manejar async
        return []  # Placeholder - implementar con LLM
    
    def get_subgraph(self, entity_id: str, depth: int = 2) -> nx.DiGraph:
        """Obtiene un subgrafo centrado en una entidad"""
        if entity_id not in self.graph:
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
        
        for entity in query_entities:
            if entity in self.graph:
                node_data = self.graph.nodes[entity]
                context_parts.append(
                    f"**{entity}** ({node_data.get('type', 'unknown')}): "
                    f"{json.dumps(node_data.get('properties', {}))}"
                )
                
                # Añadir relaciones
                for _, target, data in self.graph.out_edges(entity, data=True):
                    if relations_found < max_relations: 
                        context_parts.append(
                            f"  → {data.get('relation', 'related_to')} → {target}"
                        )
                        relations_found += 1
                
                for source, _, data in self.graph.in_edges(entity, data=True):
                    if relations_found < max_relations: 
                        context_parts.append(
                            f"  ← {data.get('relation', 'related_to')} ← {source}"
                        )
                        relations_found += 1
        
        return "\n".join(context_parts)
    
    def to_dict(self) -> dict:
        """Serializa el grafo a diccionario"""
        return nx.node_link_data(self.graph)
    
    def from_dict(self, data: dict):
        """Carga el grafo desde diccionario"""
        self.graph = nx.node_link_graph(data)
    
    def save(self, filepath: str):
        """Guarda el grafo a archivo"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f)
    
    def load(self, filepath: str):
        """Carga el grafo desde archivo"""
        with open(filepath, 'r') as f:
            self.from_dict(json.load(f))