from random import uniform


class Customer:
    def __init__(self, id: int):
        self.id = id
        self.arrive = self.attended = self.finish = None
        self.order_type = 0 if uniform(0, 1) <= 0.5 else 1

    def __str__(self):
        return f"Customer {self.id}, arrive to kitchen at time {self.arrive} with " \
               f"order {self.order_type} and finish in time {self.finish}."

    def set_arrive(self, value: float):
        self.arrive = value

    def set_attended(self, value: float):
        self.attended = value

    def set_finish(self, value: float):
        self.finish = value

    def get_id(self) -> int:
        return self.id

    def get_arrive(self) -> float:
        return self.arrive

    def get_attended(self) -> float:
        return self.attended

    def get_finish(self) -> float:
        return self.finish