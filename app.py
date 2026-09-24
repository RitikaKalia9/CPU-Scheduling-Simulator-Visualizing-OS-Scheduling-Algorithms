"""
CPU Scheduling Simulator — Beautiful Streamlit Frontend
Run:  streamlit run app.py
"""
import time
import pandas as pd
import streamlit as st

from ui import styles, state_diagram, scheduler_types, gantt
from core.models import Process, Burst
from core.algorithms import ALGORITHMS, compute_metrics
from data import presets


st.set_page_config(
    page_title="CPU Scheduling Simulator",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)
styles.inject()


# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ CPU Scheduler")
    page = st.radio(
        "Navigate",
        ["🏠 Home", "🧠 Learn", "🚀 Simulator"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<p style='font-size:.8rem;color:#94a3b8'>"
        "Built with Streamlit · Matplotlib · Python</p>",
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------
# HOME
# ------------------------------------------------------------------
if page == "🏠 Home":
    st.markdown(
        """
        <div class="hero">
          <h1>⚙️ CPU Scheduling Simulator</h1>
          <p>Visualize, compare & understand OS scheduling algorithms in real time</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    chips = [
        ("6+", "Algorithms"),
        ("CPU+IO", "Mixed workload"),
        ("Aging", "Dynamic priority"),
        ("Gantt", "Visual charts"),
    ]
    for col, (v, l) in zip([c1, c2, c3, c4], chips):
        col.markdown(
            f"<div class='metric'><span class='v'>{v}</span>"
            f"<span class='l'>{l}</span></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    state_diagram.render()

    st.markdown("---")
    st.markdown("### 🎯 Supported Algorithms")
    a1, a2, a3 = st.columns(3)
    algos = [
        ("FCFS", "First-Come First-Served: simplest, non-preemptive, suffers convoy effect.", a1),
        ("SJF",  "Shortest Job First: minimizes average waiting time (non-preemptive).", a2),
        ("SRTN", "Shortest Remaining Time Next: preemptive SJF, best avg wait.", a3),
        ("RR",   "Round Robin: fair time-slicing, great for interactive systems.", a1),
        ("LJF",  "Longest Job First: good when jobs have deadlines — rarely used.", a2),
        ("LRTN", "Longest Remaining Time Next: preemptive LJF, used in some RT systems.", a3),
    ]
    for name, desc, col in algos:
        col.markdown(
            f"<div class='algo-card'><h4>{name}</h4><p>{desc}</p></div><br>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 🎛 Priority Scheduling")
    p1, p2 = st.columns(2)
    p1.markdown(
        """
        <div class="card">
          <h4>Static Priority</h4>
          <p style="color:#cbd5e1;font-size:.9rem">
          Priority fixed at process creation. Simple but
          <b>low-priority processes can starve</b>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    p2.markdown(
        """
        <div class="card">
          <h4>Dynamic Priority (Aging)</h4>
          <p style="color:#cbd5e1;font-size:.9rem">
          Priority increases the longer a process waits.
          <b>Prevents starvation</b>, used in modern OSes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------
# LEARN
# ------------------------------------------------------------------
elif page == "🧠 Learn":
    st.markdown("## 🧠 How Scheduling Works")
    scheduler_types.render()

    st.markdown("---")
    st.markdown("### 📊 Algorithm Comparison")
    df = pd.DataFrame(
        [
            ["FCFS", "No",  "Simple, fair", "Convoy effect, long wait"],
            ["SJF",  "No",  "Min avg wait", "Starvation, needs burst estimate"],
            ["SRTN", "Yes", "Best avg wait", "Frequent context switches"],
            ["RR",   "Yes", "Fair, responsive", "Quantum tuning needed"],
            ["LJF",  "No",  "Fits long jobs early", "High avg wait"],
            ["LRTN", "Yes", "Good for RT long jobs", "High avg wait"],
            ["Priority Static",  "Yes", "Important jobs first", "Starvation"],
            ["Priority Dynamic", "Yes", "No starvation (aging)", "Tuning aging rate"],
        ],
        columns=["Algorithm", "Preemptive", "Pros", "Cons"],
    )
    st.dataframe(df, use_container_width=True, hide_index=True)


# ------------------------------------------------------------------
# SIMULATOR
# ------------------------------------------------------------------
elif page == "🚀 Simulator":
    st.markdown("## 🚀 Simulator")

    # ---------- Workload configuration ----------
    with st.expander("🔧 Workload Configuration", expanded=True):
        tab_simple, tab_mixed, tab_random, tab_manual = st.tabs(
            ["Simple CPU", "Mixed CPU+IO", "Random", "Manual"]
        )

        workload = None
        with tab_simple:
            if st.button("Load Simple CPU Workload"):
                st.session_state.workload = presets.simple_cpu()
                st.success("Loaded simple CPU workload")
        with tab_mixed:
            if st.button("Load Mixed CPU + I/O Workload"):
                st.session_state.workload = presets.mixed_io()
                st.success("Loaded mixed workload")
        with tab_random:
            n = st.slider("Number of processes", 3, 12, 6)
            io_ratio = st.slider("I/O probability", 0.0, 1.0, 0.4, 0.1)
            seed = st.number_input("Seed (optional)", value=42, step=1)
            if st.button("Generate Random"):
                st.session_state.workload = presets.random_workload(
                    n=n, io_ratio=io_ratio, seed=int(seed)
                )
                st.success(f"Generated {n} random processes")
        with tab_manual:
            st.caption("Format: PID,Arrival,CPU1,IO1,CPU2,... (leave IO blank if none)")
            st.code("P1,0,5\nP2,1,3,2,2\nP3,2,6", language="text")
            manual = st.text_area("Enter workload", height=140, key="manual_input")
            if st.button("Parse Manual Input"):
                try:
                    parsed = []
                    for line in manual.strip().splitlines():
                        parts = [x.strip() for x in line.split(",") if x.strip()]
                        pid, arrival, *nums = parts
                        bursts = []
                        for i, v in enumerate(nums):
                            bursts.append(Burst("CPU" if i % 2 == 0 else "IO", int(v)))
                        parsed.append(Process(pid, int(arrival), bursts))
                    st.session_state.workload = parsed
                    st.success(f"Parsed {len(parsed)} processes")
                except Exception as e:
                    st.error(f"Parse error: {e}")

        # Show current workload
        if "workload" in st.session_state:
            st.markdown("**Current workload:**")
            rows = []
            for p in st.session_state.workload:
                seq = " → ".join(f"{b.kind}({b.length})" for b in p.bursts)
                rows.append([p.pid, p.arrival, seq, p.priority])
            st.dataframe(
                pd.DataFrame(rows, columns=["PID", "Arrival", "Bursts", "Priority"]),
                use_container_width=True, hide_index=True,
            )

    # ---------- Algorithm selection ----------
    if "workload" not in st.session_state:
        st.info("👆 Load a workload first from the panel above.")
        st.stop()

    st.markdown("### 🎛 Algorithm Settings")
    c1, c2, c3 = st.columns([2, 1, 1])
    algo = c1.selectbox("Select algorithm", list(ALGORITHMS.keys()))
    quantum = c2.number_input("Time quantum (RR only)", 1, 20, 2)
    aging_rate = c3.number_input("Aging rate (Dynamic Priority)", 1, 10, 2)

    run = st.button("▶️ Run Simulation", use_container_width=True)

    if run:
        procs = st.session_state.workload
        kwargs = {}
        if algo == "RR":
            kwargs["quantum"] = quantum
        if algo == "Priority (Dynamic)":
            kwargs["aging_rate"] = aging_rate

        with st.spinner("Scheduling..."):
            time.sleep(0.3)
            result, cpu_tl, io_tl = ALGORITHMS[algo](procs, **kwargs)

        # ---- Metrics ----
        metrics = compute_metrics(result)
        total_time = max(cpu_tl[-1][2] if cpu_tl else 1, io_tl[-1][2] if io_tl else 1)
        busy = sum(e - s for pid, s, e in cpu_tl if pid != "IDLE")
        cpu_util = round(busy / total_time * 100, 1) if total_time else 0
        throughput = round(len(result) / total_time, 3) if total_time else 0

        st.markdown("### 📈 Results")
        m1, m2, m3, m4, m5 = st.columns(5)
        for col, (v, l) in zip(
            [m1, m2, m3, m4, m5],
            [
                (metrics["avg_waiting"],    "Avg Waiting"),
                (metrics["avg_turnaround"], "Avg Turnaround"),
                (metrics["avg_response"],   "Avg Response"),
                (f"{cpu_util}%",            "CPU Utilisation"),
                (throughput,                "Throughput"),
            ],
        ):
            col.markdown(
                f"<div class='metric'><span class='v'>{v}</span>"
                f"<span class='l'>{l}</span></div>",
                unsafe_allow_html=True,
            )

        # ---- Gantt charts ----
        st.markdown("### 🎨 Gantt Charts")
        gantt.draw(cpu_tl, "CPU Timeline", kind="CPU")
        gantt.draw(io_tl,  "I/O Timeline", kind="I/O")

        # ---- Per-process table ----
        st.markdown("### 📋 Per-Process Details")
        rows = []
        for p in sorted(result, key=lambda x: x.pid):
            rows.append({
                "PID": p.pid,
                "Arrival": p.arrival,
                "CPU Total": p.total_cpu,
                "I/O Total": p.total_io,
                "Start": p.start,
                "Completion": p.completion,
                "Waiting": p.waiting,
                "Turnaround": p.turnaround,
                "Response": p.response,
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # ---- State history per process ----
        with st.expander("🔍 State Timeline (per process)"):
            for p in sorted(result, key=lambda x: x.pid):
                st.markdown(f"**{p.pid}** — started at `{p.start}`, finished at `{p.completion}`")
                states = []
                for pid, s, e in cpu_tl:
                    if pid == p.pid:
                        states.append((s, e, "RUNNING"))
                for pid, s, e in io_tl:
                    if pid == p.pid:
                        states.append((s, e, "WAITING (I/O)"))
                states.sort()
                for s, e, kind in states:
                    st.markdown(
                        f"&nbsp;&nbsp;&nbsp;`[{s:>3} → {e:>3}]` &nbsp; **{kind}**",
                        unsafe_allow_html=True,
                    )

    # ---- Comparison mode ----
    st.markdown("---")
    if st.checkbox("📊 Compare all algorithms on this workload"):
        rows = []
        for name, fn in ALGORITHMS.items():
            kwargs = {}
            if name == "RR":
                kwargs["quantum"] = quantum
            if name == "Priority (Dynamic)":
                kwargs["aging_rate"] = aging_rate
            procs, cpu_tl, io_tl = fn(st.session_state.workload, **kwargs)
            m = compute_metrics(procs)
            total_t = cpu_tl[-1][2] if cpu_tl else 1
            busy = sum(e - s for pid, s, e in cpu_tl if pid != "IDLE")
            rows.append({
                "Algorithm": name,
                "Avg Wait": m["avg_waiting"],
                "Avg Turnaround": m["avg_turnaround"],
                "Avg Response": m["avg_response"],
                "CPU Util %": round(busy / total_t * 100, 1),
                "Throughput": round(len(procs) / total_t, 3),
            })
        st.dataframe(
            pd.DataFrame(rows).sort_values("Avg Wait"),
            use_container_width=True, hide_index=True,
        )