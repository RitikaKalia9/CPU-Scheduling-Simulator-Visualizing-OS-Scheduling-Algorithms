# ⚙️ CPU Scheduling Simulator

> An interactive web application to **visualize, compare, and analyze** the CPU scheduling algorithms used in modern Operating Systems — with support for **CPU + I/O mixed workloads**, **preemptive scheduling**, and **priority aging**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Overview

CPU scheduling is one of the most fundamental responsibilities of an Operating System. This project simulates how an OS kernel decides **which process runs on the CPU next** — and visualizes the outcome in real time.

Unlike textbook implementations that only consider pure CPU bursts, this simulator supports **realistic processes with alternating CPU and I/O bursts**, mirroring how actual workloads behave.

### What it does

- Simulates **8 scheduling algorithms** end-to-end
- Handles **mixed CPU + I/O workloads** (a process can block, run I/O, then return to the ready queue)
- Visualizes execution with **Gantt charts** (CPU timeline and I/O timeline separately)
- Computes **industry-standard metrics**: waiting time, turnaround, response time, CPU utilization, throughput
- Animates the **5-state process lifecycle** and **3 types of OS schedulers**
- Supports **Static and Dynamic (aging) Priority Scheduling**

---

## 🧠 Algorithms Implemented

| # | Algorithm | Preemptive | Key Idea |
|---|-----------|------------|----------|
| 1 | **FCFS** | ❌ | First-Come First-Served — simple FIFO |
| 2 | **SJF** | ❌ | Shortest Job First — minimizes average wait |
| 3 | **SRTN** | ✅ | Shortest Remaining Time Next — preemptive SJF |
| 4 | **Round Robin** | ✅ | Fixed time quantum — fair & responsive |
| 5 | **LJF** | ❌ | Longest Job First — good for long jobs with deadlines |
| 6 | **LRTN** | ✅ | Longest Remaining Time Next — preemptive LJF |
| 7 | **Priority (Static)** | ✅ | Fixed priority — higher priority runs first |
| 8 | **Priority (Dynamic)** | ✅ | Aging — priority increases with waiting time |

### Metrics Computed

- **Completion Time** — when the process finishes
- **Turnaround Time** = Completion − Arrival
- **Waiting Time** = Turnaround − Total CPU − Total I/O
- **Response Time** = First CPU allocation − Arrival
- **CPU Utilization** = busy_time / total_time × 100%
- **Throughput** = processes / total_time

---

## 🎨 Features

### 🏠 Home Page
- Animated **5-state process lifecycle diagram** (New → Ready → Running → Waiting → Terminated)
- Grid of algorithm cards with one-line descriptions
- Static vs Dynamic priority comparison

### 🧠 Learn Page
- Animated illustration of the **3 types of schedulers**:
  - Long-Term (Job) Scheduler
  - Short-Term (CPU) Scheduler
  - Medium-Term Scheduler (swapping)
- Comparison table of pros/cons for all algorithms

### 🚀 Simulator Page
- **4 workload sources**:
  - Simple CPU-only workload
  - Mixed CPU + I/O workload
  - Random workload generator (configurable size + I/O ratio)
  - Manual input (CSV-style)
- Configurable **time quantum** (RR) and **aging rate** (Dynamic Priority)
- Dual **Gantt charts** — CPU timeline and I/O timeline
- **Per-process table** with all computed metrics
- **Compare-all mode** — runs all 8 algorithms side by side

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Frontend | Streamlit (with custom HTML/CSS animations) |
| Visualization | Matplotlib |
| Data | Pandas, NumPy |
| Architecture | Modular (core / ui / data) |

---

## 📁 Project Structure
CPU-Scheduler/
├── app.py # Streamlit entry point (routing)
├── requirements.txt
├── README.md
├── core/
│ ├── models.py # Process, Burst dataclasses
│ └── algorithms.py # All 8 scheduling algorithms
├── ui/
│ ├── styles.py # Custom CSS (glassmorphism theme)
│ ├── state_diagram.py # Animated 5-state diagram
│ ├── scheduler_types.py # Long/Short/Medium scheduler animation
│ └── gantt.py # Matplotlib Gantt renderer
└── data/
└── presets.py # Sample + random workload generators

text

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Ritikakalia1/cpu-scheduler.git
cd cpu-scheduler

# 2. (Optional but recommended) Create a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
The app opens automatically at http://localhost:8501.

🧪 Example Workload
Mixed CPU + I/O workload (available as a preset in the app):

PID	Arrival	Bursts
P1	0	CPU(4) → IO(3) → CPU(3)
P2	1	CPU(5) → IO(2) → CPU(2)
P3	2	CPU(2) → IO(4) → CPU(3)
P4	3	CPU(6)
P5	4	CPU(3) → IO(2) → CPU(2)
Running SRTN on this workload produces:

Two separate Gantt charts — CPU timeline and I/O timeline

Per-process waiting, turnaround, and response times

Live comparison against the other 7 algorithms

🔬 Design Decisions
1. Why tick-by-tick simulation for preemptive algorithms?
Preemptive algorithms (SRTN, LRTN, Dynamic Priority) advance 1 time unit at a time. This is slower but ensures correct preemption when a shorter/longer job arrives mid-execution. A shortcut that runs full bursts would break correctness.

2. Why model I/O explicitly?
Real processes alternate between CPU and I/O. Modeling I/O as a blocking burst lets the scheduler demonstrate realistic CPU idling, I/O-wait processes, and correct Round Robin behavior (a process goes to the ready queue after its I/O completes).

3. Why aging in Dynamic Priority?
Pure priority scheduling starves low-priority processes. Aging (priority increases the longer a process waits) is the standard fix used in real kernels (e.g., Linux CFS, Windows).

4. Why separate CPU and I/O Gantt charts?
Because I/O operations run in parallel with CPU execution on modern hardware. Showing them on the same axis would be misleading — two charts tell the true story.

⏱️ Complexity Analysis
Let N = number of processes, T = total simulation time (ticks).

Non-Preemptive Algorithms (FCFS, SJF, LJF, Priority-Static)
Operation	Complexity
Decision per job	O(N) — scan for best candidate
Total	O(N²) — N jobs × O(N) decision
Preemptive Algorithms (SRTN, LRTN, RR, Priority-Dynamic)
Operation	Complexity
Decision per tick	O(N) — re-evaluate ready set
Total	O(N × T) — dominated by tick count
Why tick-by-tick? Preemption requires re-evaluating at every time unit — a new arrival mid-burst must be able to interrupt the running process. This is the price of correctness.

Space Complexity
Algorithm	Space
All algorithms	O(N + T) — processes + timeline entries
Practical Note
For a typical demo (N ≤ 10, T ≤ 200), the tick-by-tick approach is ~2000 operations — sub-millisecond in Python. Real kernels use more efficient event-driven simulations.

🎓 Concepts Demonstrated
Process lifecycle and state transitions

Context switching and PCB management

Scheduling queues (ready, wait, job pool)

Preemptive vs Non-Preemptive scheduling

Starvation and aging

Convoy effect (FCFS)

Time quantum tuning (Round Robin)

CPU + I/O overlap

Algorithm complexity trade-offs

📈 Learning Outcomes
By building this project, I gained practical experience with:

Designing a modular Python application with clean separation of concerns

Implementing classical OS algorithms with correct preemption semantics

Handling stateful simulation (remaining time, current burst, I/O blocking)

Building custom Streamlit UIs with HTML/CSS animations

Rendering Matplotlib Gantt charts embedded in web dashboards

Computing and comparing performance metrics across algorithms

🚀 Future Enhancements
□ Multilevel Feedback Queue (MLFQ) with configurable levels
□ Multiprocessor scheduling (2+ cores with load balancing)
□ Real-time scheduling (Rate Monotonic, Earliest Deadline First)
□ Unit tests with pytest for each algorithm
□ Live deployment on Streamlit Cloud
□ Export results to CSV / PDF
□ Context switch overhead simulation
📄 License
This project is licensed under the MIT License.
