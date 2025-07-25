def simulate_guar_behavior(grade, chemical, conc, temp, ph, time, rpm):
    import numpy as np

    time_points = list(range(0, time+1, 5))
    base = 1000

    modifier = 1.0
    if grade == "Fast Hydrating":
        modifier *= 1.5
    elif grade == "Industrial":
        modifier *= 0.8

    chem_factor = {
        "Water": 1.0,
        "Acid": 0.7,
        "Salt": 0.9,
        "Borax": 1.3,
        "CaCl₂": 0.6
    }[chemical]

    temp_effect = (temp / 25) ** 0.5
    ph_effect = 1.0 if 6 <= ph <= 8 else 0.7
    rpm_effect = (rpm / 300) ** 0.3

    viscosity_curve = [round(base * modifier * chem_factor * temp_effect * ph_effect * rpm_effect * (1 - np.exp(-0.1*t)), 2) for t in time_points]

    return {'time': time_points, 'viscosity': viscosity_curve}
