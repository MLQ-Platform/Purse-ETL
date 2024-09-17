from pydantic import BaseModel
from typing import List
from datetime import datetime
from decimal import Decimal


# OHLCV 항목을 나타내는 Pydantic 모델
class OHLCVItem(BaseModel):
    datetime: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal


# 응답 모델로 리스트를 포함하는 Pydantic 모델
class OHLCVResponse(BaseModel):
    data: List[OHLCVItem]
