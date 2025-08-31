# modules/visualizations.py
import plotly.express as px

def plot_portfolio_trend(df):
    """
    Line chart of portfolio value over time.
    """
    fig = px.line(df, x='Date', y='Portfolio Value', title='Portfolio Value Over Time')
    fig.update_layout(template="plotly_dark")
    return fig

def plot_allocation_pie(df):
    """
    Pie chart showing allocation of portfolio by stock.
    """
    fig = px.pie(df, names='Stock', values='Current Value', title='Portfolio Allocation')
    fig.update_traces(textinfo='percent+label')
    return fig

def plot_gains_bar(df):
    """
    Bar chart showing gain/loss per stock with color coding.
    """
    df['Color'] = df['Gain/Loss'].apply(lambda x: 'green' if x >= 0 else 'red')
    fig = px.bar(df, x='Stock', y='Gain/Loss', color='Color', title='Gain/Loss per Stock', text='Gain/Loss')
    fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside', showlegend=False)
    return fig
