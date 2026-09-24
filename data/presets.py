"""Sample workloads."""
import random
from core.models import Process, Burst


def simple_cpu():
    return [
        Process("P1", 0, [Burst("CPU", 6)]),
        Process("P2", 1, [Burst("CPU", 3)]),
        Process("P3", 2, [Burst("CPU", 8)]),
        Process("P4", 3, [Burst("CPU", 4)]),
        Process("P5", 4, [Burst("CPU", 5)]),
    ]


def mixed_io():
    """CPU + I/O mixed workload."""
    return [
        Process("P1", 0, [Burst("CPU", 4), Burst("IO", 3), Burst("CPU", 3)]),
        Process("P2", 1, [Burst("CPU", 5), Burst("IO", 2), Burst("CPU", 2)]),
        Process("P3", 2, [Burst("CPU", 2), Burst("IO", 4), Burst("CPU", 3)]),
        Process("P4", 3, [Burst("CPU", 6)]),
        Process("P5", 4, [Burst("CPU", 3), Burst("IO", 2), Burst("CPU", 2)]),
    ]


def random_workload(n=6, io_ratio=0.4, seed=None):
    if seed is not None:
        random.seed(seed)
    procs = []
    for i in range(n):
        bursts = [Burst("CPU", random.randint(2, 8))]
        # Optional IO + CPU
        if random.random() < io_ratio:
            bursts.append(Burst("IO", random.randint(1, 4)))
            bursts.append(Burst("CPU", random.randint(1, 6)))
        procs.append(
            Process(
                f"P{i+1}",
                arrival=random.randint(0, 5),
                bursts=bursts,
                priority=random.randint(1, 5),
            )
        )
    return procs