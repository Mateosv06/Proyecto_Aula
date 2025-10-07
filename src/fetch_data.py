import yfinance as yf
import pandas as pd

def get_company_data(ticker_symbol):
    

    try:
        ticker = yf.Ticker(ticker_symbol)

        # Descarga de datos
        income_statement = ticker.financials
        balance_sheet = ticker.balance_sheet
        cashflow = ticker.cashflow

        # Validación básica
        if income_statement.empty or balance_sheet.empty or cashflow.empty:
            raise ValueError("No se pudieron obtener los estados financieros.")

        data = {
            "income_statement": income_statement,
            "balance_sheet": balance_sheet,
            "cashflow": cashflow,
        }

        return data

    except Exception as e:
        raise ValueError(f"Error al obtener datos para {ticker_symbol}: {e}")


def compute_free_cash_flow(df_cashflow):
    

    # Normaliza los nombres de las filas
    df_cashflow.index = df_cashflow.index.str.lower().str.strip()

    # Posibles nombres para las filas
    ocf_aliases = ["total cash from operating activities", "operating cash flow"]
    capex_aliases = [
        "capital expenditures",
        "capital expenditure",
        "purchase of fixed assets",
        "purchase of property and equipment",
        "investments in property, plant and equipment",
    ]

    # Busca las filas
    ocf_row = None
    capex_row = None

    for name in df_cashflow.index:
        if any(alias in name for alias in ocf_aliases):
            ocf_row = name
        if any(alias in name for alias in capex_aliases):
            capex_row = name

    # Validaciones
    if ocf_row is None:
        raise ValueError("No se encontró la fila de Operating Cash Flow.")
    if capex_row is None:
        raise ValueError("No se encontró la fila de Capital Expenditures o equivalente.")

    # Calcula el flujo de caja libre (FCF)
    fcf = df_cashflow.loc[ocf_row] + df_cashflow.loc[capex_row]

    return fcf


def get_summary(ticker_symbol):
    """
    Retorna un resumen general de la empresa con datos básicos y el flujo de caja libre (FCF).
    """

    data = get_company_data(ticker_symbol)
    cashflow = data["cashflow"]

    try:
        fcf = compute_free_cash_flow(cashflow)
    except Exception as e:
        fcf = f"Error al calcular FCF: {e}"

    info = yf.Ticker(ticker_symbol).info
    summary = {
        "Nombre": info.get("longName", "N/A"),
        "Sector": info.get("sector", "N/A"),
        "País": info.get("country", "N/A"),
        "Moneda": info.get("currency", "N/A"),
        "Free Cash Flow": fcf,
    }

    return summary


if __name__ == "__main__":
    ticker = "AAPL"  
    summary = get_summary(ticker)
    print(summary)
