import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

def get_fundamental_data(ticker):
    # Legg til .OL for norske aksjer hvis det ikke allerede er der
    if ticker.isalpha() and not ticker.endswith(".OL") and len(ticker) <= 5:
        ticker += ".OL"
    
    stock = yf.Ticker(ticker)
    info = stock.info
    
    data = {
        "Selskap": info.get("longName", "N/A"),
        "Markedsverdi": f"{info.get('marketCap', 'N/A'):,}" if info.get('marketCap') else "N/A",
        "P/E-forhold": info.get("trailingPE", "N/A"),
        "EPS (Inntjening per aksje)": info.get("trailingEps", "N/A"),
        "Gjeldsgrad (Debt-to-Equity)": info.get("debtToEquity", "N/A"),
        "ROE (Return on Equity)": info.get("returnOnEquity", "N/A"),
        "Inntektsvekst": info.get("revenueGrowth", "N/A"),
        "Utbytteavkastning": info.get("dividendYield", "N/A"),
        "Beta (Volatilitet)": info.get("beta", "N/A"),
    }
    return data, stock

def evaluate_stock(data):
    pe = data.get("P/E-forhold")
    roe = data.get("ROE (Return on Equity)")
    debt = data.get("Gjeldsgrad (Debt-to-Equity)")
    growth = data.get("Inntektsvekst")
    dividend = data.get("Utbytteavkastning")
    
    rating = "Nøytral"
    
    if pe != "N/A" and pe < 20 and roe != "N/A" and roe > 15 and debt != "N/A" and debt < 1.5:
        rating = "Sterk Kjøp"
    elif pe != "N/A" and pe > 30:
        rating = "Overpriset"
    elif growth != "N/A" and growth < 0:
        rating = "Risiko – Inntektsnedgang"
    elif dividend != "N/A" and dividend > 0.05:
        rating = "Bra utbytteaksje"
    
    return rating

def plot_stock_chart(stock):
    hist = stock.history(period="6mo")
    if hist.empty:
        st.warning("Ingen prisdata tilgjengelig for denne aksjen.")
        return
    
    fig, ax = plt.subplots()
    ax.plot(hist.index, hist["Close"], label="Lukkekurs", color="blue")
    ax.set_title("📉 Aksjekurs siste 6 måneder")
    ax.set_xlabel("Dato")
    ax.set_ylabel("Pris")
    ax.legend()
    st.pyplot(fig)

# Streamlit UI
st.set_page_config(page_title="Fundamental Analyse", layout="centered")
st.title("📈 Fundamental Analyse Bot")

ticker = st.text_input("Skriv inn aksjesymbol (f.eks. AAPL for Apple, EQNR for Equinor, VAR for Vår Energi):")

if ticker:
    try:
        data, stock = get_fundamental_data(ticker)
        rating = evaluate_stock(data)
        
        st.subheader("📊 Analyse av aksjen:")
        st.json(data)
        
        st.subheader("📈 Vurdering:")
        st.success(f"Denne aksjen vurderes som: {rating}")
        
        st.subheader("📉 Aksjekursutvikling:")
        plot_stock_chart(stock)
    except Exception as e:
        st.error(f"Noe gikk galt: {e}")

st.markdown("---")
st.caption("Laget med ❤️ av din personlige AI-assistent og Elias")

