Absolutely — here is the **entire README as one single copy-paste block**. Save it directly as `README.md`.

````markdown
# ⚙️ CPU Scheduling Simulator

> An interactive web application to **visualize, compare, and analyze** CPU scheduling algorithms used in Operating Systems — with support for **CPU + I/O mixed workloads**, **preemptive scheduling**, and **priority aging**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Overview

CPU scheduling is one of the fundamental responsibilities of an Operating System. This project simulates how an OS decides **which process runs on the CPU next** and visualizes the scheduling outcome.

Unlike basic textbook implementations that only consider pure CPU bursts, this simulator supports **realistic processes with alternating CPU and I/O bursts**, allowing processes to block for I/O and later return to the ready queue.

### What It Does

- Simulates **8 scheduling algorithms**
- Handles **mixed CPU + I/O workloads**
- Supports **preemptive scheduling**
- Visualizes execution using **Gantt charts**
- Computes standard scheduling metrics
- Animates the **5-state process lifecycle**
- Demonstrates the **3 types of OS schedulers**
- Supports **Static and Dynamic (aging) Priority Scheduling**
- Provides **algorithm comparison**

---

## 🧠 Algorithms Implemented

| # | Algorithm | Preemptive | Key Idea |
|---|---|---|---|
| 1 | **FCFS** | ❌ | First-Come First-Served — simple FIFO scheduling |
| 2 | **SJF** | ❌ | Shortest Job First — selects the shortest available job |
| 3 | **SRTN** | ✅ | Shortest Remaining Time Next — preemptive SJF |
| 4 | **Round Robin** | ✅ | Uses a fixed time quantum for fair CPU sharing |
| 5 | **LJF** | ❌ | Longest Job First — selects the longest available job |
| 6 | **LRTN** | ✅ | Longest Remaining Time Next — preemptive LJF |
| 7 | **Priority (Static)** | ✅ | Fixed priority — higher-priority processes run first |
| 8 | **Priority (Dynamic)** | ✅ | Aging — priority changes based on waiting time |

---

## 📊 Metrics Computed

The simulator calculates the following metrics:

- **Completion Time** — time at which the process finishes
- **Turnaround Time** = Completion Time − Arrival Time
- **Waiting Time** = Turnaround Time − Total CPU Time − Total I/O Time
- **Response Time** = First CPU Allocation − Arrival Time
- **CPU Utilization** = `(Busy Time / Total Time) × 100`
- **Throughput** = `Number of Completed Processes / Total Time`

---

## 🎨 Features

### 🏠 Home Page

- Animated **5-state process lifecycle diagram**
  - New
  - Ready
  - Running
  - Waiting
  - Terminated
- Algorithm cards with one-line descriptions
- Static vs Dynamic Priority comparison

### 🧠 Learn Page

Explains the **3 types of OS schedulers**:

- **Long-Term (Job) Scheduler**
- **Short-Term (CPU) Scheduler**
- **Medium-Term Scheduler (Swapping)**

Also includes a comparison of the advantages and disadvantages of the implemented algorithms.

### 🚀 Simulator Page

The simulator provides four workload sources:

1. **Simple CPU-only workload**
2. **Mixed CPU + I/O workload**
3. **Random workload generator**
4. **Manual input**

Additional controls include:

- Configurable **time quantum** for Round Robin
- Configurable **aging rate** for Dynamic Priority
- CPU Gantt chart
- I/O Gantt chart
- Per-process performance table
- **Compare-All mode** for all 8 algorithms

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Frontend | Streamlit |
| Visualization | Matplotlib |
| Data Processing | Pandas, NumPy |
| Architecture | Modular (`core / ui / data`) |

---

## 📁 Project Structure

```text
CPU-Scheduler/
│
├── app.py                     # Streamlit entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── core/
│   ├── __init__.py
│   ├── models.py              # Process and Burst data models
│   └── algorithms.py          # Scheduling algorithms
│
├── ui/
│   ├── __init__.py
│   ├── styles.py              # Custom CSS
│   ├── state_diagram.py       # 5-state process lifecycle
│   ├── scheduler_types.py     # OS scheduler animation
│   └── gantt.py               # Gantt chart renderer
│
└── data/
    └── presets.py             # Sample and random workloads
````

---

## ⚙️ Installation & Setup

### Prerequisites

* Python **3.10 or higher**
* `pip`

### 1. Clone the Repository

```bash
git clone https://github.com/Ritikakalia1/cpu-scheduler.git
cd cpu-scheduler
```

### 2. Create a Virtual Environment

#### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 🧪 Example Workload

A sample mixed CPU + I/O workload is available as a preset in the application.

| PID | Arrival Time | Bursts                   |
| --- | -----------: | ------------------------ |
| P1  |            0 | CPU(4) → I/O(3) → CPU(3) |
| P2  |            1 | CPU(5) → I/O(2) → CPU(2) |
| P3  |            2 | CPU(2) → I/O(4) → CPU(3) |
| P4  |            3 | CPU(6)                   |
| P5  |            4 | CPU(3) → I/O(2) → CPU(2) |

Running SRTN on this workload produces:

* CPU and I/O Gantt charts
* Per-process waiting, turnaround, and response times
* Performance comparison with the other scheduling algorithms

---

## 🔬 Design Decisions

### 1. Why Tick-by-Tick Simulation for Preemptive Algorithms?

Preemptive algorithms such as SRTN, LRTN, and Dynamic Priority advance one time unit at a time.

This allows the simulator to detect events such as:

* New process arrivals
* I/O completion
* Priority changes
* Preemption

A burst-level shortcut could miss a preemption event occurring in the middle of a CPU burst.

---

### 2. Why Model I/O Explicitly?

Real processes frequently alternate between CPU execution and I/O operations.

For example:

```text
CPU → I/O → CPU → I/O → CPU
```

When a process performs I/O, it leaves the CPU and enters the waiting state. After its I/O completes, it returns to the ready queue.

This allows the simulator to demonstrate:

* CPU blocking
* I/O waiting
* CPU and I/O overlap
* Ready-queue re-entry
* More realistic Round Robin behavior

---

### 3. Why Aging in Dynamic Priority?

A pure priority scheduler can cause **starvation**, where low-priority processes wait for a long time.

Aging addresses this by gradually increasing the priority of a waiting process.

This allows processes that have waited for a long time to eventually receive CPU time.

---

### 4. Why Separate CPU and I/O Gantt Charts?

CPU execution and I/O operations can overlap in time.

Therefore, the simulator displays them using separate timelines:

```text
CPU Timeline
| P1 | P2 | P3 | P1 |

I/O Timeline
     | P2 |    | P3 |
```

This makes CPU execution and I/O activity easier to understand.

---

## ⏱️ Complexity Analysis

Let:

* `N` = number of processes
* `T` = total simulation time in ticks

### Non-Preemptive Algorithms

Examples:

* FCFS
* SJF
* LJF
* Static Priority

| Operation           | Complexity          |
| ------------------- | ------------------- |
| Candidate selection | O(N)                |
| Overall simulation  | Approximately O(N²) |

The scheduler may scan the ready processes to select the next process.

### Preemptive Algorithms

Examples:

* SRTN
* LRTN
* Round Robin
* Dynamic Priority

| Operation             | Complexity |
| --------------------- | ---------- |
| Decision at each tick | O(N)       |
| Overall simulation    | O(N × T)   |

The tick-based approach allows the simulator to detect arrivals and other events that may cause preemption.

### Space Complexity

| Component           | Complexity |
| ------------------- | ---------- |
| Process data        | O(N)       |
| Simulation timeline | O(T)       |
| Overall             | O(N + T)   |

### Practical Note

For a typical demonstration with:

```text
N ≤ 10
T ≤ 200
```

the number of simulation steps remains small and is easily handled by Python.

Real operating systems use more sophisticated event-driven mechanisms and scheduling data structures rather than repeatedly scanning every process at every time unit.

---

## 🎓 Concepts Demonstrated

The project demonstrates the following Operating Systems concepts:

* Process lifecycle and state transitions
* Process Control Block (PCB) concepts
* Ready and waiting queues
* Preemptive vs non-preemptive scheduling
* Context switching
* Starvation and aging
* Convoy effect
* Time quantum in Round Robin
* CPU + I/O overlap
* Scheduling performance metrics
* Algorithm complexity
* Scheduling trade-offs

---

## 📈 Learning Outcomes

By building this project, I gained practical experience with:

* Designing a modular Python application
* Separating application logic into `core`, `ui`, and `data` modules
* Implementing classical CPU scheduling algorithms
* Implementing preemption and stateful simulation
* Handling CPU and I/O bursts
* Building interactive Streamlit interfaces
* Creating custom HTML/CSS UI components
* Rendering Matplotlib Gantt charts
* Computing scheduling performance metrics
* Comparing multiple algorithms using a common workload

---

## 🚀 Future Enhancements

The following features can be added in future versions:

* [ ] Multilevel Feedback Queue (MLFQ) with configurable levels
* [ ] Multiprocessor scheduling with 2+ simulated CPUs
* [ ] Load balancing between simulated CPUs
* [ ] Real-time scheduling algorithms

  * Rate Monotonic Scheduling
  * Earliest Deadline First
* [ ] Unit tests using `pytest`
* [ ] Live deployment
* [ ] Export results to CSV/PDF
* [ ] Context-switch overhead simulation

---

## 📄 License

This project is licensed under the **MIT License**.

```
```
