def run_simulation(powder_weight, powder_mesh, moisture, rpm, mixer_size,
                     water_qty, split_daal_qty, chemicals, method, viscometer):

    chemical_effect = sum(c["weight"] for c in chemicals)
    mesh_factor = {"80": 0.9, "100": 1.0, "200": 1.1}[powder_mesh]
    mixer_factor = {"Small": 0.8, "Medium": 1.0, "Large": 1.2}[mixer_size]

    viscosity = viscometer * (1 + 0.01 * chemical_effect) * mesh_factor * mixer_factor
    time_to_react = (powder_weight + water_qty + sum(c["weight"] for c in chemicals)/1000) / (rpm + 1)

    result = {
        "Adjusted Viscosity (cP)": round(viscosity, 2),
        "Estimated Reaction Time (min)": round(time_to_react, 2),
        "Powder Weight (kg)": powder_weight,
        "Mesh Size": powder_mesh,
        "Moisture (%)": moisture,
        "Water (L)": water_qty,
        "Split Daal (kg)": split_daal_qty,
        "Chemicals Used": chemicals,
        "Viscometer Method": method
    }
    return result
