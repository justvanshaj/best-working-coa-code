import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from modules.simulation import simulate_guar_behavior

st.set_page_config(page_title="Guar Gum Simulator", layout="wide")
st.title("Guar Gum + Chemical Reaction Simulator")

with st.sidebar:
    st.header("Input Parameters")
    grade = st.selectbox("Guar Gum Grade", ["Fast Hydrating", "Food Grade", "Industrial"])
    chemical = st.selectbox("Mixing Chemical", ["Water", "Acid", "Salt", "Borax", "CaCl₂"])
    concentration = st.slider("Guar Concentration (% w/w)", 0.1, 10.0, 2.0)
    temperature = st.slider("Temperature (°C)", 20, 100, 30)
    ph = st.slider("pH Level", 1.0, 14.0, 7.0)
    mix_time = st.slider("Mixing Time (minutes)", 1, 120, 10)
    rpm = st.slider("Stirring Speed (RPM)", 0, 2000, 250)

if st.button("Simulate Reaction"):
    result = simulate_guar_behavior(grade, chemical, concentration, temperature, ph, mix_time, rpm)

    st.subheader("Predicted Viscosity Curve")
    fig, ax = plt.subplots()
    ax.plot(result['time'], result['viscosity'], marker='o', color='blue')
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Viscosity (cps)")
    ax.set_title("Viscosity vs Time")
    st.pyplot(fig)

    st.subheader("Simulation Output Data")
    st.dataframe(pd.DataFrame(result))
