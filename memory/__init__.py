"""Memory management package for OS simulation."""

from .memory_manager import MemoryManager
from .page_table import PageTable
from .fifo_replacement import FIFOReplacement
from .lru_replacement import LRUReplacement
from .optimal_replacement import OptimalReplacement
from .clock_replacement import ClockReplacement

__all__ = [
    'MemoryManager',
    'PageTable',
    'FIFOReplacement',
    'LRUReplacement',
    'OptimalReplacement',
    'ClockReplacement'
]
