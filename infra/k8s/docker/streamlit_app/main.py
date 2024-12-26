import os
import mlflow
import numpy as np
import pandas as pd
import streamlit as st
import plotly_express as px 
import plotly.graph_objects as go


def header() -> None:
    st.header("Olist Price Elasticity")
    st.write("---")

def sidebar_header(
    experiment_id: str
) -> None:
    st.sidebar.header("Filters")
    st.sidebar.text(f"Experiment Id: {experiment_id}")
    st.sidebar.write("---")

def sidebar_filters(
    df_runs: pd.DataFrame
) -> list:
    filter_products = st.sidebar.multiselect(
        "Available Products",
        df_runs["product_id"].unique(),
        default=df_runs["product_id"].unique()[0]
    )

    filter_date = st.sidebar.multiselect(
        "Train Dates",
        df_runs["train_date"].unique(),
        default=df_runs["train_date"].unique()[0]
    )
    
    if filter_products == [] or filter_date == []:
        raise TypeError("PLEASE, SELECT FILTERS!")

    return filter_date, filter_products

def get_mlflow_experiment(
    mlflow: mlflow,
    experiment_name: str
) -> str:
    try:
        return mlflow.get_experiment_by_name(name=experiment_name).experiment_id
    except:
        return mlflow.create_experiment(name=experiment_name)

def get_mlflow_runs(
    mlflow: mlflow,
    experiment_id: str
) -> pd.DataFrame:
    df_runs = mlflow.search_runs(experiment_ids=[experiment_id])
    df_runs = df_runs[["run_id", "params.train_date", "params.product_id", "metrics.vlpreco", "metrics.const"]]
    df_runs.columns = ["run_id", "train_date", "product_id", "log_elasticity", "b"]

    return df_runs

def plot_weekly_price_elasticity(
    df_runs_pivot: pd.DataFrame,
    yaxis_title: str = "Price Elasticity"
):
    fig = px.line(
        df_runs_pivot,
        title="Price Elasticity by Product",
        markers=True
    )

    fig.update_layout(
        xaxis=dict(tickformat="%Y-%m-%d"),
        xaxis_title="Train Date",
        yaxis_title=yaxis_title,
        height=500
        #yaxis_range=[-0.5, 5]
    )

    return fig

def tab_weekly_price_elasticity(
    df_filter_runs: pd.DataFrame
) -> None:
    st.html("<br>")
    df_runs_pivot = df_filter_runs.pivot(
        index="train_date",
        columns="product_id",
        values="log_elasticity"
    )

    st.write("Weekly Log Elasticity by Product")
    st.dataframe(df_runs_pivot)

    st.plotly_chart(plot_weekly_price_elasticity(df_runs_pivot, "Demand"), use_container_width=True)

    query_params = st.experimental_get_query_params()
    scroll_position = query_params.get("scroll", ["0"])[0]
    st.experimental_set_query_params(scroll=scroll_position)

def tab_simulate_demand(
    df_filter_runs: pd.DataFrame
) -> None:
    st.html("<br>")

    input_price = st.slider(
        label="Provided Product Price",
        min_value=10,
        max_value=500
    )

    df_filter_runs["demand"] = np.expm1(df_filter_runs["log_elasticity"] * np.log(input_price) + df_filter_runs["b"])

    df_runs_pivot = df_filter_runs.pivot(
        index="train_date",
        columns="product_id",
        values="demand"
    )

    st.plotly_chart(plot_weekly_price_elasticity(df_runs_pivot))

if __name__ == "__main__":
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_SERVER"))
    st.set_page_config(
        layout="wide",
        page_title="Olist - Price Elasticity",
        page_icon=":fire:"
    )

    experiment_id = get_mlflow_experiment(
        mlflow=mlflow,
        experiment_name="OlistPriceElasticity"
    )

    df_runs = get_mlflow_runs(
        mlflow=mlflow,
        experiment_id=experiment_id
    )

    header()
    sidebar_header(experiment_id=experiment_id)
    filter_date, filter_products = sidebar_filters(df_runs=df_runs)
    df_filter_runs = df_runs[
        (df_runs["product_id"].isin(filter_products)) &
        (df_runs["train_date"].isin(filter_date))
    ]
    
    tab_weekly, tab_sim_demand = st.tabs(
        ["Weekly Price Elasticity", "Simulate Demand"]
    )

    with tab_weekly:
        tab_weekly_price_elasticity(df_filter_runs)

    with tab_sim_demand:
        tab_simulate_demand(df_filter_runs)

