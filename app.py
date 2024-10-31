# emissions_calculator.py

import streamlit as st

def calculate_emissions(coal_burned_tons, biomass_burned_tons):
    # Define emission factors (in tons per ton of fuel burned)
    emission_factors = {
        'CO': 0.001,     # tons CO
        'CO2': 0.28,     # tons CO2
        'NO': 0.00003,   # tons NO
        'SO2': 0.0003,   # tons SO2
        'O2': 0.075      # tons O2 (approx. excess air)
    }

    # Define biomass emission factors (in tons per ton of biomass burned)
    biomass_emission_factors = {
        'CO': 0.0008,    # tons CO
        'CO2': 0.09,     # tons CO2
        'NO': 0.00002,   # tons NO
        'SO2': 0.0005,  # tons SO2
        'O2': 0.06       # tons O2 (approx. excess air)
    }

    # Convert tons to grams
    grams_per_ton = 1_000_000  # 1 ton = 1 million grams

    # Calculate emissions in grams for coal
    emissions_grams_coal = {gas: factor * coal_burned_tons * grams_per_ton for gas, factor in emission_factors.items()}
    
    # Calculate emissions in grams for biomass
    emissions_grams_biomass = {gas: factor * biomass_burned_tons * grams_per_ton for gas, factor in biomass_emission_factors.items()}

    # Total emissions in grams
    total_emissions_grams = {gas: emissions_grams_coal.get(gas, 0) + emissions_grams_biomass.get(gas, 0) for gas in emission_factors.keys()}

    # Convert grams to moles
    molar_masses = {
        'CO': 28.01,   # g/mol
        'CO2': 44.01,  # g/mol
        'NO': 30.01,   # g/mol
        'SO2': 64.07,  # g/mol
        'O2': 32.00    # g/mol
    }

    emissions_moles = {gas: total_emissions_grams[gas] / molar_masses[gas] for gas in total_emissions_grams}

    # Assume volume of flue gas produced per ton of coal and biomass burned
    volume_of_flue_gas_nmc = 2000  # Nm³ per ton of fuel burned

    # Assume standard conditions (1 atm pressure and 25°C)
    standard_pressure = 101325  # Pa
    standard_temperature = 25 + 273.15  # K
    ideal_gas_constant = 8.314  # J/(mol·K)

    # Calculate the volume of each gas at standard conditions using the ideal gas law
    gas_volumes_nmc = {gas: moles * ideal_gas_constant * standard_temperature / standard_pressure for gas, moles in emissions_moles.items()}

    # Calculate concentrations in percentage and mg/Nm³
    concentrations = {
        'CO': (gas_volumes_nmc['CO'] / (volume_of_flue_gas_nmc * (coal_burned_tons + biomass_burned_tons))) * 100,
        'CO2': (gas_volumes_nmc['CO2'] / (volume_of_flue_gas_nmc * (coal_burned_tons + biomass_burned_tons))) * 100,
        'O2': (gas_volumes_nmc['O2'] / (volume_of_flue_gas_nmc * (coal_burned_tons + biomass_burned_tons))) * 100,
        'NO': (gas_volumes_nmc['NO'] / volume_of_flue_gas_nmc) * 1_000_000,  # Convert to mg/Nm³
        'SO2': (gas_volumes_nmc['SO2'] / volume_of_flue_gas_nmc) * 1_000_000  # Convert to mg/Nm³
    }

    return concentrations

# Streamlit UI setup
st.title("Emission Calculator - NIMIR")
st.subheader("Developed by mak3.12")

st.write("Enter the amount of coal and biomass burned (in tons) to calculate emissions concentrations in NIMIR.")

# Streamlit input fields
coal_burned = st.number_input("Amount of coal burned (in tons):", min_value=0.0, step=0.1)
biomass_burned = st.number_input("Amount of biomass burned (in tons):", min_value=0.0, step=0.1)

# Calculate and display emissions if values are provided
if st.button("Calculate Emissions"):
    if coal_burned >= 0 and biomass_burned >= 0:
        emissions = calculate_emissions(coal_burned, biomass_burned)

        # Display results
        st.write(f"### Emissions from burning {coal_burned:.2f} tons of coal and {biomass_burned:.2f} tons of biomass:")
        st.write(f"**CO concentration:** {emissions['CO']:.2f}%")
        st.write(f"**CO2 concentration:** {emissions['CO2']:.2f}%")
        st.write(f"**O2 concentration:** {emissions['O2']:.2f}%")
        st.write(f"**NO concentration:** {emissions['NO']:.2f} mg/Nm³")
        st.write(f"**SO2 concentration:** {emissions['SO2']:.2f} mg/Nm³")
    else:
        st.write("Please enter non-negative values for coal and biomass burned.")
