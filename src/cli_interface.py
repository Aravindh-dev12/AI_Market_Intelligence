import streamlit as st
import json

with open("insights/insights.json") as f:
    insights = json.load(f)

st.title("AI Market Intelligence Dashboard")
index = st.selectbox("Select Insight", range(len(insights)))

item = insights[index]
st.write(f"**Insight:** {item['insight']}")
st.write(f"**Confidence:** {item['confidence']}")
st.write(f"**Recommendation:** {item['recommendation']}")
