from enum import Enum


class EnumWithValues(str, Enum):
    @classmethod
    def values(cls):
        return [x.value for x in cls.__members__.values()]

    def __str__(self):
        return self.value
