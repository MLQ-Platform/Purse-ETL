from abc import ABC
from abc import abstractmethod


class BaseLoader(ABC):
    """
    Loader Abstract Singletone Class
    """

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass
