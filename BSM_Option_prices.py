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