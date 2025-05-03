import pandas as pd
import plotly.express as px

# Country name mapping (normalized to match Plotly ISO alpha-3)
country_iso_mapping = {
    "USA": "USA",
    "France": "FRA",
    "Canada": "CAN",
    "Portugal": "PRT",
    "Luxembourg": "LUX",
    "Germany": "DEU",
    "Sweden": "SWE",
    "Netherlands": "NLD",
    "UK": "GBR",
    "Italy": "ITA",
    "Spain": "ESP",
    "Switzerland": "CHE",
    "Australia": "AUS",
    "Norway": "NOR"
}

def build_choropleth_df(summary_df):
    df = summary_df.copy()
    df["iso_alpha"] = df["country"].map(country_iso_mapping)

    # Warn if any countries were not mapped
    unmapped = df[df["iso_alpha"].isna()]
    if not unmapped.empty:
        print("⚠️ Warning: Unmapped countries found in choropleth:", unmapped["country"].unique().tolist())

    return df.dropna(subset=["iso_alpha"])


def build_choropleth_map(df):
    fig = px.choropleth(
        df,
        locations="iso_alpha",
        color="total_spent",
        hover_name="country",
        color_continuous_scale="Viridis",
        title="🌍 Travel Spending by Country",
        labels={"total_spent": "Total Spent (€)"},
        template="plotly_white"
    )
    fig.update_geos(projection_type="natural earth")
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig


def build_spending_barchart(df):
    fig = px.bar(
        df.sort_values("total_spent", ascending=False),
        x="country",
        y="total_spent",
        color="total_spent",
        color_continuous_scale="Viridis",
        labels={"total_spent": "Total Spent (€)", "country": "Country"},
        title="💳 Spending by Country",
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-30, margin={"r": 10, "t": 40, "l": 10, "b": 20})
    return fig
