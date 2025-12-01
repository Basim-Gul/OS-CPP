"""Test package for OS simulation."""

from .test_scenario_1 import test_cpu_bound_batch
from .test_scenario_2 import test_interactive_mixed
from .test_scenario_3 import test_deadlock_demo
from .test_scenario_4 import test_race_condition
from .test_scenario_5 import test_memory_thrashing

__all__ = [
    'test_cpu_bound_batch',
    'test_interactive_mixed',
    'test_deadlock_demo',
    'test_race_condition',
    'test_memory_thrashing'
]
