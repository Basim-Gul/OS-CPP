"""Synchronization package for OS simulation."""

from .sync_manager import SyncManager
from .critical_section import CriticalSection
from .race_detector import RaceConditionDemo

__all__ = [
    'SyncManager',
    'CriticalSection',
    'RaceConditionDemo'
]
