import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.fetch_data import get_summary, compute_free_cash_flow, get_company_data

st.set_page_config(page_title="Resumen Financiero", page_icon="📊", layout="wide")

st.title("📈 Resumen Financiero de la Empresa")

# Entrada del ticker
ticker = st.text_input("Ingrese el ticker de la empresa (ej: AAPL, MSFT, TSLA):", value="AAPL")

if st.button("Buscar datos"):
    try:
        with st.spinner("Descargando datos desde Yahoo Finance..."):
            data = get_company_data(ticker)
            summary = get_summary(ticker)

        st.subheader(f"📊 Información general de {summary['Nombre']}")
        st.write(f"**Sector:** {summary['Sector']}")
        st.write(f"**País:** {summary['País']}")
        st.write(f"**Moneda:** {summary['Moneda']}")

        # Mostrar tabla del flujo de caja
        cashflow = data["cashflow"]
        st.write("### 💵 Flujo de Caja (últimos años)")
        st.dataframe(cashflow)

        # Calcular FCF
        fcf = compute_free_cash_flow(cashflow)

        # Graficar FCF
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=fcf.index.strftime("%Y"),
            y=fcf.values / 1e9,
            name="Free Cash Flow",
            marker_color="green"
        ))

        fig.update_layout(
            title="Evolución del Free Cash Flow (en miles de millones)",
            xaxis_title="Año",
            yaxis_title="FCF (Billones)",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")
