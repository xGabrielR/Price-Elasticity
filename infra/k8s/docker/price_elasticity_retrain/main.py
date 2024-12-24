import os
import boto3
import mlflow
import awswrangler
import numpy as np
import pandas as pd
import statsmodels.api as sm

from datetime import datetime, timedelta
from matplotlib import pyplot as plt


def read_data(
    date: str,
    product_id: str | bool = None
) -> pd.DataFrame:
    product_id = f" AND i.product_id = '{product_id}' " if product_id else ""

    query = f"""
    WITH filter_months AS ( 
    SELECT 
            i.product_id, 
            date(p.order_purchase_timestamp) AS dtPedido,
            MAX(i.price) AS vlPreco,
            COUNT(*) AS demanda
        FROM oltp_prod_order_item i 
        LEFT JOIN oltp_prod_order p ON i.order_id = p.order_id
        WHERE p.order_purchase_timestamp <= DATE('{date}')  {product_id}
        GROUP BY i.product_id, date(p.order_purchase_timestamp)
    ),
    filter_products AS (
        SELECT 
            product_id,
            COUNT(*) AS qtd
        FROM filter_months
        GROUP BY 1
        HAVING count(*) >= 50
    )
    SELECT 
        f.product_id,
        f.dtPedido,
        f.vlPreco,
        f.demanda
    FROM filter_months f
    ORDER BY 1, 2
    """

    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1"
    )

    return awswrangler.athena.read_sql_query(
        query,
        database="ols_lh_trusted",
        boto3_session=session
    )

def fit_ols(
    demand: pd.Series,
    price: pd.Series,
    extra_plots: bool = True,
    print_summary: bool = True,
    return_demand_price_fig: bool = False
):
    
    # Fit OLS Model
    x_price = sm.add_constant(price)
    lr = sm.OLS(demand, x_price).fit()

    if print_summary:
        print(lr.summary())

    # Generate Extra Figures
    if extra_plots:
        fig, ax = plt.subplots(1, 2, figsize=(15, 4))
        ax = ax.flatten()

        ax[0].set_title("Price & Demand Histogram")
        ax[0].hist(price, bins=10, histtype="step", label="price")
        ax[0].hist(demand, bins=10, histtype="step", label="demand")

        ax[1].set_title("Price x Demand")
        ax[1].scatter(x=demand, y=price)
        ax[1].set_xlabel("demand")
        ax[1].set_ylabel("price")

        for axi in ax:
            axi.legend()
            axi.grid(2)

        fig = plt.figure(figsize=(10,5))
        sm.graphics.plot_regress_exog(lr, "vlPreco", fig=fig)
        fig.tight_layout(pad=1.0);

        min_max_price = np.array([min(price), max(price)])
        predictions = np.exp(lr.predict(sm.add_constant(min_max_price)))
        min_max_price = np.exp(min_max_price)

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.scatter(np.exp(price), np.exp(demand))
        ax.plot(min_max_price, predictions, "k--")
        ax.set_xlabel("Price")
        ax.set_ylabel("Demand");
        ax.set_title(datetime.now())
        ax.grid(2)

        return lr, fig
    
    if return_demand_price_fig:
        min_max_price = np.array([min(price), max(price)])
        predictions = np.exp(lr.predict(sm.add_constant(min_max_price)))
        min_max_price = np.exp(min_max_price)

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.scatter(np.exp(price), np.exp(demand))
        ax.plot(min_max_price, predictions, "k--")
        ax.set_xlabel("Price")
        ax.set_ylabel("Demand");
        ax.set_title(datetime.now())
        ax.grid(2)

        return lr, fig

    else:
        return lr
    

if __name__ == "__main__":
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_SERVER"))
    experiment_name = "OlistPriceElasticity"

    try:
        experiment_id = mlflow.get_experiment_by_name(name=experiment_name).experiment_id
    except:
        experiment_id = mlflow.create_experiment(name=experiment_name)

    print(f"Experiment Id: {experiment_id}")

    products = [
        "8c591ab0ca519558779df02023177f44",
        "165f86fe8b799a708a20ee4ba125c289",
        "461f43be3bdf8844e65b62d9ac2c7a5a"
    ]

    train_date = os.getenv("TRAIN_DATE")

    for product_id in products:
        print(f"Product: {product_id}, Train Date: {train_date}")
        df = read_data(date=train_date, product_id=product_id)

        with mlflow.start_run(
            experiment_id=experiment_id,
            run_name=f"ols-{train_date}-{product_id}"
        ) as active_run:
            
            # Fit Model
            lr, fig = fit_ols(
                np.log1p(df["demanda"]),
                np.log1p(df["vlpreco"]),
                print_summary=False,
                extra_plots=False,
                return_demand_price_fig=True
            );
            
            mlflow.log_params({
                "train_date": train_date,
                "product_id": product_id
            })
            
            mlflow.log_metrics(lr.params.to_dict())
            mlflow.log_figure(fig, "figs/demand_x_price.png")
            mlflow.sklearn.log_model(
                lr,
                "models/ols",
            );
