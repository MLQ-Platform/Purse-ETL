from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from etl.utils import get_db_uri
from etl.utils import load_db_config
from etl.loader import SQLDatabaseLoader
from etl.loader.query import upsert_query_func
from etl.loader.table import OHLCV

from etl.extractor.binance_collector import BinanceFuturesUM
from etl.extractor.binance_collector.types import TimeFrame
from etl.transformer.binance_collector import BinanceKlinesTransformer


default_args = {
    "owner": "purse",
    "depends_on_past": False,
    "start_date": datetime(2024, 9, 2),
    "email": ["eppioes@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


dag = DAG(
    "purse_etl_dag",
    default_args=default_args,
    description="Purse ETL Pipeline DAG",
    schedule="0 0 * * *",  # 매일 자정 스케쥴링
    catchup=False,
)

config = load_db_config()
db_uri = get_db_uri(config)

tickers = config["universe"]["tickers"]


def extract(ticker, **context):
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

    extractor = BinanceFuturesUM(ticker=ticker, timeframe=TimeFrame.MINUTE5)
    klines = extractor.load(start_date=start_date, end_date=end_date)
    return klines


def transform(ticker, **context):
    klines = context["task_instance"].xcom_pull(task_ids=f"extract_{ticker.lower()}")
    transformer = BinanceKlinesTransformer()
    ohlcv = transformer.transform(klines)
    return ohlcv


def load(ticker, **context):
    ohlcv = context["task_instance"].xcom_pull(task_ids=f"transform_{ticker.lower()}")

    loader = SQLDatabaseLoader(db_uri=db_uri)
    loader.connect()

    table = OHLCV(
        datetime=ohlcv.index.tolist(),
        open=ohlcv.open.tolist(),
        high=ohlcv.high.tolist(),
        low=ohlcv.low.tolist(),
        close=ohlcv.close.tolist(),
        volume=ohlcv.volume.tolist(),
    )

    query = upsert_query_func(
        table, table_name=f"ohlcv_{ticker}".lower(), unique_key="datetime"
    )
    loader.transaction(query)
    loader.close()


for ticker in tickers:
    extract_task = PythonOperator(
        task_id=f"extract_{ticker.lower()}",
        python_callable=extract,
        op_args=[ticker],
        provide_context=True,
        dag=dag,
    )

    transform_task = PythonOperator(
        task_id=f"transform_{ticker.lower()}",
        python_callable=transform,
        op_args=[ticker],
        provide_context=True,
        dag=dag,
    )

    load_task = PythonOperator(
        task_id=f"load_{ticker.lower()}",
        python_callable=load,
        op_args=[ticker],
        provide_context=True,
        dag=dag,
    )

    # Define task dependencies
    extract_task >> transform_task >> load_task
