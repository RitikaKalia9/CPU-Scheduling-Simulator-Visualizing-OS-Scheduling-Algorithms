import streamlit as st


def render():
    st.markdown("### Types of Schedulers")
    st.markdown(
        "<p style='color:#94a3b8'>Three schedulers cooperate to keep the CPU busy and fair.</p>",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="algo-card">
              <h4>Long-Term (Job) Scheduler</h4>
              <p>Decides <b>which jobs enter the ready queue</b> from the job pool.
              Controls degree of multiprogramming.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="sched-flow" style="flex-direction:column;gap:.6rem">
              <div class="sched-box sb-new">JOB POOL</div>
              <div class="arrow">&#11015;</div>
              <div class="sched-box sb-ready">READY QUEUE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="algo-card">
              <h4>Short-Term (CPU) Scheduler</h4>
              <p>Picks the <b>next process for the CPU</b>. Runs every few ms -
              must be very fast.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="sched-flow" style="flex-direction:column;gap:.6rem">
              <div class="sched-box sb-ready">READY QUEUE</div>
              <div class="arrow">&#11015;</div>
              <div class="sched-box sb-cpu">CPU CORE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="algo-card">
              <h4>Medium-Term Scheduler</h4>
              <p>Handles <b>swapping</b>: suspends/resumes processes to manage
              memory pressure.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="sched-flow" style="flex-direction:column;gap:.6rem">
              <div class="sched-box sb-cpu">MAIN MEMORY</div>
              <div class="arrow">&#11014;&#11015;</div>
              <div class="sched-box sb-io">SWAP SPACE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
