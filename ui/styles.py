"""Inject global CSS."""
import streamlit as st


CSS = """
<style>
/* ---------- Global ---------- */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
.main {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #e2e8f0;
}
h1, h2, h3 { color: #f1f5f9 !important; letter-spacing: -0.02em; }

/* ---------- Hero ---------- */
.hero {
    background: linear-gradient(120deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(99, 102, 241, 0.4);
}
.hero h1 { font-size: 3rem; margin: 0; color: white !important; }
.hero p  { font-size: 1.15rem; color: #f1f5f9; margin-top: .6rem; opacity: .95; }

/* ---------- Cards ---------- */
.card {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.25);
    transition: transform .2s, border-color .2s;
}
.card:hover { transform: translateY(-2px); border-color: #6366f1; }

/* ---------- Process state diagram ---------- */
.state-stage {
    display: flex; justify-content: space-between; align-items: center;
    position: relative; height: 220px; padding: 0 30px;
    background: rgba(15, 23, 42, .7);
    border-radius: 20px; border: 1px dashed rgba(148,163,184,.3);
    margin-bottom: 1rem; overflow: hidden;
}
.state-node {
    width: 130px; height: 130px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: .95rem; color: white;
    box-shadow: 0 0 30px currentColor;
    animation: pulse 2s infinite ease-in-out;
    position: relative; z-index: 2;
}
@keyframes pulse {
    0%, 100% { transform: scale(1);   opacity: 1; }
    50%      { transform: scale(1.08); opacity: .85; }
}
.n-new       { background: radial-gradient(circle, #64748b, #334155); color: #cbd5e1; }
.n-ready     { background: radial-gradient(circle, #22c55e, #15803d); color: #dcfce7; }
.n-running   { background: radial-gradient(circle, #3b82f6, #1d4ed8); color: #dbeafe; }
.n-waiting   { background: radial-gradient(circle, #eab308, #a16207); color: #fef9c3; }
.n-terminated{ background: radial-gradient(circle, #ef4444, #991b1b); color: #fee2e2; }

/* ---------- Metric chips ---------- */
.metric {
    background: linear-gradient(135deg, #1e293b, #334155);
    border-left: 4px solid #6366f1;
    padding: .9rem 1.1rem;
    border-radius: 10px;
    text-align: center;
}
.metric .v { font-size: 1.6rem; font-weight: 800; color: #a5b4fc; display:block; }
.metric .l { font-size: .78rem; color: #94a3b8; text-transform: uppercase; letter-spacing: .08em; }

/* ---------- Algorithm card ---------- */
.algo-card {
    background: linear-gradient(135deg, rgba(99,102,241,.15), rgba(139,92,246,.1));
    border: 1px solid rgba(139, 92, 246, .35);
    border-radius: 14px; padding: 1rem 1.2rem; height: 100%;
}
.algo-card h4 { color: #c4b5fd !important; margin: 0 0 .3rem 0; }
.algo-card p  { font-size: .85rem; color: #cbd5e1; margin: 0; }

/* ---------- Scheduler types animation ---------- */
.sched-flow {
    display: flex; align-items: center; justify-content: space-around;
    padding: 1.5rem; background: rgba(15,23,42,.6); border-radius: 16px;
    border: 1px solid rgba(148,163,184,.15);
}
.sched-box {
    text-align: center; color: #e2e8f0; font-size: .85rem; font-weight: 600;
    padding: .8rem; border-radius: 12px; min-width: 110px;
    animation: slide 3s infinite ease-in-out;
}
@keyframes slide {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-6px); }
}
.sb-new     { background: #475569; }
.sb-ready   { background: #16a34a; }
.sb-cpu     { background: #2563eb; }
.sb-io      { background: #ca8a04; }
.sb-done    { background: #dc2626; }
.arrow      { color: #94a3b8; font-size: 1.6rem; animation: fade 1.5s infinite; }
@keyframes fade { 0%,100%{opacity:.3} 50%{opacity:1} }

/* ---------- Streamlit tweaks ---------- */
.stButton>button {
    background: linear-gradient(120deg, #6366f1, #8b5cf6);
    color: white; border: none; border-radius: 10px;
    padding: .55rem 1.4rem; font-weight: 600;
    transition: transform .15s;
}
.stButton>button:hover { transform: translateY(-2px); }
.stTabs [data-baseweb="tab"] { font-weight: 600; }
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)