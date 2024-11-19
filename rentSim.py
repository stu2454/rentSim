import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title and Description
st.title("Assistive Technology Funding Simulation with Repairs, Maintenance, and Error Bars")
st.write("""
This simulation compares the 'Fund to Purchase' and 'Fund to Hire' models for assistive technology funding, 
including repair and maintenance costs. Standard error bars provide a sense of statistical variability.
""")

# Sidebar for Inputs
st.sidebar.header("Simulation Parameters")

# Funding Agency Inputs
st.sidebar.subheader("Funding Agency")
initial_budget = st.sidebar.number_input("Initial Budget ($)", value=100000)
purchase_cost = st.sidebar.number_input("Purchase Cost per Device ($)", value=5000)
maintenance_cost = st.sidebar.number_input("Annual Maintenance Cost per Device ($)", value=500)
rental_cost = st.sidebar.number_input("Monthly Rental Cost per Device ($)", value=200)

# Repairs and Maintenance Parameters
st.sidebar.subheader("Repairs and Maintenance")
repair_cost = st.sidebar.number_input("Repair Cost per Device ($)", value=300)
repair_frequency = st.sidebar.slider("Average Repairs per Year per Device", 0.0, 5.0, 1.5)
replacement_threshold = st.sidebar.slider("Replacement Threshold (% of Purchase Cost)", 0, 100, 50) / 100
funding_coverage = st.sidebar.slider("Funding Coverage for Repairs (%)", 0, 100, 80) / 100

# Variability Inputs
st.sidebar.subheader("Variability Settings")
repair_cost_variability = st.sidebar.slider("Repair Cost Variability ($)", 0.0, 500.0, 100.0)
repair_frequency_variability = st.sidebar.slider("Repair Frequency Variability", 0.0, 2.0, 0.5)
rental_cost_variability = st.sidebar.slider("Rental Cost Variability ($)", 0.0, 200.0, 50.0)
replacement_threshold_variability = st.sidebar.slider("Replacement Threshold Variability", 0.0, 0.5, 0.1)

# Participant Inputs
st.sidebar.subheader("Participants")
num_participants = st.sidebar.slider("Number of Participants", 10, 1000, 100)
upgrade_prob = st.sidebar.slider("Probability of Device Change (%)", 0, 100, 20) / 100
usage_duration = st.sidebar.slider("Average Usage Duration (Years)", 1, 10, 5)

# Simulation Parameters
num_simulations = 1000  # Number of simulations for variability

# Run Simulation Button
if st.sidebar.button("Run Simulation"):
    # Arrays to store simulated costs
    purchase_costs = []
    hire_costs = []

    for _ in range(num_simulations):
        # Add user-defined variability to parameters
        repair_freq_var = np.random.normal(repair_frequency, repair_frequency_variability)
        repair_cost_var = np.random.normal(repair_cost, repair_cost_variability)
        rental_cost_var = np.random.normal(rental_cost, rental_cost_variability)
        replacement_threshold_var = np.random.normal(replacement_threshold, replacement_threshold_variability)

        # Ensure values remain within reasonable limits
        repair_freq_var = max(repair_freq_var, 0)  # Frequency can't be negative
        repair_cost_var = max(repair_cost_var, 0)  # Cost can't be negative
        rental_cost_var = max(rental_cost_var, 0)  # Rental cost can't be negative
        replacement_threshold_var = min(max(replacement_threshold_var, 0), 1)  # Between 0 and 1

        # Calculate repair costs
        repair_funded_cost = repair_cost_var * funding_coverage
        total_repair_cost = repair_funded_cost * repair_freq_var * usage_duration * num_participants

        # Purchase Model
        purchase_total = (
            num_participants * purchase_cost +
            num_participants * maintenance_cost * usage_duration +
            total_repair_cost
        )
        if repair_cost_var > purchase_cost * replacement_threshold_var:
            purchase_total += num_participants * purchase_cost * upgrade_prob

        # Hire Model
        hire_total = (
            num_participants * rental_cost_var * 12 * usage_duration +
            total_repair_cost
        )

        # Store simulated costs
        purchase_costs.append(purchase_total)
        hire_costs.append(hire_total)

    # Calculate mean and standard error
    purchase_mean = np.mean(purchase_costs)
    hire_mean = np.mean(hire_costs)
    purchase_se = np.std(purchase_costs) / np.sqrt(num_simulations)
    hire_se = np.std(hire_costs) / np.sqrt(num_simulations)

    # Display Results
    st.subheader("Simulation Results")
    st.write(f"**Mean Total Cost (Purchase Model):** ${purchase_mean:,.2f} ± {purchase_se:,.2f}")
    st.write(f"**Mean Total Cost (Hire Model):** ${hire_mean:,.2f} ± {hire_se:,.2f}")

    # Visualisation
    fig, ax = plt.subplots()
    ax.bar(["Purchase Model", "Hire Model"], [purchase_mean, hire_mean], yerr=[purchase_se, hire_se],
           color=["blue", "green"], capsize=5, alpha=0.8)
    ax.set_ylabel("Total Cost ($)")
    ax.set_title("Cost Comparison with Error Bars")
    st.pyplot(fig)

# Footer
st.write("---")
st.write("This simulation evaluates funding strategies for assistive technology with a focus on variability.")
