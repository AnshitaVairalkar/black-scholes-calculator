import math
import numpy as np
from scipy.stats import norm

def get_user_input():
    # Retrieves user input for parameters and ensures they are valid numbers and non-negative for S and T.
    while True:
        try:
            S = float(input("Enter the current stock price (Spot Price): "))
            if S < 0:
                print("Invalid input: Spot Price cannot be negative. Please re-enter.")
                continue

            X = float(input("Enter the strike price (Strike Price): "))
            if X < 0:
                print("Invalid input: Strike Price cannot be negative. Please re-enter.")
                continue

            T = float(input("Enter the time to maturity (in years, Time to Maturity): "))
            if T < 0:
                print("Invalid input: Time to Maturity cannot be negative. Please re-enter.")
                continue

            sigma = float(input("Enter the volatility (Volatility, as a decimal): "))
            if sigma < 0:
                print("Invalid input: Volatility cannot be negative. Please re-enter.")
                continue

            r = float(input("Enter the risk-free interest rate (Interest Rate, as a decimal): "))
            if r < 0:
                print("Invalid input: Risk-free interest rate cannot be negative. Please re-enter.")
                continue

            return S, X, T, sigma, r
        except ValueError:
            print("Invalid input, please enter numbers.")

def black_scholes_call_put(S, X, T, sigma, r):
    # Calculates the Black-Scholes model prices for European call and put options.
    d1 = (math.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    call_price = S * norm.cdf(d1) - X * math.exp(-r * T) * norm.cdf(d2)
    put_price = X * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return call_price, put_price

inputs = get_user_input()
call_price, put_price = black_scholes_call_put(*inputs)

print()
print(f"Call Option Price: {call_price:.2f}")
print(f"Put Option Price: {put_price:.2f}")


def option_greeks_approx(S, X, T, r, sigma):
    base_call_price, base_put_price = black_scholes_call_put(S, X, T, sigma, r) # Calculate the base call and put prices

    dS = S * 0.01  # 1% of stock price
    dT = 1/365  # One day change for Theta
    dr = 0.0001  # 0.01% change for interest rate
    dsigma = 0.01  # 1% change for volatility

    # Delta Approximation
    call_delta = (black_scholes_call_put(S + dS, X, T, sigma, r)[0] - base_call_price) / dS
    put_delta = (black_scholes_call_put(S + dS, X, T, sigma, r)[1] - base_put_price) / dS

    # Gamma Approximation (requires a second order approximation)
    call_gamma = (black_scholes_call_put(S + dS, X, T, sigma, r)[0] - 2 * base_call_price + black_scholes_call_put(S - dS, X, T, sigma, r)[0]) / (dS ** 2)
    put_gamma = (black_scholes_call_put(S + dS, X, T, sigma, r)[1] - 2 * base_put_price + black_scholes_call_put(S - dS, X, T, sigma, r)[1]) / (dS ** 2)

    # Theta Approximation
    call_theta = (black_scholes_call_put(S, X, T - dT, sigma, r)[0] - base_call_price) / dT
    put_theta = (black_scholes_call_put(S, X, T - dT, sigma, r)[1] - base_put_price) / dT

    # Vega Approximation
    call_vega = (black_scholes_call_put(S, X, T, sigma + dsigma, r)[0] - base_call_price) / dsigma
    put_vega = (black_scholes_call_put(S, X, T, sigma + dsigma, r)[1] - base_put_price) / dsigma

    # Rho Approximation
    call_rho = (black_scholes_call_put(S, X, T, sigma, r + dr)[0] - base_call_price) / dr
    put_rho = (black_scholes_call_put(S, X, T, sigma, r + dr)[1] - base_put_price) / dr

    return {
        "call_delta": call_delta, "call_gamma": call_gamma, "call_theta": call_theta,
        "call_vega": call_vega, "call_rho": call_rho,
        "put_delta": put_delta, "put_gamma": put_gamma, "put_theta": put_theta,
        "put_vega": put_vega, "put_rho": put_rho
    }


greeks_approx = option_greeks_approx(*inputs)

# Printing Option Greeks
print("Option Greeks: For Call Option")
print(f"Call Delta: {greeks_approx['call_delta']:.4f}")
print(f"Call Gamma: {greeks_approx['call_gamma']:.4f}")
print(f"Call Theta: {greeks_approx['call_theta']:.4f}")
print(f"Call Vega: {greeks_approx['call_vega']:.4f}")
print(f"Call Rho: {greeks_approx['call_rho']:.4f}")

print()

print("Option Greeks: For Put Option")
print(f"Put Delta: {greeks_approx['put_delta']:.4f}")
print(f"Put Gamma: {greeks_approx['put_gamma']:.4f}")
print(f"Put Theta: {greeks_approx['put_theta']:.4f}")
print(f"Put Vega: {greeks_approx['put_vega']:.4f}")
print(f"Put Rho: {greeks_approx['put_rho']:.4f}")