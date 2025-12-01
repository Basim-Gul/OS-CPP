"""Resource Allocation Graph (RAG) implementation for OS simulation."""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


class NodeType(Enum):
    """Type of node in the RAG."""
    PROCESS = "process"
    RESOURCE = "resource"


@dataclass
class Node:
    """A node in the Resource Allocation Graph."""
    node_id: str
    node_type: NodeType
    name: str
    
    # For resource nodes
    total_instances: int = 1
    available_instances: int = 1


@dataclass
class Edge:
    """An edge in the Resource Allocation Graph."""
    from_node: str
    to_node: str
    edge_type: str  # 'request' (P -> R) or 'assignment' (R -> P)
    count: int = 1
    timestamp: int = 0


class ResourceAllocationGraph:
    """Resource Allocation Graph for deadlock detection and visualization."""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.adjacency_list: Dict[str, List[str]] = {}  # For cycle detection
    
    def add_process(self, pid: int, name: str = None) -> None:
        """Add a process node to the graph."""
        node_id = f"P{pid}"
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(
                node_id=node_id,
                node_type=NodeType.PROCESS,
                name=name or f"Process {pid}"
            )
            self.adjacency_list[node_id] = []
    
    def add_resource(self, rid: int, name: str = None, instances: int = 1) -> None:
        """Add a resource node to the graph."""
        node_id = f"R{rid}"
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(
                node_id=node_id,
                node_type=NodeType.RESOURCE,
                name=name or f"Resource {rid}",
                total_instances=instances,
                available_instances=instances
            )
            self.adjacency_list[node_id] = []
    
    def add_request_edge(self, pid: int, rid: int, count: int = 1, 
                         timestamp: int = 0) -> None:
        """Add a request edge from process to resource (P -> R)."""
        from_node = f"P{pid}"
        to_node = f"R{rid}"
        
        # Ensure nodes exist
        if from_node not in self.nodes:
            self.add_process(pid)
        if to_node not in self.nodes:
            self.add_resource(rid)
        
        # Check if edge already exists
        for edge in self.edges:
            if (edge.from_node == from_node and edge.to_node == to_node 
                and edge.edge_type == 'request'):
                edge.count += count
                return
        
        # Add new edge
        edge = Edge(from_node, to_node, 'request', count, timestamp)
        self.edges.append(edge)
        self.adjacency_list[from_node].append(to_node)
    
    def add_assignment_edge(self, rid: int, pid: int, count: int = 1,
                           timestamp: int = 0) -> None:
        """Add an assignment edge from resource to process (R -> P)."""
        from_node = f"R{rid}"
        to_node = f"P{pid}"
        
        # Ensure nodes exist
        if from_node not in self.nodes:
            self.add_resource(rid)
        if to_node not in self.nodes:
            self.add_process(pid)
        
        # Check if edge already exists
        for edge in self.edges:
            if (edge.from_node == from_node and edge.to_node == to_node 
                and edge.edge_type == 'assignment'):
                edge.count += count
                return
        
        # Add new edge
        edge = Edge(from_node, to_node, 'assignment', count, timestamp)
        self.edges.append(edge)
        self.adjacency_list[from_node].append(to_node)
        
        # Update resource availability
        if from_node in self.nodes:
            self.nodes[from_node].available_instances -= count
    
    def remove_request_edge(self, pid: int, rid: int, count: int = 1) -> bool:
        """Remove a request edge."""
        from_node = f"P{pid}"
        to_node = f"R{rid}"
        
        for i, edge in enumerate(self.edges):
            if (edge.from_node == from_node and edge.to_node == to_node 
                and edge.edge_type == 'request'):
                if edge.count <= count:
                    self.edges.pop(i)
                    if to_node in self.adjacency_list[from_node]:
                        self.adjacency_list[from_node].remove(to_node)
                else:
                    edge.count -= count
                return True
        return False
    
    def remove_assignment_edge(self, rid: int, pid: int, count: int = 1) -> bool:
        """Remove an assignment edge."""
        from_node = f"R{rid}"
        to_node = f"P{pid}"
        
        for i, edge in enumerate(self.edges):
            if (edge.from_node == from_node and edge.to_node == to_node 
                and edge.edge_type == 'assignment'):
                if edge.count <= count:
                    self.edges.pop(i)
                    if to_node in self.adjacency_list[from_node]:
                        self.adjacency_list[from_node].remove(to_node)
                else:
                    edge.count -= count
                
                # Update resource availability
                if from_node in self.nodes:
                    self.nodes[from_node].available_instances += count
                return True
        return False
    
    def remove_process(self, pid: int) -> None:
        """Remove a process and all its edges from the graph."""
        node_id = f"P{pid}"
        
        # Remove all edges involving this process
        self.edges = [e for e in self.edges 
                      if e.from_node != node_id and e.to_node != node_id]
        
        # Update adjacency list
        if node_id in self.adjacency_list:
            del self.adjacency_list[node_id]
        for node, neighbors in self.adjacency_list.items():
            if node_id in neighbors:
                neighbors.remove(node_id)
        
        # Remove node
        if node_id in self.nodes:
            del self.nodes[node_id]
    
    def get_request_edges(self, pid: int = None) -> List[Edge]:
        """Get all request edges, optionally filtered by process."""
        if pid is None:
            return [e for e in self.edges if e.edge_type == 'request']
        node_id = f"P{pid}"
        return [e for e in self.edges 
                if e.edge_type == 'request' and e.from_node == node_id]
    
    def get_assignment_edges(self, pid: int = None, rid: int = None) -> List[Edge]:
        """Get all assignment edges, optionally filtered."""
        edges = [e for e in self.edges if e.edge_type == 'assignment']
        if pid is not None:
            edges = [e for e in edges if e.to_node == f"P{pid}"]
        if rid is not None:
            edges = [e for e in edges if e.from_node == f"R{rid}"]
        return edges
    
    def get_processes_holding_resource(self, rid: int) -> List[int]:
        """Get list of process IDs holding a resource."""
        node_id = f"R{rid}"
        pids = []
        for edge in self.edges:
            if edge.from_node == node_id and edge.edge_type == 'assignment':
                pid = int(edge.to_node[1:])
                pids.append(pid)
        return pids
    
    def get_resources_held_by_process(self, pid: int) -> List[int]:
        """Get list of resource IDs held by a process."""
        node_id = f"P{pid}"
        rids = []
        for edge in self.edges:
            if edge.to_node == node_id and edge.edge_type == 'assignment':
                rid = int(edge.from_node[1:])
                rids.append(rid)
        return rids
    
    def get_wait_for_graph(self) -> Dict[int, List[int]]:
        """Create a wait-for graph from the RAG.
        
        Returns: {pid: [pids that this process is waiting for]}
        """
        wait_for: Dict[int, List[int]] = {}
        
        # For each request edge P -> R
        for req_edge in self.get_request_edges():
            pid = int(req_edge.from_node[1:])
            rid = int(req_edge.to_node[1:])
            
            if pid not in wait_for:
                wait_for[pid] = []
            
            # Find who holds this resource
            for assign_edge in self.edges:
                if (assign_edge.from_node == req_edge.to_node and 
                    assign_edge.edge_type == 'assignment'):
                    holder_pid = int(assign_edge.to_node[1:])
                    if holder_pid != pid and holder_pid not in wait_for[pid]:
                        wait_for[pid].append(holder_pid)
        
        return wait_for
    
    def to_ascii(self) -> str:
        """Generate ASCII representation of the graph."""
        lines = ["Resource Allocation Graph:", "=" * 40]
        
        # List processes
        processes = [n for n in self.nodes.values() if n.node_type == NodeType.PROCESS]
        resources = [n for n in self.nodes.values() if n.node_type == NodeType.RESOURCE]
        
        lines.append("\nProcesses:")
        for p in processes:
            lines.append(f"  [{p.node_id}] {p.name}")
        
        lines.append("\nResources:")
        for r in resources:
            lines.append(f"  ({r.node_id}) {r.name} "
                        f"[{r.available_instances}/{r.total_instances} available]")
        
        lines.append("\nEdges:")
        for edge in self.edges:
            if edge.edge_type == 'request':
                lines.append(f"  {edge.from_node} --wants--> {edge.to_node} (count: {edge.count})")
            else:
                lines.append(f"  {edge.from_node} --held-by--> {edge.to_node} (count: {edge.count})")
        
        return "\n".join(lines)
    
    def reset(self) -> None:
        """Reset the graph to empty state."""
        self.nodes.clear()
        self.edges.clear()
        self.adjacency_list.clear()
