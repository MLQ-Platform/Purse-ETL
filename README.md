# Purse-ETL

Purse-ETL is a data extraction, transformation, and loading (ETL) tool designed for handling futures OHLCV data from Binance. This package provides functionalities for collecting data, transforming it into a standard OHLCV format, and loading it into a database for further analysis.


## Quick Start
```python
from etl.extractor.binance_collector import BinanceFuturesUM
from etl.extractor.binance_collector.types import TimeFrame

# Binance Data Collection Extractor
extractor_um = BinanceFuturesUM(ticker='BTCUSDT', timeframe=TimeFrame.MINUTE5)

# Klines Data
klines = extractor_um.load(start_date='2024-09-12', end_date='2024-09-12')

# Transformer 
transformer = BinanceKlinesTransformer()

ohlcv = transformer.transform(klines)
```

Example Output:
```
                     open     high      low    close   volume
datetime                                                   
2024-09-12 00:00:00  57305.6  57384.6  57283.1  57343.7  657.984
2024-09-12 00:05:00  57343.8  57425.4  57343.8  57421.9  416.098
...
2024-09-12 23:55:00  58070.4  58104.1  58067.8  58097.0  184.711
```

