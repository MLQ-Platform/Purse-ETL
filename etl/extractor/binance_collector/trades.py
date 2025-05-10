from etl.extractor.binance_collector import BaseBinanceCollection


class BinanceFuturesTradesUM(BaseBinanceCollection):
    """
    Trades USD-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(
            market_type="futures/um",
            data_type="trades",
            ticker=ticker,
            timeframe=timeframe,
        )


class BinanceFuturesTradesCM(BaseBinanceCollection):
    """
    Trades COIN-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(
            market_type="futures/cm",
            data_type="trades",
            ticker=ticker,
            timeframe=timeframe,
        )
