import math

from customer import Customer
from utils import attend_customer_time, is_bad_time, get_arrive_time, get_free_chef, TOTAL_TIME


def simulate(total_time_work: int, lambda_value: int, amount_chefs: int, extra_chef: bool):
    amount_chefs += extra_chef

    arrives_number = amount_customers_now = elapsed_time = 0
    chefs = [0] * amount_chefs
    service_time = [math.inf] * amount_chefs  # finalization time
    attended_by_chef = [0] * amount_chefs
    customers_dict = {}
    pending_customers = []
    arrive_time = get_arrive_time(lambda_value)

    while True:
        if extra_chef:
            bad_time = is_bad_time(elapsed_time)

            if bad_time and math.isinf(chefs[-1]):
                chefs[-1] = 0

            if not bad_time and chefs[-1] == 0:
                chefs[-1] = service_time[-1] = math.inf

        if arrive_time <= min(service_time) and arrive_time <= total_time_work:  # new arrival
            elapsed_time = arrive_time
            arrives_number += 1
            amount_customers_now += 1
            customer = customers_dict[arrives_number] = Customer(arrives_number)
            customer.set_arrive(arrive_time)
            arrive_time += get_arrive_time(lambda_value)

            free_worker = get_free_chef(chefs)

            if free_worker != -1:  # assign chef to attend customer
                customer.set_attended(elapsed_time)
                chefs[free_worker] = arrives_number
                service_time[free_worker] = elapsed_time + attend_customer_time(customer)
                attended_by_chef[free_worker] += 1
            else:
                pending_customers.append(arrives_number)
        else:
            if arrive_time > total_time_work and not amount_customers_now:
                overtime = max(elapsed_time - total_time_work, 0)
                break

            # attend customers
            t_i = min(service_time)
            elapsed_time = t_i
            i = service_time.index(t_i)
            customer = chefs[i]
            customers_dict[customer].set_finish(t_i)
            amount_customers_now -= 1

            if pending_customers:  # attend first customer in queue
                customer_id = pending_customers.pop(0)
                chefs[i] = customer_id
                customers_dict[customer_id].set_attended(t_i)
                service_time[i] = elapsed_time + attend_customer_time(customers_dict[customer_id])
                attended_by_chef[i] += 1
            else:  # release worker
                chefs[i] = 0
                service_time[i] = math.inf

    return customers_dict


def run(simulations: int, lambda_value: int, extra_chef: bool):
    total_out_time, total_customers = 0, 0

    for _ in range(simulations):
        customers = simulate(TOTAL_TIME, lambda_value, 2, extra_chef)
        out_time = [1 if (customer.attended - customer.arrive) > 5 else 0 for customer in customers.values()]

        total_out_time += sum(out_time)
        total_customers += len(customers)

    customers = total_customers / simulations
    out_time = total_out_time / simulations

    return (out_time / customers) * 100


if __name__ == '__main__':
    for lambda_value in [1 / 2, 1 / 3, 1 / 4, 1 / 5, 1 / 6, 1 / 7, 1 / 8]:
        print(f"------------------Testing with lambda {lambda_value}-------------------------")
        print(f"Dos chefs: ", run(1000, lambda_value, False), "%")
        print(f"Tres chefs: ", run(1000, lambda_value, True), "%\n\n")
