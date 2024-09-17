import pandas as pd

from fastapi import Query
from fastapi import APIRouter
from fastapi import HTTPException

from etl.loader import SQLDatabaseLoader
from etl.utils import load_db_config
from etl.utils import get_db_uri

from sqlalchemy import text
from datetime import datetime

router = APIRouter()

config = load_db_config()

uri = get_db_uri(config)

loader = SQLDatabaseLoader(uri)


@router.get(
    "/historical/futures",
    # response_model=OHLCVResponse,
    summary="Futures OHLCV Query API",
)
async def get_future_historical(
    ticker: str = Query(..., description="Ticker Name (e.g., BTCUSDT)"),
    start_date: str = Query(
        ..., description="Start Date of Queried Data (e.g., 2024-03-01)"
    ),
    end_date: str = Query(
        ..., description="End Date of Queried Data (e.g., 2024-03-05)"
    ),
):
    # DATE TIME FORMAT CHECK
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD format.",
        )

    # DB CONNETCTION
    try:
        loader.connect()

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="DB Connection is Failed.",
        )

    # DB QUERY EXECUTION
    try:
        query = text(f"""
            SELECT * FROM ohlcv_{ticker.lower()}
            WHERE datetime BETWEEN '{start_date}' AND '{end_date}'
            """)

        data = loader.sql_engine.execute(query)

        if not data.rowcount:
            raise HTTPException(
                status_code=404,
                detail="No data found for the given ticker and date range.",
            )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Query Execution is Failed.",
        )

    finally:
        loader.close()

    fetched_data = data.fetchall()
    fetched_data = pd.DataFrame(fetched_data)
    fetched_data = fetched_data.to_dict(orient="records")
    return fetched_data
