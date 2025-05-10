from etl.extractor.binance_collector import BaseBinanceCollection


class BinanceFuturesAggTradesUM(BaseBinanceCollection):
    """
    USD-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(
            market_type="futures/um",
            data_type="aggTrades",
            ticker=ticker,
            timeframe=timeframe,
        )


class BinanceFuturesAggTradesCM(BaseBinanceCollection):
    """
    Agg Trades COIN-M COLLECTOR
    """

    def __init__(self, ticker: str, timeframe: str) -> None:
        super().__init__(
            market_type="futures/cm",
            data_type="aggTrades",
            ticker=ticker,
            timeframe=timeframe,
        )
