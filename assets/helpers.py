import pandas as pd
import numpy as np
from datetime import datetime

def generate_ohlc_data():
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    open_p = np.random.normal(1200, 50, 30)
    close_p = open_p + np.random.normal(0, 30, 30)
    high_p = np.maximum(open_p, close_p) + np.random.uniform(5, 20, 30)
    low_p = np.minimum(open_p, close_p) - np.random.uniform(5, 20, 30)
    return pd.DataFrame({'Date': dates, 'Open': open_p, 'High': high_p, 'Low': low_p, 'Close': close_p})

def generate_bess_revenue(ep_ratio=4.0, deg_cost=150):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    arb_weight = 0.8 if ep_ratio >= 3.0 else 0.3
    anc_weight = 1.0 - arb_weight
    base_val = 100000
    arb = [base_val * arb_weight * np.random.uniform(0.9, 1.1) for _ in range(6)]
    ancillary = [base_val * anc_weight * np.random.uniform(0.9, 1.1) for _ in range(6)]
    capacity = [20000] * 6
    return pd.DataFrame({'Month': months, 'Arbitrage': arb, 'Ancillary': ancillary, 'Capacity': capacity})

def generate_clipping_data(capacity, grid_limit):
    hours = np.arange(0, 24, 0.5)
    generation = capacity * np.exp(-((hours - 12)**2) / 8) 
    generation = np.maximum(generation - 0.5, 0)
    delivered = np.minimum(generation, grid_limit)
    curtailed = np.maximum(generation - grid_limit, 0)
    return pd.DataFrame({'Hour': hours, 'Potential Generation': generation, 'Grid Limit': [grid_limit] * len(hours), 'Delivered Energy': delivered, 'Curtailed Energy': curtailed})

# New Carbon Helper (v7.5)
def calculate_liability_forecast(client_annual_mwh, ppa_mwh_avoided, ge_factor_start, tax_rate_start, escalation_rate, term_years):
    ge_factor = ge_factor_start
    tax_rate = tax_rate_start
    tax_free_allowance = 0.60 
    forecast_data = []
    
    for year in range(1, term_years + 1):
        gross_emissions = client_annual_mwh * ge_factor / 1000 
        avoided_emissions = ppa_mwh_avoided * ge_factor / 1000
        allowance_reduction = gross_emissions * tax_free_allowance
        taxable_emissions = max(0, gross_emissions - allowance_reduction - avoided_emissions)
        annual_liability = taxable_emissions * tax_rate
        
        forecast_data.append({
            'Year': year,
            'GEF': ge_factor,
            'TaxRate': tax_rate,
            'GrossEmissions': gross_emissions,
            'AvoidedEmissions': avoided_emissions,
            'NetTaxableEmissions': taxable_emissions,
            'AnnualLiability': annual_liability
        })
        ge_factor *= 1.01
        tax_rate *= (1 + escalation_rate / 100)
    return pd.DataFrame(forecast_data)

def mock_get_market_data(): return "R 1,267"
def mock_get_grid_risk(): return "STAGE 4" 
def mock_get_vix(): return "24.5"

# --- NEW: v8.1 Next-Gen Shield Helpers ---

def simulate_covenant_breach(current_ratio, threshold, volatility, simulations=1000):
    """
    Simulates the probability of Net Debt/EBITDA breaching a threshold.
    Returns: Probability (%), Distribution Array
    """
    np.random.seed(42)
    # Simulate end-of-year ratio based on volatility
    simulated_ratios = np.random.normal(current_ratio, volatility, simulations)
    breaches = simulated_ratios[simulated_ratios > threshold]
    prob_breach = len(breaches) / simulations
    return prob_breach * 100, simulated_ratios

def calculate_black_scholes_put(S, K, T, r, sigma):
    """
    Simplified Black-Scholes for Merchant Tail Floor Option.
    S: Spot Price, K: Strike, T: Time, r: Risk-free rate, sigma: Volatility
    """
    from scipy.stats import norm
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = (K * np.exp(-r * T) * norm.cdf(-d2)) - (S * norm.cdf(-d1))
    return max(0.0, put_price)

def generate_merchant_tail_scenario(strike, volatility, term_years):
    """Generates a volatile spot price curve vs a flat floor."""
    months = np.arange(1, (term_years * 12) + 1)
    base_price = 0.85 # R/kWh
    # Random walk
    spot_curve = [base_price]
    for _ in range(len(months)-1):
        change = np.random.normal(0, volatility/10)
        spot_curve.append(max(0.2, spot_curve[-1] * (1 + change)))
    
    floor_curve = [strike] * len(months)
    return pd.DataFrame({'Month': months, 'Spot Price': spot_curve, 'Floor Price': floor_curve})
