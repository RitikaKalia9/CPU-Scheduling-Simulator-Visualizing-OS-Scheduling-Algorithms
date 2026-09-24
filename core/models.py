"""Process models with CPU + I/O burst support."""
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class Burst:
    """A single burst: either CPU or IO."""
    kind: str          # "CPU" or "IO"
    length: int


@dataclass
class Process:
    pid: str
    arrival: int
    bursts: List[Burst]           # alternating CPU/IO sequence, starts & ends with CPU
    priority: int = 0             # lower = higher priority
    # ---- computed ----
    start: int = -1               # first CPU allocation
    completion: int = 0
    waiting: int = 0
    turnaround: int = 0
    response: int = -1
    cpu_time: int = 0
    io_time: int = 0
    state_history: List[Tuple[int, int, str]] = field(default_factory=list)  # (start, end, state)

    @property
    def total_cpu(self) -> int:
        return sum(b.length for b in self.bursts if b.kind == "CPU")

    @property
    def total_io(self) -> int:
        return sum(b.length for b in self.bursts if b.kind == "IO")

    @property
    def total_burst(self) -> int:
        return self.total_cpu + self.total_io

    @property
    def first_cpu(self) -> int:
        return self.bursts[0].length if self.bursts else 0