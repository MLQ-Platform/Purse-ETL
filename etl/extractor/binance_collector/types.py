from enum import Enum


class TimeFrame(Enum):
    HOUR12 = "12h"
    HOUR1 = "1h"
    MINUTE1 = "1m"
    MINUTE5 = "5m"
    DAY1 = "1d"
    TRADES = "trades"
    AGGTRADES = "aggTrades"
    BOOKDEPTH = "bookDepth"
    BOOKTICKER = "bookTicker"
