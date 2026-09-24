"""
All scheduling algorithms.
Every algorithm returns:
    (processes, cpu_timeline, io_timeline)
where cpu_timeline/io_timeline are lists of (pid_or_"IDLE", start, end).
"""
import copy
from typing import List, Tuple
from .models import Process, Burst


Timeline = List[Tuple[str, int, int]]


# ---------------- helpers ----------------
def _first_cpu_left(p: Process) -> int:
    """Return remaining CPU needed for the process's current CPU burst."""
    return p._cpu_left


def _advance(p: Process, dt: int) -> None:
    p._cpu_left -= dt


def _strip(procs: List[Process]) -> List[Process]:
    """Deep-copy processes and attach private working state."""
    out = copy.deepcopy(procs)
    for p in out:
        p._cpu_left = p.bursts[0].length if p.bursts else 0
        p._burst_idx = 0
        p._io_left = 0
        p._in_io = False
    return out


def _finalize(processes: List[Process]) -> None:
    for p in processes:
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.total_cpu - p.total_io
        if p.response == -1:
            p.response = p.start - p.arrival


def _push_segment(timeline: Timeline, pid: str, start: int, end: int):
    if end <= start:
        return
    if timeline and timeline[-1][0] == pid and timeline[-1][2] == start:
        timeline[-1] = (pid, timeline[-1][1], end)
    else:
        timeline.append((pid, start, end))


# ---------------- algorithms ----------------

def fcfs(procs: List[Process], **_) -> Tuple:
    ps = _strip(procs)
    ps.sort(key=lambda p: (p.arrival, p.pid))
    time = 0
    cpu_tl: Timeline = []
    io_tl: Timeline = []
    for p in ps:
        if time < p.arrival:
            cpu_tl.append(("IDLE", time, p.arrival))
            time = p.arrival
        p.start = time
        p.response = p.start - p.arrival
        while p._burst_idx < len(p.bursts):
            b = p.bursts[p._burst_idx]
            if b.kind == "CPU":
                _push_segment(cpu_tl, p.pid, time, time + b.length)
                time += b.length
                p.cpu_time += b.length
            else:
                _push_segment(io_tl, p.pid, time, time + b.length)
                time += b.length
                p.io_time += b.length
            p._burst_idx += 1
        p.completion = time
        p._cpu_left = 0
    _finalize(ps)
    return ps, cpu_tl, io_tl


def sjf(procs: List[Process], **_) -> Tuple:
    """Non-preemptive shortest job first (by total CPU)."""
    ps = _strip(procs)
    remaining = ps[:]
    done = []
    time = 0
    cpu_tl: Timeline = []
    io_tl: Timeline = []

    while remaining:
        avail = [p for p in remaining if p.arrival <= time]
        if not avail:
            nxt = min(p.arrival for p in remaining)
            cpu_tl.append(("IDLE", time, nxt))
            time = nxt
            continue
        p = min(avail, key=lambda x: (x.total_cpu, x.arrival, x.pid))
        remaining.remove(p)
        p.start = time
        p.response = p.start - p.arrival
        while p._burst_idx < len(p.bursts):
            b = p.bursts[p._burst_idx]
            if b.kind == "CPU":
                _push_segment(cpu_tl, p.pid, time, time + b.length)
                time += b.length
                p.cpu_time += b.length
            else:
                _push_segment(io_tl, p.pid, time, time + b.length)
                time += b.length
                p.io_time += b.length
            p._burst_idx += 1
        p.completion = time
        done.append(p)
    _finalize(done)
    return done, cpu_tl, io_tl


def srtn(procs: List[Process], **_) -> Tuple:
    """Shortest Remaining Time Next (preemptive SJF by CPU burst)."""
    ps = _strip(procs)
    n = len(ps)
    time = 0
    completed = 0
    cpu_tl: Timeline = []
    io_tl: Timeline = []

    # IO devices: assume unlimited, so IO runs in parallel — we just log
    io_queue = []  # (process, finish_time)

    while completed < n:
        # Release IO that has finished
        ready_now = []
        for p in io_queue:
            if p.arrival <= time and not p._in_io:
                pass
        # Simplify: treat IO as blocking process (single device model).
        # (For educational clarity we keep IO serial to show "Waiting" state.)

        avail = [p for p in ps if p.arrival <= time and p._cpu_left > 0]
        if not avail:
            time += 1
            continue

        p = min(avail, key=lambda x: (x._cpu_left, x.arrival, x.pid))
        if p.response == -1:
            p.response = time - p.arrival
            p.start = time

        # Run 1 time unit
        _push_segment(cpu_tl, p.pid, time, time + 1)
        p._cpu_left -= 1
        p.cpu_time += 1
        time += 1

        if p._cpu_left == 0:
            # Move to next burst (IO)
            p._burst_idx += 1
            if p._burst_idx < len(p.bursts):
                b = p.bursts[p._burst_idx]
                _push_segment(io_tl, p.pid, time, time + b.length)
                time += b.length
                p.io_time += b.length
                p._burst_idx += 1
                # Now next CPU burst
                if p._burst_idx < len(p.bursts):
                    p._cpu_left = p.bursts[p._burst_idx].length
                else:
                    p._cpu_left = 0
            if p._cpu_left == 0:
                p.completion = time
                completed += 1

    _finalize(ps)
    return ps, cpu_tl, io_tl


def round_robin(procs: List[Process], quantum: int = 2, **_) -> Tuple:
    ps = _strip(procs)
    ps.sort(key=lambda p: (p.arrival, p.pid))
    n = len(ps)
    time = 0
    idx = 0
    queue = []
    cpu_tl: Timeline = []
    io_tl: Timeline = []
    completed = 0

    while idx < n and ps[idx].arrival <= time:
        queue.append(ps[idx]); idx += 1

    while completed < n:
        if not queue:
            if idx < n:
                time = ps[idx].arrival
                while idx < n and ps[idx].arrival <= time:
                    queue.append(ps[idx]); idx += 1
            continue

        p = queue.pop(0)

        # Handle IO first if next burst is IO
        if p._cpu_left == 0 and p._burst_idx < len(p.bursts) and p.bursts[p._burst_idx].kind == "IO":
            b = p.bursts[p._burst_idx]
            _push_segment(io_tl, p.pid, time, time + b.length)
            time += b.length
            p.io_time += b.length
            p._burst_idx += 1
            if p._burst_idx < len(p.bursts):
                p._cpu_left = p.bursts[p._burst_idx].length
            # Release any arrivals during IO
            while idx < n and ps[idx].arrival <= time:
                queue.append(ps[idx]); idx += 1

        if p.response == -1 and p._cpu_left > 0:
            p.response = time - p.arrival
            p.start = time

        run = min(quantum, p._cpu_left)
        if run > 0:
            _push_segment(cpu_tl, p.pid, time, time + run)
            time += run
            p._cpu_left -= run
            p.cpu_time += run

        # Release arrivals
        while idx < n and ps[idx].arrival <= time:
            queue.append(ps[idx]); idx += 1

        # Is the process finished?
        if p._cpu_left == 0:
            p._burst_idx += 1
            if p._burst_idx >= len(p.bursts):
                p.completion = time
                completed += 1
            else:
                queue.append(p)
        else:
            queue.append(p)

    _finalize(ps)
    return ps, cpu_tl, io_tl


def ljf(procs: List[Process], **_) -> Tuple:
    """Longest Job First (non-preemptive)."""
    ps = _strip(procs)
    remaining = ps[:]
    done = []
    time = 0
    cpu_tl: Timeline = []
    io_tl: Timeline = []

    while remaining:
        avail = [p for p in remaining if p.arrival <= time]
        if not avail:
            nxt = min(p.arrival for p in remaining)
            cpu_tl.append(("IDLE", time, nxt))
            time = nxt
            continue
        p = max(avail, key=lambda x: (x.total_cpu, -x.arrival, x.pid))
        remaining.remove(p)
        p.start = time
        p.response = p.start - p.arrival
        while p._burst_idx < len(p.bursts):
            b = p.bursts[p._burst_idx]
            if b.kind == "CPU":
                _push_segment(cpu_tl, p.pid, time, time + b.length)
                time += b.length
                p.cpu_time += b.length
            else:
                _push_segment(io_tl, p.pid, time, time + b.length)
                time += b.length
                p.io_time += b.length
            p._burst_idx += 1
        p.completion = time
        done.append(p)
    _finalize(done)
    return done, cpu_tl, io_tl


def lrtn(procs: List[Process], **_) -> Tuple:
    """Longest Remaining Time Next (preemptive LJF)."""
    ps = _strip(procs)
    n = len(ps)
    time = 0
    completed = 0
    cpu_tl: Timeline = []
    io_tl: Timeline = []

    while completed < n:
        avail = [p for p in ps if p.arrival <= time and p._cpu_left > 0]
        if not avail:
            time += 1
            continue
        p = max(avail, key=lambda x: (x._cpu_left, -x.arrival, x.pid))
        if p.response == -1:
            p.response = time - p.arrival
            p.start = time

        _push_segment(cpu_tl, p.pid, time, time + 1)
        p._cpu_left -= 1
        p.cpu_time += 1
        time += 1

        if p._cpu_left == 0:
            p._burst_idx += 1
            if p._burst_idx < len(p.bursts):
                b = p.bursts[p._burst_idx]
                _push_segment(io_tl, p.pid, time, time + b.length)
                time += b.length
                p.io_time += b.length
                p._burst_idx += 1
                if p._burst_idx < len(p.bursts):
                    p._cpu_left = p.bursts[p._burst_idx].length
            if p._cpu_left == 0:
                p.completion = time
                completed += 1

    _finalize(ps)
    return ps, cpu_tl, io_tl


def priority_scheduling(procs: List[Process], mode: str = "static",
                        aging_rate: int = 1, **_) -> Tuple:
    """
    Preemptive priority scheduling.
    mode = "static"  → priority never changes
    mode = "dynamic" → aging: waiting time increases effective priority
    """
    ps = _strip(procs)
    n = len(ps)
    time = 0
    completed = 0
    cpu_tl: Timeline = []
    io_tl: Timeline = []
    wait_since_last_cpu = {p.pid: 0 for p in ps}

    while completed < n:
        avail = [p for p in ps if p.arrival <= time and p._cpu_left > 0]
        if not avail:
            time += 1
            continue

        if mode == "dynamic":
            # effective priority = priority - aging_factor
            # lower effective value wins
            def key(p):
                eff = p.priority - (wait_since_last_cpu[p.pid] // max(1, aging_rate))
                return (eff, p.arrival, p.pid)
        else:
            def key(p):
                return (p.priority, p.arrival, p.pid)

        p = min(avail, key=key)
        if p.response == -1:
            p.response = time - p.arrival
            p.start = time

        _push_segment(cpu_tl, p.pid, time, time + 1)
        p._cpu_left -= 1
        p.cpu_time += 1
        wait_since_last_cpu[p.pid] = 0
        time += 1

        # all other ready processes age
        for q in avail:
            if q.pid != p.pid:
                wait_since_last_cpu[q.pid] += 1

        if p._cpu_left == 0:
            p._burst_idx += 1
            if p._burst_idx < len(p.bursts):
                b = p.bursts[p._burst_idx]
                _push_segment(io_tl, p.pid, time, time + b.length)
                time += b.length
                p.io_time += b.length
                p._burst_idx += 1
                if p._burst_idx < len(p.bursts):
                    p._cpu_left = p.bursts[p._burst_idx].length
            if p._cpu_left == 0:
                p.completion = time
                completed += 1

    _finalize(ps)
    return ps, cpu_tl, io_tl


ALGORITHMS = {
    "FCFS":  fcfs,
    "SJF":   sjf,
    "SRTN":  srtn,
    "RR":    round_robin,
    "LJF":   ljf,
    "LRTN":  lrtn,
    "Priority (Static)":  lambda ps, **kw: priority_scheduling(ps, mode="static", **kw),
    "Priority (Dynamic)": lambda ps, **kw: priority_scheduling(ps, mode="dynamic", **kw),
}


def compute_metrics(processes: List[Process]) -> dict:
    n = len(processes)
    if n == 0:
        return {}
    return {
        "avg_waiting": round(sum(p.waiting for p in processes) / n, 2),
        "avg_turnaround": round(sum(p.turnaround for p in processes) / n, 2),
        "avg_response": round(sum(p.response for p in processes) / n, 2),
        "cpu_util": None,  # filled by UI from timeline
    }