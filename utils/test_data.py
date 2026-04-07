from __future__ import annotations

import pytest

from models.order_data import OrderEntryPoint


FAQ_DATA = [
    pytest.param(0, "Сутки — 400 рублей. Оплата курьеру — наличными или картой.", id="faq_price"),
    pytest.param(
        1,
        "Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим.",
        id="faq_several_scooters",
    ),
    pytest.param(
        2,
        "Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30.",
        id="faq_rental_time",
    ),
    pytest.param(3, "Только начиная с завтрашнего дня. Но скоро станем расторопнее.", id="faq_today"),
    pytest.param(
        4,
        "Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010.",
        id="faq_extend_or_return_early",
    ),
    pytest.param(
        5,
        "Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится.",
        id="faq_charger",
    ),
    pytest.param(
        6,
        "Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои.",
        id="faq_cancel",
    ),
    pytest.param(7, "Да, обязательно. Всем самокатов! И Москве, и Московской области.", id="faq_mkad"),
]

ORDER_ENTRY_POINTS = [OrderEntryPoint.TOP, OrderEntryPoint.BOTTOM]

ORDER_CASES = [
    pytest.param(
        "faker_black",
        {
            "delivery_offset_days": 2,
            "metro": "Черкизовская",
            "rental_period": "сутки",
            "color": "black",
            "comment_prefix": "Позвоните за 15 минут",
        },
        id="faker_black",
    ),
    pytest.param(
        "faker_grey",
        {
            "delivery_offset_days": 3,
            "metro": "Черкизовская",
            "rental_period": "двое суток",
            "color": "grey",
            "comment_prefix": "Домофон 45, подъезд 2",
        },
        id="faker_grey",
    ),
]
