from etl.extractor.binance_collector import BaseBinanceCollection


class BinanceFuturesKlinesUM(BaseBinanceCollection):
    """
    USD-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(
            market_type="futures/um",
            data_type="klines",
            ticker=ticker,
            timeframe=timeframe,
        )


class BinanceFuturesKlinesCM(BaseBinanceCollection):
    """
    COIN-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(
            market_type="futures/cm",
            data_type="klines",
            ticker=ticker,
            timeframe=timeframe,
        )


class BinanceSpotKlines(BaseBinanceCollection):
    """
    SPOT COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(
            market_type="spot",
            data_type="klines",
            ticker=ticker,
            timeframe=timeframe,
        )
