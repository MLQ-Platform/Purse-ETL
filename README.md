# Purse-ETL v1.0.0

Purse-ETL is a data extraction, transformation, and loading (ETL) tool designed for handling futures OHLCV data from Binance. This package provides functionalities for collecting data, transforming it into a standard OHLCV format, and loading it into a database for further analysis.

## Package Structre
```plaintext
├── etl
│   ├── __init__.py
│   ├── extractor
│   │   ├── __init__.py
│   │   ├── abstract.py
│   │   └── binance_collector
│   │       ├── __init__.py
│   │       ├── books.py
│   │       ├── klines.py
│   │       └── types.py
│   ├── loader
│   │   ├── __init__.py
│   │   ├── abstract.py
│   │   ├── query.py
│   │   ├── redis_loader.py
│   │   ├── sql_loader.py
│   │   └── table.py
│   ├── logger
│   │   ├── __init__.py
│   │   └── setup_logger.py
│   ├── transformer
│   │   ├── __init__.py
│   │   └── binance_collector
│   │       ├── __init__.py
│   │       ├── book_transformer.py
│   │       └── klines_transformer.py
│   └── utils.py
```

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

### 3. Load Data to MySQL Database

With the transformed data ready, load it into a MySQL database.

#### 3.1 Database Configuration

Load the database configuration and create a connection.

```python
from etl.loader import SQLDatabaseLoader
from etl.utils import load_db_config, get_db_uri 

# Get DB Config
db_config = load_db_config()

# Get DB URI
db_uri = get_db_uri(db_config)

# Initialize Loader
loader = SQLDatabaseLoader(db_uri=db_uri)
loader.connect()
```

#### 3.2 Prepare the Data for Loading

Create an `OHLCV` object to represent the data.

```python
from etl.loader.table import OHLCV
from etl.loader.query import upsert_query_func

ticker = 'BTCUSDt'

# Create OHLCV Object
table = OHLCV(
    datetime=ohlcv.index.tolist(),
    open=ohlcv.open.tolist(),
    high=ohlcv.high.tolist(),
    low=ohlcv.low.tolist(),
    close=ohlcv.close.tolist(),
    volume=ohlcv.volume.tolist(),
)
```

#### 3.3 Generate Upsert Query

Generate an upsert query to insert or update data in the database.

```python
# Generate Upsert Query
query = upsert_query_func(
    table, table_name=f"ohlcv_{ticker}".lower(), unique_key="datetime"
)
```

#### 3.4 Execute the Data Transaction

Execute the transaction to load the data into the database.

```python
# Data Transaction
loader.transaction(query)
loader.close()
```
