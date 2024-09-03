from typing import List, Any
from dataclasses import dataclass
from dataclasses import fields


@dataclass
class Table:
    @property
    def columns(self) -> List[str]:
        """
        List of Data Feilds
        """
        return [field.name for field in fields(self)]

    @property
    def itertuples(self) -> List[Any]:
        """
        List or Row Values
        """
        return [
            tuple(getattr(self, column)[i] for column in self.columns)
            for i in range(len(getattr(self, self.columns[0])))
        ]

    @property
    def comma_seperated_columns(self) -> str:
        """
        Comma Seperated Columns
        """
        csc = ", ".join(self.columns)
        return csc

    @property
    def comma_seperated_itertuples(self) -> str:
        """
        Comma Seperated Values
        """
        csv = ", ".join(str(tuple(row)) for row in self.itertuples)
        return csv


@dataclass
class OHLCV(Table):
    datetime: List[str]
    open: List[float]
    high: List[float]
    low: List[float]
    close: List[float]
    volume: List[float]
