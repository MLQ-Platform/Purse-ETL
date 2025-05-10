# Purse-ETL

Purse-ETL is a data extraction, transformation, and loading (ETL) tool designed for handling futures OHLCV data from Binance. This package provides functionalities for collecting data, transforming it into a standard OHLCV format, and loading it into a database for further analysis.


## Quick Start

### 1. Extract Futures OHLCV from Binance Data Collection

The first step is to extract the OHLCV data from Binance using the `BinanceFuturesUM` extractor.

```python
from etl.extractor.binance_collector import BinanceFuturesUM
from etl.extractor.binance_collector.types import TimeFrame

# Binance Data Collection Extractor
extractor_um = BinanceFuturesUM(ticker='BTCUSDT', timeframe=TimeFrame.MINUTE5)

# Klines Data
klines = extractor_um.load(start_date='2024-09-12', end_date='2024-09-12')
```

Example Output:
```
2024-09-18 02:26:19,108 - INFO - Files in ZIP for 2024-09-12: ['BTCUSDT-5m-2024-09-12.csv']
2024-09-18 02:26:19,120 - INFO - Loaded data with shape: (288, 12)
```

### 2. Transform OHLCV Data

Once the data is extracted, transform it into the standard OHLCV format using `BinanceKlinesTransformer`.

```python
from etl.transformer.binance_collector import BinanceKlinesTransformer

transformer = BinanceKlinesTransformer()
ohlcv = transformer.transform(klines)
ohlcv
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

