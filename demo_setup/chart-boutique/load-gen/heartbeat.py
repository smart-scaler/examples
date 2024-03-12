# import rlautoscaler.utils.logger as Log
import random

from locust import LoadTestShape, FastHttpUser
from locust import TaskSet, constant_throughput

products = [
    '0PUK6V6EV0',
    '1YMWWN1N4O',
    '2ZYFJ3GM2N',
    '66VCHSJNUP',
    '6E92ZMYYFZ',
    '9SIQT8TOJO',
    'L9ECAV7KIM',
    'LS4PSXUNUM',
    'OLJCESPC7Z']


def index(l):
    l.client.get("/")


def setCurrency(l):
    currencies = ['EUR', 'USD', 'JPY', 'CAD']
    l.client.post("/setCurrency",
                  {'currency_code': random.choice(currencies)})


def browseProduct(l):
    l.client.get("/product/" + random.choice(products))


def viewCart(l):
    l.client.get("/cart")


def addToCart(l):
    product = random.choice(products)
    l.client.get("/product/" + product)
    l.client.post("/cart", {
        'product_id': product,
        'quantity': random.choice([1, 2, 3, 4, 5, 10])})


def checkout(l):
    addToCart(l)
    l.client.post("/cart/checkout", {
        'email': 'someone@example.com',
        'street_address': '1600 Amphitheatre Parkway',
        'zip_code': '94043',
        'city': 'Mountain View',
        'state': 'CA',
        'country': 'United States',
        'credit_card_number': '4432-8015-6152-0454',
        'credit_card_expiration_month': '1',
        'credit_card_expiration_year': '2039',
        'credit_card_cvv': '672',
    })


class UserTasks(TaskSet):
    """
    Locust user task set.
    """

    def on_start(self):
        index(self)

    tasks = {index: 10,
             setCurrency: 10,

             viewCart: 10,
             checkout: 1}

    # tasks = {index: 1, checkout:1, viewCart:3}


class User(FastHttpUser):
    """
    A locust user class that will be hatched and run by the locust runner.
    """

    tasks = {UserTasks}
    wait_time = constant_throughput(1)
    connection_timeout = 2.0
    network_timeout = 2.0
    # host = "http://abae047c010e04445aa98ba5266551dc-874206348.us-east-1.elb.amazonaws.com"


class CustomShape(LoadTestShape):
    """
    docstring
    """

    step_time = 60
    phase_1 = 40
    phase_2 = 80
    phase_length = 5

    def tick(self):
        run_time = self.get_run_time()

        current_user = run_time // 60
        from math import sin, cos

        user_num = int(7 + (cos(4 * current_user / 6) + (5 * sin(4 * current_user / 30))))
        # user_num = int(40+ 5*(5*sin(4*current_user/30)))
        # print(user_num)
        return user_num, 40

# locust -f sinusoidal.py
# locust --headless -f sinusoidal.py --host=http://XX.XXX.XX.XXX:XX
