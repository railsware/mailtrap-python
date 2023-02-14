from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Dict


class BaseEntity(metaclass=ABCMeta):
    @property
    @abstractmethod
    def api_data(self) -> Dict[str, Any]:
        raise NotImplementedError

    @staticmethod
    def omit_none_values(data: Dict[str, Any]) -> Dict[str, Any]:
        return {key: value for key, value in data.items() if value is not None}
