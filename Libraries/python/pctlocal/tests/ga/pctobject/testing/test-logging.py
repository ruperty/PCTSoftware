import logging

logging.basicConfig(
    filename="test.log",
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d:%(levelname)s:%(module)s-%(lineno)d %(message)s",datefmt= '%H:%M:%S'
    )

class Pizza():
    def __init__(self, name, price):
        self.name = name
        self.price = price
        logging.info("Pizza created: \n{} (${})".format(self.name, self.price))

    def make(self, quantity=1):
        logging.debug("Made {} {} pizza(s)".format(quantity, self.name))

    def eat(self, quantity=1):
        logging.debug("Ate {} pizza(s)".format(quantity, self.name))

pizza_01 = Pizza("artichoke", 15)
pizza_01.make()
pizza_01.eat()

pizza_02 = Pizza("margherita", 12)
pizza_02.make(2)
pizza_02.eat()