from abc import ABCMeta
from abc import abstractmethod
from typing import Any


class BaseEntity(metaclass=ABCMeta):
    @property
    @abstractmethod
    def api_data(self) -> dict[str, Any]:
        raise NotImplementedError

    @staticmethod
    def omit_none_values(data: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in data.items() if value is not None}
