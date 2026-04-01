from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class OrderEntryPoint(str, Enum):
    TOP = "top"
    BOTTOM = "bottom"


@dataclass(frozen=True, slots=True)
class OrderData:
    case_id: str
    first_name: str
    last_name: str
    address: str
    metro: str
    phone: str
    delivery_date: str
    rental_period: str
    color: str
    comment: str

    def __str__(self) -> str:
        return self.case_id
