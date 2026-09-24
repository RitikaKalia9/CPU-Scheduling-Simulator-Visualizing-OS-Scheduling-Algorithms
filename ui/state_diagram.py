import streamlit as st


def render():
    st.markdown("### Process State Lifecycle")
    st.markdown(
        "<p style='color:#94a3b8'>Watch a process move through the 5 canonical OS states.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="state-stage">
            <div class="state-node n-new">NEW</div>
            <div class="arrow">&#10132;</div>
            <div class="state-node n-ready" style="animation-delay:.4s">READY</div>
            <div class="arrow">&#10132;</div>
            <div class="state-node n-running" style="animation-delay:.8s">RUNNING</div>
            <div class="arrow">&#10132;</div>
            <div class="state-node n-waiting" style="animation-delay:1.2s">WAITING</div>
            <div class="arrow">&#10132;</div>
            <div class="state-node n-terminated" style="animation-delay:1.6s">TERMINATED</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="card">
              <h4>Transitions</h4>
              <ul style="color:#cbd5e1;font-size:.9rem;line-height:1.9">
                <li><b>New &rarr; Ready</b> - admitted by long-term scheduler</li>
                <li><b>Ready &rarr; Running</b> - dispatched by short-term scheduler</li>
                <li><b>Running &rarr; Waiting</b> - I/O or event wait</li>
                <li><b>Waiting &rarr; Ready</b> - I/O completes</li>
                <li><b>Running &rarr; Ready</b> - preempted</li>
                <li><b>Running &rarr; Terminated</b> - exit()</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="card">
              <h4>Quick Facts</h4>
              <ul style="color:#cbd5e1;font-size:.9rem;line-height:1.9">
                <li><b>Ready</b> queue holds processes wanting CPU</li>
                <li><b>Wait</b> queue holds processes blocked on I/O</li>
                <li>Only <b>one</b> process runs per CPU core at a time</li>
                <li><b>Context switch</b> saves/restores PCB</li>
                <li>Too many switches = overhead; too few = idle CPU</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
