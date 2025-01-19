import datetime
import logging
import random
from math import sin, cos
from pathlib import Path

import jwt
import json
from locust import LoadTestShape, FastHttpUser, constant
from locust import SequentialTaskSet
from locust import task, events as locust_events 
from rest_framework import status as http_status_code


import threading

# 1. Failure Tracker
class FailureTracker:
    def __init__(self):
        self.lock = threading.Lock()
        self.failures = 0
        self.total_requests = 0
        self.failures_gradient = True
        self.failures_graph = [True for _ in range(200)]
        self.current_step = 0

    def on_request_failure(self, request_type, name, response_time, exception, **kwargs):
        with self.lock:
            # print(f"Failure tracked: {name} - {exception}")
            pass
            if "503" in str(exception):
                self.failures += 1
                self.failures_graph.pop()
                self.failures_graph.insert(0, False)
            else:
                self.failures_graph.pop()
                self.failures_graph.insert(0, True)
            self.total_requests += 1
        logging.debug(f"Failure tracked: {name} - {exception}")

    def on_request_success(self, request_type, name, response_time, **kwargs):
        with self.lock:
            self.total_requests += 1
            self.failures_graph.pop()
            self.failures_graph.insert(0, True)
        logging.debug(f"Success tracked: {name}")

    def get_failure_rate(self):
        with self.lock:
            if self.total_requests == 0:
                return 0.0
            return self.failures / self.total_requests

    def reset(self):
        with self.lock:
            self.failures = 0
            self.total_requests = 0

    def are_failures_cleared(self):
        with self.lock:
            return self.failures_graph.count(True)/ len(self.failures_graph) == 1
    
    def set_current_step(self, current_step):
        with self.lock:
            self.current_step = current_step
    
    def get_current_step(self):
        with self.lock:
            return self.current_step
    

# Instantiate the failure tracker
failure_tracker = FailureTracker()

# 2. Register event listener for 'request' event
@locust_events.request.add_listener
def handle_request(request_type, name, response_time, response_length, exception, context, **kwargs):
    
    if exception is None:
        failure_tracker.on_request_success(request_type, name, response_time, **kwargs)
        
    else:
        failure_tracker.on_request_failure(request_type, name, response_time, exception, **kwargs)
        

# List of users (pre-loaded into ACME Fitness shop)
users = ["eric", "phoebe", "dwight", "han", "elaine", "walter"]

current_working_directory = Path.cwd()

num_users=20

# GuestUserBrowsing simulates traffic for a Guest User (Not logged in)
class UserBrowsing(SequentialTaskSet):
    def on_start(self):
        self.getProducts()

    def listCatalogItems(self):
        try:
            products = []
            response = self.client.get("/products")
            if response.status_code == http_status_code.HTTP_200_OK:
                
                items = json.loads(response.content)["data"]
                for item in items:
                    products.append(item["id"])
            else:
                global num_users
                num_users = num_users+20
            return products
        except Exception as exc:
            print(exc)
            

    def getProductDetails(self, id):
        """Get details of a specific product"""
        try:
            details = {}
            response = self.client.get("/products/" + id)
            if response.status_code == http_status_code.HTTP_200_OK:
                details = json.loads(response.content)["data"]
                logging.debug("getProductDetails: " + str(details))
            return details
        except Exception as exc:
            print(exc)

    # def getProductImages(self, id):
    #     """Gets all three image URLs for a product"""
    #     try:
    #         details = self.getProductDetails(id)
    #         if details:
    #             for x in range(1, 4):
    #                 self.client.get(details["imageUrl" + str(x)])
    #     except Exception as exc:
            print(f"getProductImages {exc}")
            pass

    def getProductName(self, id):
        try:
            name = ""
            details = self.getProductDetails(id)
            if details:
                name = details["name"]
            logging.debug("NAME: " + name + " for id: " + id)
            return name
        except Exception as exc:
            # print(f"getProductName {exc}")
            pass

    @task(2)
    def getProducts(self):
        try:
            self.client.get("/products")
        except Exception as exc:
            # print(f"getProducts {exc}")
            pass

    # @task(2)
    # def getProduct(self):
    #     """Get details of a specific product"""
    #     try:
    #         products = self.listCatalogItems()
    #         id = random.choice(products)
    #         response = self.client.get("/products/" + id)
    #         if response.status_code == http_status_code.HTTP_200_OK:
    #             product = json.loads(response.content)
    #             logging.debug("Product info - " + str(product))
    #     except Exception as exc:
    #         # print(f"getProduct {exc}")
    #         pass

    # @task(2)
    # def getImages(self):
    #     """Get images of a random product"""
    #     try:
    #         logging.debug("User - Get images of random product")
    #         products = self.listCatalogItems()
    #         id = random.choice(products)
    #         self.getProductImages(id)
    #     except Exception as exc:
    #         print(exc)

    # @task(2)
    # def index(self):
    #     try:
    #         self.client.get("/")
    #     except Exception as exc:
    #         print(exc)


# AuthUserBrowsing simulates traffic for Authenticated Users (Logged in)
class AuthUserBrowsing(UserBrowsing):
    """
    AuthUserBrowsing extends the base UserBrowsing class as an authenticated user
    interacting with the cart and making orders
    """
    Order_Info = {
        "userid":
            "8888",
        "firstname":
            "Eric",
        "lastname":
            "Cartman",
        "address": {
            "street": "20 Riding Lane Av",
            "city": "San Francisco",
            "zip": "10201",
            "state": "CA",
            "country": "USA"
        },
        "email":
            "jblaze@marvel.com",
        "delivery":
            "UPS/FEDEX",
        "card": {
            "type": "amex/visa/mastercard/bahubali",
            "number": "3498347979811234",
            "expMonth": "12",
            "expYear": "{a}".format(a=datetime.date.today().year + 5),
            "ccv": "123"
        },
        "cart": [{
            "id": "1234",
            "description": "redpants",
            "quantity": "1",
            "price": "4"
        }, {
            "id": "5678",
            "description": "bluepants",
            "quantity": "1",
            "price": "4"
        }],
        "total":
            "100"
    }

    def on_start(self):
        self.login()

    def removeProductFromCart(self, userid, productid):
        """Removes a specific product from the cart by setting the quantity of the product to 0"""
        try:
            self.client.post("/cart/item/modify/" + userid,
                             json={
                                 "itemid": productid,
                                 "quantity": 0
                             })
        except Exception as exc:
            # print(f"removeProductFromCart {exc}")
            pass

    @task
    def login(self):
        """Login a random user"""
        try:
            user = random.choice(users)
            response = self.client.post("/login/",
                                        json={
                                            "username": user,
                                            "password": "vmware1!"
                                        })

            body = json.loads(response.content)
            decoded_token = jwt.decode(body['access_token'],
                                       "secret",
                                       algorithms=["HS256"],
                                       options={
                                           "verify_signature": False,
                                           "verify_exp": False
                                       })
            self.user.userid = decoded_token["sub"]
        except Exception as exc:
            # print(f"login {exc}")
            pass

    # @task(5)
    # def addToCart(self):
    #     """Randomly adds 1 or 2 of a random product to the cart"""
    #     try:
    #         products = self.listCatalogItems()
    #         productid = random.choice(products)

    #         details = self.getProductDetails(productid)
    #         self.client.post("/cart/item/add/{a}".format(a=self.user.userid),
    #                          json={
    #                              "name": details["name"],
    #                              "price": details["price"],
    #                              "shortDescription": "Test add to cart",
    #                              "quantity": random.randint(1, 2),
    #                              "itemid": productid
    #                          })
    #     except Exception as exc:
    #         # print(exc)
    #         print("addToCart", exc)

    # @task
    # def removeFromCart(self):
    #     """Remove a random product from the cart. Helps prevent the cart from overflowing"""
    #     try:
    #         products = self.listCatalogItems()
    #         productid = random.choice(products)
    #         self.removeProductFromCart(self.user.userid, productid)

    #     except Exception as exc:
    #         print("removeFromCart", exc)

    # @task(20)
    # def checkout(self):
    #     try:
    #         response = self.client.get("/cart/items/" + self.user.userid)
    #         body = json.loads(response.content)
    #         self.client.post("/order/add/" + self.user.userid,
    #                          json=self.Order_Info)

    #     except Exception as exc:
    #         print("checkout", exc)


class User(FastHttpUser):
    """
    A locust user class that will be hatched and run by the locust runner.
    """

    tasks = [UserBrowsing, AuthUserBrowsing]
    wait_time = constant(1)


class CustomShape(LoadTestShape):
    """
    A custom load shape that adjusts the number of users based on failure rates.
    The step counter resets to zero whenever failures are cleared.
    """

    step_time = 10          # Time interval for steps in seconds
    initial_users = 20     # Starting number of users
    user_increment = 60    # Users to add at each step
    spawn_rate = 20        # Users to spawn per second
    max_users = 1280       # Maximum number of users
    cycle = 180            # Cycle duration

    def __init__(self):
        super().__init__()
        self.step_counter = 0  # Initialize step counter

    def tick(self):
        run_time = self.get_run_time()
        current_step = run_time // self.step_time
        
        # Check if failures are cleared
        if failure_tracker.are_failures_cleared():
            self.step_counter = 0          # Reset step counter
            failure_tracker.reset()       # Reset failure tracker
            # logging.info("Failures cleared. Resetting user count to initial_users.")
            return (self.initial_users, self.spawn_rate)

        # Increment step counter only if there are failures
        # print(f"current_step: {current_step}, failure_tracker.get_current_step(): {failure_tracker.get_current_step()}")
        pass
        if (current_step>failure_tracker.get_current_step()):
            failure_tracker.set_current_step(current_step)
            self.step_counter += 1

        # Calculate failure rate
        failure_rate = failure_tracker.get_failure_rate()
        failure_adjustment = 1 if failure_rate > 0 else 0

        # Calculate user number based on current step and cycle
        
        user_num = self.initial_users * failure_adjustment * (2 ** self.step_counter)

        # Ensure user number does not exceed maximum
        if user_num > self.max_users:
            user_num = self.max_users

        logging.debug(f"Step: {self.step_counter}, Users: {user_num}, Failure Rate: {failure_rate}")

        return int(user_num), self.spawn_rate
