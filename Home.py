import streamlit as st

st.set_page_config(
    page_title="ECON1500 Data Visualizations",
    page_icon="📊",
    layout="wide"
)

st.title("ECON1500 Data Visualization Hub")
st.markdown("---")

st.markdown("""
# Welcome to the ECON1500 Data Visualization Hub

This web application provides interactive visualizations for the ECON1500 class at Brown University:

## Available Visualizations:

### 1. Trade Proposal Word Cloud
Explore key terms and connections between topics in the North American Trade proposal using an interactive word cloud and network graph.

### 2. Project Submission Statistics
View statistics about final project submissions, including group sizes, student distribution, and project types.

## How to Use
Select a visualization from the sidebar menu to get started!

## About
These visualizations were created as part of the ECON1500 class to provide helpful insights into project submissions and topic exploration.

---
*Created with Streamlit*
""")

# Add sidebar info
st.sidebar.success("Select a visualization above.")

# Add footer with info
st.markdown("---")
st.markdown("© 2025 | ECON1500 Macroeconomic Challenges | Brown University") 