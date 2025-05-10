import pandas as pd


class BinanceAggTradesColumnMap:
    COLMAP = {
        0: "agg_trade_id",
        1: "price",
        2: "quantity",
        3: "first_trade_id",
        4: "last_trade_id",
        5: "transact_time",
        6: "is_buyer_maker",
    }

    TYPEMAP = {
        COLMAP[0]: int,
        COLMAP[1]: float,
        COLMAP[2]: float,
        COLMAP[3]: int,
        COLMAP[4]: int,
        COLMAP[5]: int,
        COLMAP[6]: bool,
    }


class BinanceAggTradesTransformer:
    def transform(self, agg_trades: pd.DataFrame) -> pd.DataFrame:
        """
        Transform Aggregated Trades data to ohlcv dataframe
        """
        agg_trades = self._rename(agg_trades)
        agg_trades = self._casting(agg_trades)
        agg_trades = self._unix2datetime(agg_trades)
        return agg_trades

    def _rename(self, agg_trades: pd.DataFrame) -> pd.DataFrame:
        """
        agg_trades dataframe to ohlcv dataframe
        """
        col_map = BinanceAggTradesColumnMap.COLMAP

        agg_trades = agg_trades.rename(col_map, axis=1)
        return agg_trades

    def _unix2datetime(self, agg_trades: pd.DataFrame) -> pd.DataFrame:
        """
        agg_trades dataframe index preprocessing
        """
        time_col = BinanceAggTradesColumnMap.COLMAP[5]

        agg_trades[time_col] = pd.to_datetime(agg_trades[time_col], unit="ms")
        return agg_trades

    def _casting(self, agg_trades: pd.DataFrame) -> pd.DataFrame:
        """
        agg_trades dataframe type casting
        """
        agg_trades = agg_trades.astype(BinanceAggTradesColumnMap.TYPEMAP)
        return agg_trades
