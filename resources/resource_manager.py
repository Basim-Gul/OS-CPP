"""Resource Manager for OS simulation."""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from models.resource import Resource, ResourceType
from models.process import Process


@dataclass
class AllocationEvent:
    """Record of a resource allocation event."""
    timestamp: int
    event_type: str  # 'allocate', 'release', 'request', 'deny'
    process_id: int
    resource_id: int
    resource_name: str
    count: int
    success: bool
    message: str = ""


class ResourceManager:
    """Manages resources and their allocation to processes."""
    
    def __init__(self):
        self.resources: Dict[int, Resource] = {}
        self.processes: Dict[int, Process] = {}
        self.allocation_history: List[AllocationEvent] = []
        self.current_time: int = 0
        
        # Initialize default resources
        self._init_default_resources()
    
    def _init_default_resources(self) -> None:
        """Initialize the default system resources."""
        default_resources = [
            (1, "CPU", ResourceType.CPU, 4),
            (2, "Memory", ResourceType.MEMORY, 16),  # 16 memory units
            (3, "Printer", ResourceType.PRINTER, 2),
            (4, "Disk", ResourceType.DISK, 4)
        ]
        
        for rid, name, rtype, instances in default_resources:
            self.add_resource(Resource(rid, name, rtype, instances))
    
    def add_resource(self, resource: Resource) -> None:
        """Add a resource to the system."""
        self.resources[resource.rid] = resource
    
    def remove_resource(self, rid: int) -> Optional[Resource]:
        """Remove a resource from the system."""
        return self.resources.pop(rid, None)
    
    def get_resource(self, rid: int) -> Optional[Resource]:
        """Get a resource by ID."""
        return self.resources.get(rid)
    
    def get_resource_by_name(self, name: str) -> Optional[Resource]:
        """Get a resource by name."""
        for resource in self.resources.values():
            if resource.name == name:
                return resource
        return None
    
    def register_process(self, process: Process) -> None:
        """Register a process with the resource manager."""
        self.processes[process.pid] = process
    
    def unregister_process(self, pid: int) -> None:
        """Unregister a process and release all its resources."""
        if pid in self.processes:
            self.release_all(pid)
            del self.processes[pid]
    
    def request(self, pid: int, rid: int, count: int = 1) -> bool:
        """Request resources for a process.
        
        Returns True if allocation was successful, False otherwise.
        """
        if rid not in self.resources:
            self._log_event('deny', pid, rid, "", count, False, "Resource not found")
            return False
        
        resource = self.resources[rid]
        
        if resource.is_available(count):
            success = resource.allocate(pid, count)
            if success:
                # Update process allocation tracking
                if pid in self.processes:
                    process = self.processes[pid]
                    if resource.name in process.allocated_resources:
                        process.allocated_resources[resource.name] += count
                    else:
                        process.allocated_resources[resource.name] = count
                
                self._log_event('allocate', pid, rid, resource.name, count, True,
                              f"Allocated {count} instance(s)")
                return True
        
        # Resource not available, add to waiting queue
        resource.request(pid)
        
        # Track in process requested resources
        if pid in self.processes:
            process = self.processes[pid]
            if resource.name in process.requested_resources:
                process.requested_resources[resource.name] += count
            else:
                process.requested_resources[resource.name] = count
        
        self._log_event('request', pid, rid, resource.name, count, False,
                       f"Waiting for {count} instance(s)")
        return False
    
    def release(self, pid: int, rid: int, count: Optional[int] = None) -> int:
        """Release resources from a process.
        
        Returns the number of instances released.
        """
        if rid not in self.resources:
            return 0
        
        resource = self.resources[rid]
        released = resource.release(pid, count)
        
        if released > 0:
            # Update process allocation tracking
            if pid in self.processes:
                process = self.processes[pid]
                if resource.name in process.allocated_resources:
                    process.allocated_resources[resource.name] -= released
                    if process.allocated_resources[resource.name] <= 0:
                        del process.allocated_resources[resource.name]
            
            self._log_event('release', pid, rid, resource.name, released, True,
                          f"Released {released} instance(s)")
        
        return released
    
    def release_all(self, pid: int) -> Dict[int, int]:
        """Release all resources held by a process.
        
        Returns a dict of resource_id -> released_count.
        """
        released = {}
        for rid, resource in self.resources.items():
            count = resource.release(pid)
            if count > 0:
                released[rid] = count
                self._log_event('release', pid, rid, resource.name, count, True,
                              f"Released all {count} instance(s)")
        
        # Clear process allocation tracking
        if pid in self.processes:
            self.processes[pid].allocated_resources.clear()
            self.processes[pid].requested_resources.clear()
        
        return released
    
    def get_allocation_matrix(self) -> Dict[int, Dict[int, int]]:
        """Get the current allocation matrix.
        
        Returns: {pid: {rid: count}}
        """
        allocation = {}
        for rid, resource in self.resources.items():
            for pid, count in resource.allocated_to.items():
                if pid not in allocation:
                    allocation[pid] = {}
                allocation[pid][rid] = count
        return allocation
    
    def get_available_vector(self) -> Dict[int, int]:
        """Get the available resources vector.
        
        Returns: {rid: available_count}
        """
        return {rid: r.available_instances for rid, r in self.resources.items()}
    
    def get_max_matrix(self) -> Dict[int, Dict[int, int]]:
        """Get the maximum resource needs (for Banker's algorithm).
        
        Returns: {pid: {rid: max_need}}
        """
        # This would typically come from process declarations
        # For now, we'll estimate based on current allocation + requested
        max_matrix = {}
        for pid in self.processes:
            max_matrix[pid] = {}
            process = self.processes[pid]
            for rid, resource in self.resources.items():
                allocated = resource.get_allocated_count(pid)
                # Assume max = allocated + 2 (for demonstration)
                max_matrix[pid][rid] = allocated + 2
        return max_matrix
    
    def get_status(self) -> Dict:
        """Get the current resource status."""
        return {
            'resources': [
                {
                    'id': r.rid,
                    'name': r.name,
                    'type': r.resource_type.value,
                    'total': r.total_instances,
                    'available': r.available_instances,
                    'allocated_to': dict(r.allocated_to),
                    'waiting': list(r.waiting_queue)
                }
                for r in self.resources.values()
            ],
            'allocation_matrix': self.get_allocation_matrix(),
            'available': self.get_available_vector()
        }
    
    def _log_event(self, event_type: str, pid: int, rid: int, 
                   resource_name: str, count: int, success: bool,
                   message: str = "") -> None:
        """Log a resource allocation event."""
        event = AllocationEvent(
            timestamp=self.current_time,
            event_type=event_type,
            process_id=pid,
            resource_id=rid,
            resource_name=resource_name,
            count=count,
            success=success,
            message=message
        )
        self.allocation_history.append(event)
    
    def set_time(self, time: int) -> None:
        """Set the current simulation time."""
        self.current_time = time
    
    def reset(self) -> None:
        """Reset the resource manager to initial state."""
        for resource in self.resources.values():
            resource.reset()
        self.processes.clear()
        self.allocation_history.clear()
        self.current_time = 0
