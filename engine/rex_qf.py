import numpy as np

class REX_QF_Engine:
    def run_monte_carlo(self, sigma, iterations=10000):
        np.random.seed(42)
        mu = 0.05; S0 = 1200; T = 30/365 
        Z = np.random.normal(0, 1, iterations)
        ST = S0 * np.exp((mu - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
        strike = 3000
        payouts = np.maximum(ST - strike, 0)
        s_ael_95 = np.percentile(payouts, 95) 
        return ST, s_ael_95

    def calculate_score(self, rev_ael_ratio, tc_risk, complexity_factor):
        rev_score_norm = min(rev_ael_ratio, 2.0) * 50 
        complexity_points = complexity_factor * 100
        es_score = (0.5 * rev_score_norm) + (0.3 * tc_risk) + (0.2 * complexity_points)
        return es_score
