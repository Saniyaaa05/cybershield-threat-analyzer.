import ipaddress
import json
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="CyberShield | Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ CyberShield")
st.caption("CYBERSECURITY • THREAT INTELLIGENCE • IP ANALYSIS")

st.markdown("""
Investigate public IP addresses, review reputation indicators,
and generate security investigation reports.
""")

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.header("Settings")
mode = st.sidebar.selectbox(
    "Analysis mode",
    ["Demo mode"],
)

st.sidebar.info(
    "Demo mode uses synthetic data, not live threat intelligence."
)

st.subheader("IP Investigation")

with st.form("ip_form"):
    ip_text = st.text_input(
        "Enter an IP address",
        placeholder="8.8.8.8",
    )
    submitted = st.form_submit_button(
        "🔍 Analyze IP",
        use_container_width=True,
    )

if submitted:
    try:
        address = ipaddress.ip_address(ip_text.strip())

        if not address.is_global:
            st.error(
                "Please enter a globally routable public IP address."
            )
        else:
            # Synthetic score for demonstration only.
            # It is NOT a real reputation lookup.
            result = {
                "IP Address": str(address),
                "Risk Score": 35,
                "Risk Level": "Low",
                "Abuse Reports": 12,
                "Source": "Synthetic demo data",
                "Checked At (UTC)": datetime.now(
                    timezone.utc
                ).isoformat(),
            }

            st.session_state.history.insert(0, result)
            st.success("Demo analysis completed.")

    except ValueError:
        st.error("Invalid IP address. Please try again.")

history = st.session_state.history

if history:
    latest = history[0]

    st.subheader("Investigation Results")
    st.warning(
        "DEMO ONLY: The displayed score and report count are "
        "artificial examples. They do not describe the actual IP."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Risk Score", f"{latest['Risk Score']}/100")
    c2.metric("Risk Level", latest["Risk Level"])
    c3.metric("Abuse Reports", latest["Abuse Reports"])

    st.progress(latest["Risk Score"] / 100)

    st.markdown("### Investigation details")
    st.json(latest)

    st.markdown("### Investigation history")
    df = pd.DataFrame(history)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("### Export your report")
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "Download JSON report",
            data=json.dumps(history, indent=2),
            file_name="cybershield_report.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "Download CSV report",
            data=df.to_csv(index=False),
            file_name="cybershield_report.csv",
            mime="text/csv",
            use_container_width=True,
        )
else:
    st.info(
        "Enter a public IP address above to start a demo investigation."
    )

st.divider()
st.caption(
    "CyberShield is an educational defensive-security project. "
    "Demo scores are synthetic and must not be used for security decisions."
)
