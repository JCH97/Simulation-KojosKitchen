import math
from random import random
from customer import Customer

TOTAL_TIME = 660


def uniform(a: int, b: int) -> float:
    return a + (b - a) * random()


def prepare_sushi() -> float:
    return uniform(3, 5)


def prepare_sandwich() -> float:
    return uniform(5, 8)


def get_arrive_time(lambda_value=10) -> float:
    return -(1 / lambda_value) * math.log(uniform(0, 1))


def attend_customer_time(customer: Customer):
    return prepare_sushi() if customer.order_type == 0 else prepare_sandwich()


def get_free_chef(chefs: list) -> int:
    for i, chef in enumerate(chefs):
        if chef == 0:
            return i

    return -1


def is_bad_time(time: int) -> bool:
    return (90 <= time <= 210) or (420 <= time <= 540)
