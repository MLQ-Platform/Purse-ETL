import pandas as pd


class BinanceBookDepthColumnMap:
    COLMAP = {
        0: "timestamp",
        1: "percentage",
        2: "depth",
        3: "notional",
    }

    TYPEMAP = {
        COLMAP[1]: int,
        COLMAP[2]: float,
        COLMAP[3]: float,
    }


class BinanceBookDepthTransformer:
    def transform(self, book_depth: pd.DataFrame) -> pd.DataFrame:
        """
        Transform Book Depth data to ohlcv dataframe
        """
        book_depth = self._rename(book_depth)
        book_depth = self._casting(book_depth)
        book_depth = self._unix2datetime(book_depth)
        return book_depth

    def _rename(self, book_depth: pd.DataFrame) -> pd.DataFrame:
        """
        book_depth dataframe to ohlcv dataframe
        """
        col_map = BinanceBookDepthColumnMap.COLMAP

        book_depth = book_depth.rename(col_map, axis=1)
        return book_depth

    def _unix2datetime(self, book_depth: pd.DataFrame) -> pd.DataFrame:
        """
        book_depth dataframe index preprocessing
        """
        time_col = BinanceBookDepthColumnMap.COLMAP[0]

        book_depth[time_col] = pd.to_datetime(book_depth[time_col])
        return book_depth

    def _casting(self, book_depth: pd.DataFrame) -> pd.DataFrame:
        """
        book_depth dataframe type casting
        """
        book_depth = book_depth.astype(BinanceBookDepthColumnMap.TYPEMAP)
        return book_depth
