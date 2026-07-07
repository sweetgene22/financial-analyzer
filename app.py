import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Financial Statement Analyzer")
st.write("Analyze any public company's financial health instantly")

ticker_input = st.text_input("Enter a stock ticker (e.g. AAPL, MSFT, GOOGL)")

def rate_financial_health(row):
  score = 0
  if row["Gross Margin %"] > 40: score += 3
  elif row["Gross Margin %"] > 20: score += 1
  if row["Operating Margin %"] > 20: score +=3
  elif row["Operating Margin %"] > 10: score +=1
  if row["Net Margin %"] > 15: score += 3
  elif row["Net Margin %"] > 5: score += 1
  if score >= 7: return "Excellent"
  elif score >= 4: return "Good"
  else: return "Poor"

if ticker_input:
  try:
      ticker = ticker_input.strip().upper()
      stock = yf.Ticker(ticker)
      stmt = stock.income_stmt
      
      revenue = stmt.loc["Total Revenue"].iloc[0]
      gross_profit = stmt.loc["Gross Profit"].iloc[0]
      operating_income = stmt.loc["Operating Income"].iloc[0]
      net_income = stmt.loc["Net Income"].iloc[0]

      gross_margin = round(gross_profit / revenue * 100, 2)
      operating_margin = round(operating_income / revenue * 100, 2)
      net_margin = round(net_income / revenue * 100, 2)
      rating = rate_financial_health(gross_margin, operating_margin, net_margin)

      st.subheader(f"{ticker} Financial Analysis")
      st.write(f"Total Revenue: ${round(revenue/1e9, 2)}B")
      st.write(f"Gross Margin: {gross_margin}%")
      st.write(f"Operating Margin: {operating_margin}%")
      st.write(f"Net Margin: {net_margin}%")
      st.write(f"Health Rating: {rating}
  except Exception as e:
      st.error(f"Error: {e}")
  
