import streamlit as st
from modules.simulation import run_simulation

st.set_page_config(page_title="Guar Gum Simulator", layout="wide")
st.title("Guar Gum Industrial Simulator")

st.sidebar.header("Powder Preparation")
powder_weight = st.sidebar.number_input("Powder Weight (kg)", min_value=0.0, step=0.1)
powder_mesh = st.sidebar.selectbox("Powder Mesh Size", ["80", "100", "200"])
moisture_content = st.sidebar.slider("Moisture in Powder (%)", 0.0, 20.0, 10.0)

st.sidebar.header("Mixer Configuration")
mixer_rpm = st.sidebar.number_input("Mixer RPM", min_value=0)
mixer_size = st.sidebar.selectbox("Mixer Size", ["Small", "Medium", "Large"])

st.sidebar.header("Water + Split Daal Input (Pre-Powder)")
water_qty = st.sidebar.number_input("Water Quantity (L)", min_value=0.0)
split_daal_qty = st.sidebar.number_input("Split Daal Quantity (kg)", min_value=0.0)

st.sidebar.header("Chemical Inputs")
num_chemicals = st.sidebar.slider("Number of Chemicals", 1, 5, 2)
chemicals = []
for i in range(num_chemicals):
    name = st.sidebar.text_input(f"Chemical {i+1} Name", value=f"Chemical_{i+1}")
    weight = st.sidebar.number_input(f"{name} Weight (g)", min_value=0.0, key=f"weight_{i}")
    chemicals.append({"name": name, "weight": weight})

st.sidebar.header("Viscosity")
method = st.sidebar.selectbox("Viscosity Method", ["Brookfield", "Fann"])
viscometer_reading = st.sidebar.number_input("Viscometer Reading (cP)", min_value=0.0)

if st.button("Run Simulation"):
    result = run_simulation(
        powder_weight, powder_mesh, moisture_content,
        mixer_rpm, mixer_size,
        water_qty, split_daal_qty,
        chemicals, method, viscometer_reading
    )
    st.success("Simulation Complete!")
    st.json(result)
