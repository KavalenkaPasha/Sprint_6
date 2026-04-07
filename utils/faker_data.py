from __future__ import annotations

from datetime import date, timedelta

from faker import Faker

from models.order_data import OrderData


Faker.seed(1234)
fake = Faker("ru_RU")


def _build_safe_address() -> str:
    """Возвращает адрес в формате, который стабильно проходит клиентскую валидацию."""
    street_name = fake.street_name().replace("проспект", "пр-кт").replace("переулок", "пер.")
    house_number = fake.building_number().replace("/", "")
    apartment = fake.random_int(min=1, max=250)
    return f"{street_name}, д. {house_number}, кв. {apartment}"


def generate_order_data(
    *,
    case_id: str = "generated_order",
    metro: str = "Черкизовская",
    rental_period: str = "сутки",
    color: str = "black",
    delivery_offset_days: int = 2,
    comment_prefix: str | None = None,
) -> OrderData:
    delivery_date = (date.today() + timedelta(days=delivery_offset_days)).strftime(
        "%d.%m.%Y"
    )
    comment = (comment_prefix or fake.text(max_nb_chars=50)).replace("\n", " ").strip()

    return OrderData(
        case_id=case_id,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        address=_build_safe_address(),
        metro=metro,
        phone=fake.numerify(text="+79#########"),
        delivery_date=delivery_date,
        rental_period=rental_period,
        color=color,
        comment=comment,
    )
