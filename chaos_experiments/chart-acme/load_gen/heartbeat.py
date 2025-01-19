import datetime
import logging
import random
from math import sin, cos
from pathlib import Path

import jwt
from locust import LoadTestShape, FastHttpUser, constant
from locust import SequentialTaskSet
from locust import task
from rest_framework import status as http_status_code

# List of users (pre-loaded into ACME Fitness shop)
users = ["eric", "phoebe", "dwight", "han", "elaine", "walter"]

current_working_directory = Path.cwd()


# GuestUserBrowsing simulates traffic for a Guest User (Not logged in)
class UserBrowsing(SequentialTaskSet):
    def on_start(self):
        self.getProducts()

    def listCatalogItems(self):
        try:
            products = []
            response = self.client.get("/products")
            if response.status_code == http_status_code.HTTP_200_OK:
                items = response.json()["data"]
                for item in items:
                    products.append(item["id"])
            return products
        except Exception as exc:
            print("listCatalogItems exception: {a}".format(a=exc))

    def getProductDetails(self, id):
        """Get details of a specific product"""
        try:
            details = {}
            response = self.client.get("/products/" + id)
            if response.status_code == http_status_code.HTTP_200_OK:
                details = response.json()["data"]
                logging.debug("getProductDetails: " + str(details))
            return details
        except Exception as exc:
            print("getProductDetails exception: {a}".format(a=exc))

    def getProductImages(self, id):
        """Gets all three image URLs for a product"""
        try:
            details = self.getProductDetails(id)
            if details:
                for x in range(1, 4):
                    self.client.get(details["imageUrl" + str(x)])
        except Exception as exc:
            print("getProductImages exception: {a}".format(a=exc))

    def getProductName(self, id):
        try:
            name = ""
            details = self.getProductDetails(id)
            if details:
                name = details["name"]
            logging.debug("NAME: " + name + " for id: " + id)
            return name
        except Exception as exc:
            print("getProductName exception: {a}".format(a=exc))

    @task(2)
    def getProducts(self):
        try:
            self.client.get("/products")
        except Exception as exc:
            print("getProducts exception: {a}".format(a=exc))

    @task(2)
    def getProduct(self):
        """Get details of a specific product"""
        try:
            products = self.listCatalogItems()
            id = random.choice(products)
            response = self.client.get("/products/" + id)
            if response.status_code == http_status_code.HTTP_200_OK:
                product = response.json()
                logging.debug("Product info - " + str(product))
        except Exception as exc:
            print("getProduct exception: {a}".format(a=exc))

    @task(2)
    def getImages(self):
        """Get images of a random product"""
        try:
            logging.debug("User - Get images of random product")
            products = self.listCatalogItems()
            id = random.choice(products)
            self.getProductImages(id)
        except Exception as exc:
            print("getImages exception: {a}".format(a=exc))

    @task(2)
    def index(self):
        try:
            self.client.get("/")
        except Exception as exc:
            print("index exception: {a}".format(a=exc))


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
            print("removeProductFromCart exception: {a}".format(a=exc))

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
            body = response.json()
            decoded_token = jwt.decode(body["access_token"],
                                       "secret",
                                       algorithms=["HS256"],
                                       options={
                                           "verify_signature": False,
                                           "verify_exp": False
                                       })
            self.user.userid = decoded_token["sub"]
        except Exception as exc:
            print("login exception: {a}".format(a=exc))

    @task(5)
    def addToCart(self):
        """Randomly adds 1 or 2 of a random product to the cart"""
        try:
            products = self.listCatalogItems()
            productid = random.choice(products)

            details = self.getProductDetails(productid)
            self.client.post("/cart/item/add/{a}".format(a=self.user.userid),
                             json={
                                 "name": details["name"],
                                 "price": details["price"],
                                 "shortDescription": "Test add to cart",
                                 "quantity": random.randint(1, 2),
                                 "itemid": productid
                             })
        except Exception as exc:
            print("addToCart exception: {a}".format(a=exc))

    @task
    def removeFromCart(self):
        """Remove a random product from the cart. Helps prevent the cart from overflowing"""
        try:
            products = self.listCatalogItems()
            productid = random.choice(products)
            self.removeProductFromCart(self.user.userid, productid)
        except Exception as exc:
            print("removeFromCart exception: {a}".format(a=exc))

    @task(20)
    def checkout(self):
        try:
            self.client.get("/cart/items/" + self.user.userid).json()
            self.client.post("/order/add/" + self.user.userid,
                             json=self.Order_Info)

        except Exception as exc:
            print("checkout exception: {a}".format(a=exc))


class User(FastHttpUser):
    """
    A locust user class that will be hatched and run by the locust runner.
    """

    tasks = [UserBrowsing, AuthUserBrowsing]
    wait_time = constant(1)


class CustomShape(LoadTestShape):
    step_time = 60

    def tick(self):
        run_time = self.get_run_time()
        current_user = run_time // self.step_time
        user_num = int(7 + (cos(4 * current_user / 6) + (5 * sin(4 * current_user / 30))))
        return user_num, 50

# locust --headless -f acmefitness.py --host=http://34.159.136.97:80
