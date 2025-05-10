from etl.extractor.binance_collector import BaseBinanceCollection


class BinanceFuturesBookTickerUM(BaseBinanceCollection):
    """
    Book Ticker USD-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(
            market_type="futures/um",
            data_type="bookTicker",
            ticker=ticker,
            timeframe=timeframe,
        )


class BinanceFuturesBookTickerCM(BaseBinanceCollection):
    """
    Book Ticker COIN-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(
            market_type="futures/cm",
            data_type="bookTicker",
            ticker=ticker,
            timeframe=timeframe,
        )
