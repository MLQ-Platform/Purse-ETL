import io
import zipfile
import requests
import pandas as pd

from typing import List
from typing import Optional

from etl.logger import setup_logger
from etl.extractor import BaseExtractor

# Logger 설정
logger = setup_logger(
    loggger_name="BinanceKlinesCollector",
    file_name="extractor@binance_collector.log",
)


class BaseBinanceKlinesCollection(BaseExtractor):
    BASE_URL = "https://data.binance.vision/data"

    def __init__(self, market_type: str, ticker: str, timeframe: str):
        """
        Binance Data Collection Klines Loader

        Args:
            market_type (str)
            ticker (str)
            timeframe (str)
        """

        self._ticker = ticker
        self._market_type = market_type
        self._timeframe = timeframe

    @property
    def market_type(self):
        return self._market_type

    @property
    def ticker(self):
        return self._ticker.upper()

    @property
    def timeframe(self):
        return self._timeframe

    def load(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Data Loading Method

        Args:
            start_date (str)
            end_date (str)
        """

        final_data = []

        # 날짜 범위 생성
        date_range = self._generate_date_range(start_date, end_date)

        for date in date_range:
            df = self._fetch_klines(date)

            if df is not None:
                final_data.append(df)

        if final_data:
            combined_data = pd.concat(final_data)
            logger.info(f"Loaded data with shape: {combined_data.shape}")
            return combined_data

        else:
            logger.warning("No data was loaded.")
            return pd.DataFrame()

    def _fetch_klines(self, date: str) -> Optional[pd.DataFrame]:
        """
        Specific Data of Date Loader

        Args:
            date (str)
        """

        url = (
            f"{self.BASE_URL}/{self.market_type}/daily/klines/"
            f"{self.ticker}/{self.timeframe}/"
            f"{self.ticker}-{self.timeframe}-{date}.zip"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            z = zipfile.ZipFile(io.BytesIO(response.content))
            file_list = z.namelist()

            logger.info(f"Files in ZIP for {date}: {file_list}")

            f = z.open(file_list[0])
            data = pd.read_csv(f, header=None)

            if pd.to_numeric(data.iloc[0], errors="coerce").isna().any():
                data.drop(0, inplace=True)

            f.close()
            z.close()

            return data

        except requests.RequestException as e:
            logger.error(f"Failed to download file for {date}: {e}")

        except zipfile.BadZipFile as e:
            logger.error(f"Failed to unzip file for {date}: {e}")

        except Exception as e:
            logger.error(f"An unexpected error occurred for {date}: {e}")

    def _generate_date_range(self, start_date: str, end_date: str) -> List[str]:
        """
        Data Range Gen

        Args:
            start_date (str): 'YYYY-MM-DD'
            end_date (str): 'YYYY-MM-DD'
        """

        start_date = pd.to_datetime(start_date).strftime("%Y-%m-%d")
        end_date = pd.to_datetime(end_date).strftime("%Y-%m-%d")

        date_range = pd.date_range(start=start_date, end=end_date, freq="D")
        return date_range.strftime("%Y-%m-%d").tolist()


class BinanceFuturesUM(BaseBinanceKlinesCollection):
    """
    USD-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(market_type="futures/um", ticker=ticker, timeframe=timeframe)


class BinanceFuturesCM(BaseBinanceKlinesCollection):
    """
    COIN-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(market_type="futures/cm", ticker=ticker, timeframe=timeframe)


class BinanceSpot(BaseBinanceKlinesCollection):
    """
    SPOT COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(market_type="spot", ticker=ticker, timeframe=timeframe)
