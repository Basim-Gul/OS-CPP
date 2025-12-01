"""Resources package for OS simulation."""

from .resource_manager import ResourceManager
from .rag import ResourceAllocationGraph
from .deadlock_detector import DeadlockDetector
from .bankers_algorithm import BankersAlgorithm
from .deadlock_resolver import DeadlockResolver

__all__ = [
    'ResourceManager',
    'ResourceAllocationGraph',
    'DeadlockDetector',
    'BankersAlgorithm',
    'DeadlockResolver'
]
