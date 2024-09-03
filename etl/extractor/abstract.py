from abc import ABC
from abc import abstractmethod


class BaseExtractor(ABC):
    """
    Extractor Abstract Class
    """

    @abstractmethod
    def load(self, data):
        pass
