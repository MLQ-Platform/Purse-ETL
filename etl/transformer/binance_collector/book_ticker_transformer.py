import pandas as pd


class BinanceBookTickerColumnMap:
    COLMAP = {
        0: "update_id",
        1: "best_bid_price",
        2: "best_bid_qty",
        3: "best_ask_price",
        4: "best_ask_qty",
        5: "transaction_time",
        6: "event_time",
    }

    TYPEMAP = {
        COLMAP[0]: int,
        COLMAP[1]: float,
        COLMAP[2]: float,
        COLMAP[3]: float,
        COLMAP[4]: float,
        COLMAP[5]: int,
        COLMAP[6]: int,
    }


class BinanceBookTickerTransformer:
    def transform(self, book_ticker: pd.DataFrame) -> pd.DataFrame:
        """
        Transform Book Ticker data to ohlcv dataframe
        """
        book_ticker = self._rename(book_ticker)
        book_ticker = self._casting(book_ticker)
        book_ticker = self._unix2datetime(book_ticker)
        return book_ticker

    def _rename(self, book_ticker: pd.DataFrame) -> pd.DataFrame:
        """
        book_ticker dataframe to ohlcv dataframe
        """
        col_map = BinanceBookTickerColumnMap.COLMAP

        book_ticker = book_ticker.rename(col_map, axis=1)
        return book_ticker

    def _unix2datetime(self, book_ticker: pd.DataFrame) -> pd.DataFrame:
        """
        book_ticker dataframe index preprocessing
        """
        colmap = BinanceBookTickerColumnMap.COLMAP

        book_ticker[colmap[5]] = pd.to_datetime(book_ticker[colmap[5]], unit="ms")
        book_ticker[colmap[6]] = pd.to_datetime(book_ticker[colmap[6]], unit="ms")
        return book_ticker

    def _casting(self, book_ticker: pd.DataFrame) -> pd.DataFrame:
        """
        book_ticker dataframe type casting
        """
        book_ticker = book_ticker.astype(BinanceBookTickerColumnMap.TYPEMAP)
        return book_ticker
