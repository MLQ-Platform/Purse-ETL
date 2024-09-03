import pandas as pd


class BinanceKilinesColumnMap:
    COLMAP = {
        0: "datetime",
        1: "open",
        2: "high",
        3: "low",
        4: "close",
        5: "volume",
    }


class BinanceKlinesTransformer:
    def transform(self, klines: pd.DataFrame) -> pd.DataFrame:
        """
        Transform klines data to ohlcv dataframe
        """
        ohlcv = self._kilnes2ohlcv(klines)
        ohlcv = self._unix2datetime(ohlcv)
        ohlcv = self._casting(ohlcv)
        return ohlcv

    def _kilnes2ohlcv(self, klines: pd.DataFrame) -> pd.DataFrame:
        """
        klines dataframe to ohlcv dataframe
        """
        col_map = BinanceKilinesColumnMap.COLMAP

        ohlcv = klines.iloc[:, : len(col_map)]
        ohlcv = ohlcv.rename(col_map, axis=1)
        return ohlcv

    def _unix2datetime(self, ohlcv: pd.DataFrame) -> pd.DataFrame:
        """
        ohlcv dataframe index preprocessing
        """
        col_map = BinanceKilinesColumnMap.COLMAP

        ohlcv = ohlcv.set_index(col_map[0])
        ohlcv.index = pd.to_numeric(ohlcv.index)
        ohlcv.index = pd.to_datetime(ohlcv.index, unit="ms")
        return ohlcv

    def _casting(self, ohlcv: pd.DataFrame) -> pd.DataFrame:
        """
        ohlcv dataframe type casting
        """
        ohlcv = ohlcv.astype(float)
        ohlcv.index = ohlcv.index.astype(str)
        return ohlcv
