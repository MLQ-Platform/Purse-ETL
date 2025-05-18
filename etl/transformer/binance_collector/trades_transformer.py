import pandas as pd


class BinanceTradesColumnMap:
    COLMAP = {
        0: "id",
        1: "price",
        2: "qty",
        3: "quote_qty",
        4: "time",
        5: "is_buyer_maker",
    }

    TYPEMAP = {
        COLMAP[0]: int,
        COLMAP[1]: float,
        COLMAP[2]: float,
        COLMAP[3]: float,
        COLMAP[4]: int,
    }


class BinanceTradesTransformer:
    def transform(self, trades: pd.DataFrame) -> pd.DataFrame:
        """
        Transform Aggregated Trades data to ohlcv dataframe
        """
        trades = self._rename(trades)
        trades = self._casting(trades)
        trades = self._casting_bool(trades)
        trades = self._unix2datetime(trades)
        return trades

    def _rename(self, trades: pd.DataFrame) -> pd.DataFrame:
        """
        trades dataframe to ohlcv dataframe
        """
        col_map = BinanceTradesColumnMap.COLMAP

        trades = trades.rename(col_map, axis=1)
        return trades

    def _unix2datetime(self, trades: pd.DataFrame) -> pd.DataFrame:
        """
        trades dataframe index preprocessing
        """
        time_col = BinanceTradesColumnMap.COLMAP[4]

        trades[time_col] = pd.to_datetime(trades[time_col], unit="ms")
        return trades

    def _casting(self, trades: pd.DataFrame) -> pd.DataFrame:
        """
        trades dataframe type casting
        """
        trades = trades.astype(BinanceTradesColumnMap.TYPEMAP)
        return trades

    def _casting_bool(self, trades: pd.DataFrame) -> pd.DataFrame:
        """
        trades dataframe bool type casting
        """
        trades[BinanceTradesColumnMap.COLMAP[5]] = trades[
            BinanceTradesColumnMap.COLMAP[5]
        ].map({"true": True, "false": False})
        return trades
