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

## Data Structure

***AggTrades***

| 필드 | 설명 |
|------|------|
| Aggregate tradeId | 집계 거래 ID |
| Price | 거래 가격 |
| Quantity | 거래량 |
| First tradeId | 집계된 첫 번째 거래 ID |
| Last tradeId | 집계된 마지막 거래 ID |
| Timestamp | 거래 시간 (밀리초 단위) |
| Was the buyer the maker | 매수자가 메이커인지 여부 (true/false) |

***Klines***

USD-M Futures Klines:
| 필드 | 설명 |
|------|------|
| Open time | 시작 시간 (밀리초) |
| Open | 시가 |
| High | 고가 |
| Low | 저가 |
| Close | 종가 |
| Volume | 거래량 |
| Close time | 종료 시간 (밀리초) |
| Quote asset volume | 견적 자산 거래량 (USDT 등) |
| Number of trades | 거래 건수 |
| Taker buy base asset volume | 테이커 매수 기초 자산 거래량 |
| Taker buy quote asset volume | 테이커 매수 견적 자산 거래량 |
| Ignore | 사용하지 않는 필드 |

***Trades***

USD-M Futures Trades:
| 필드 | 설명 |
|------|------|
| trade Id | 거래 ID |
| price | 거래 가격 |
| qty | 거래량 |
| quoteQty | 견적 자산 거래량 (가격 × 거래량) |
| time | 거래 시간 (밀리초) |
| isBuyerMaker | 매수자가 메이커인지 여부 |

***Book Depth***
| 필드 | 설명 |
|------|------|
| timestamp | 데이터가 기록된 시간 |
| percentage | 현재가 대비 가격 변동 비율(%) |
| depth | 해당 가격대에 쌓인 주문량 |
| notional | 해당 가격대의 명목가치(depth × 가격) |
