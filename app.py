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
      stmt = stock.income_stmt.T
      stmt.columns = [str(col).split(" ")[0] for col in stmt.columns]

      df = stmt[["Total", "Gross", "Operating", "Net"]].dropna()
      df = df / 1e9
      df = df.round(2)

      df["Gross Margin %"] = (df["Gross"] / df["Total"] * 100).round(2)
      df["Operating Margin %"] = (df["Operating"] / df["Total"] * 100).round(2)
      df["Net Margin %"] = (df["Net"] / df["Total"] * 100).round(2)
      df["Health Rating"] = df.apply(rate_financial_health, axis=1)

      st.subheader(f"{ticker} Financial Analysis")
      st.dataframe(df[["Total", "Net", "Gross Margin %", "Operating Margin %", "Net Margin %", "Health Rating"]])

      st.subheader("Margin Trends")
      st.line_chart(df[["Gross Margin %", "Operating Margin %", "Net Margin %"]])

      st.subheader("Health Rating")
      for idx, row in df.iterrows():
          st.write(f"{idx}: {row['Health Rating']}")
  except Exception as e:
      st.error("Could not fetch data. Please check the ticker and try again.")
  
