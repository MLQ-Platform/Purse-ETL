from etl.extractor.binance_collector import BaseBinanceCollection


class BinanceFuturesPremiumIndexUM(BaseBinanceCollection):
    """
    USD-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(
            market_type="futures/um",
            data_type="premiumIndexKlines",
            ticker=ticker,
            timeframe=timeframe,
        )


class BinanceFuturesPremiumIndexCM(BaseBinanceCollection):
    """
    COIN-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(
            market_type="futures/cm",
            data_type="premiumIndexKlines",
            ticker=ticker,
            timeframe=timeframe,
        )
