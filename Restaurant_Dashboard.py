import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Restaurant Dashboard",
    page_icon="🥡",
    layout="wide"
)

# Title of the Dashboard
st.title("Restaurant Dashboard")

st.header("The Problem")
st.markdown("In today's competitive market, where restaurants often open and close swiftly, understanding ideal locations and success strategies is crucial for owners. Our project provides valuable insights from data spanning 14 states, using visualizations and predictive models to help potential restaurant owners understand specific location demographics and estimate business success.")

st.subheader("Objective")
st.markdown("**How can we help business owners understand the demographics of the location and estimate the success of the business?**")

# Importing cleaned data
df = pd.read_csv("data/clean_data.csv")
st.subheader("Data Demonstration")
st.dataframe(df)
