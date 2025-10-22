import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd

# --- Configuration ---
MEMBERS = ["Shaheer", "MSN", "Ali"]
OPTIONS = {
    "Fajr with Jamaat (+5)": 5,
    "Fajr prayed alone (+2)": 2,
    "Fajr Qaza (-1)": -1
}
DATA_FILE = "fajr_data.json"
DAYS_LIMIT = 30

# --- Helper Functions ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
        if (datetime.now() - start_date).days >= DAYS_LIMIT:
            return reset_data()
        return data
    return reset_data()

def reset_data():
    data = {
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "scores": {m: 0 for m in MEMBERS},
        "records": []
    }
    save_data(data)
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def records_to_df(records):
    if not records:
        return pd.DataFrame(columns=["date"] + MEMBERS)
    rows = []
    for r in records:
        row = {"date": r["date"]}
        for m in MEMBERS:
            # store points not label to show chart
            # find points from OPTIONS by label
            label = r.get(m, "")
            points = next((v for k,v in OPTIONS.items() if k==label), 0)
            row[m] = points
        rows.append(row)
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df

# --- App UI ---
st.set_page_config(page_title="Fajr Tracker", page_icon="🌅", layout="centered")
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg,#f7fbf9,#ffffff); }
    .big-title {font-size:32px; font-weight:700; color:#0b4d2b;}
    .muted {color: #6b7280; font-size:14px;}
    .card {background: white; padding: 18px; border-radius:12px; box-shadow: 0 6px 18px rgba(15,23,42,0.06);}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="big-title">🌙 Family Fajr Prayer Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="muted">Track daily Fajr for Shaheer, MSN, and Ali — auto-reset every 30 days.</div>')
st.write("")

data = load_data()
start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
day_number = (datetime.now() - start_date).days + 1

st.markdown(f"**📅 Day {day_number} / {DAYS_LIMIT}** (Auto-reset after 30 days)")
st.write("")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("🕋 Record Today's Fajr")
    today = datetime.now().strftime("%Y-%m-%d")
    daily_record = {"date": today}

    with st.form("fajr_form"):
        cols = st.columns(len(MEMBERS))
        for i, member in enumerate(MEMBERS):
            with cols[i]:
                choice = st.selectbox(member, list(OPTIONS.keys()), key=member)
                daily_record[member] = choice
        submitted = st.form_submit_button("💾 Save Today's Record")

    if submitted:
        # add points and save
        for member in MEMBERS:
            choice = daily_record[member]
            data["scores"][member] += OPTIONS.get(choice, 0)
            # store the label for history
        data["records"].append(daily_record)
        save_data(data)
        st.success("✅ Today's record saved successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
st.markdown('<div class="card">', unsafe_allow_html=True)
st.header("📊 Current Points")
cols = st.columns(len(MEMBERS))
for i, member in enumerate(MEMBERS):
    with cols[i]:
        st.metric(label=member, value=f"{data['scores'][member]} pts")

st.write("")
# Chart of cumulative points over time
st.subheader("📈 Progress (last 30 entries)")
df = records_to_df(data["records"])
if not df.empty:
    # cumulative sum per member
    df_sorted = df.sort_values("date")
    cum = df_sorted.set_index("date").cumsum()
    st.line_chart(cum)
else:
    st.info("No records yet — submit today's record to see progress.")

st.markdown('</div>', unsafe_allow_html=True)

st.write("")
with st.expander("📅 View Past Records (most recent first)"):
    if data["records"]:
        for record in reversed(data["records"][-30:]):
            st.markdown(f"**{record['date']}**")
            for m in MEMBERS:
                st.write(f"• {m}: {record.get(m, '—')}")
            st.write("---")
    else:
        st.info("No past records yet.")

st.write("")
st.markdown('<div style="text-align:center; color:gray; font-size:0.9em;">Made with ❤️ for your family</div>', unsafe_allow_html=True)

st.sidebar.header("Controls")
if st.sidebar.button("🔄 Reset Data (start new 30-day cycle)"):
    reset_data()
    st.sidebar.success("Data reset — new cycle started.")

st.sidebar.write("")
st.sidebar.write("Start date: ", data['start_date'])
st.sidebar.write("Records saved: ", len(data['records']))
