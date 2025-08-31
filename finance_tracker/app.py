# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from modules import data_fetch, calculations, visualizations
from datetime import datetime

# Load portfolio
df = pd.read_csv('data/portfolio.csv')

# Fetch live prices
df['Current Price'] = df['Stock'].apply(data_fetch.fetch_current_price)
df['Previous Close'] = df['Stock'].apply(lambda x: data_fetch.fetch_stock_data(x, period="2d")['Close'].iloc[0])

# Historical prices for volatility calculation
historical_prices = {ticker: data_fetch.fetch_stock_data(ticker) for ticker in df['Stock']}

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Professional Stock Portfolio Tracker"

# Layout
app.layout = html.Div([
    html.H1("?? Stock Portfolio Tracker", style={"textAlign": "center"}),

    html.Div([
        html.H2("Portfolio Value Trend"),
        dcc.Graph(id='portfolio_trend')
    ], style={'width':'80%', 'margin':'auto'}),

    html.Div([
        html.H2("Portfolio Allocation"),
        dcc.Graph(id='allocation_pie')
    ], style={'width':'80%', 'margin':'auto'}),

    html.Div([
        html.H2("Gains / Losses"),
        dcc.Graph(id='gains_bar')
    ], style={'width':'80%', 'margin':'auto'}),

    html.H2("Portfolio Metrics"),
    html.Div(id='metrics_table', style={'width':'60%', 'margin':'auto', 'fontSize':'18px', 'marginBottom':'30px'}),

    # Auto-update every 5 minutes
    dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0)
])

# Callback to update dashboard
@app.callback(
    [Output('portfolio_trend', 'figure'),
     Output('allocation_pie', 'figure'),
     Output('gains_bar', 'figure'),
     Output('metrics_table', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    # Fetch live prices
    df['Current Price'] = df['Stock'].apply(data_fetch.fetch_current_price)
    df['Previous Close'] = df['Stock'].apply(lambda x: data_fetch.fetch_stock_data(x, period="2d")['Close'].iloc[0])
    
    # Calculate portfolio metrics
    df_metrics = calculations.calculate_portfolio(df)
    df_metrics['Date'] = datetime.today().strftime('%Y-%m-%d')
    total_value = df_metrics['Current Value'].sum()
    total_gain = df_metrics['Gain/Loss'].sum()
    volatility = calculations.portfolio_volatility(df_metrics, historical_prices)

    # Create charts
    trend_fig = visualizations.plot_portfolio_trend(df_metrics)
    pie_fig = visualizations.plot_allocation_pie(df_metrics)
    gains_fig = visualizations.plot_gains_bar(df_metrics)

    # Metrics table
    table = html.Table([
        html.Tr([html.Th("Metric"), html.Th("Value")]),
        html.Tr([html.Td("Total Portfolio Value"), html.Td(f"${total_value:,.2f}")]),
        html.Tr([html.Td("Total Gain/Loss"), html.Td(f"${total_gain:,.2f}")]),
        html.Tr([html.Td("Portfolio Volatility (Annualized %)"), html.Td(f"{volatility*100:.2f}%")])
    ], style={'margin':'20px'})

    return trend_fig, pie_fig, gains_fig, table

# Run server
if __name__ == "__main__":
    app.run_server(debug=True)
