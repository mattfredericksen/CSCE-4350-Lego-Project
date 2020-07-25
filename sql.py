from mysql.connector import connect


class LegoDB:
    def __init__(self, host, username, password, database):
        self.credentials = {
            'host': host,
            'username': username,
            'password': password,
            'database': database
        }
        self.user_id = None
        self.user_type = None
        self.store = None

    def execute(self, query, *args, single=False, procedure=False, fetch=True):
        """This function is used by many others to wrap the process of connecting
        to the database, executing SQL, committing, and closing the connection.
        """
        db = connect(**self.credentials)
        cursor = db.cursor()
        if procedure:
            cursor.callproc(query, args)
            result = None
        else:
            cursor.execute(query, args)
            if single:
                result = cursor.fetchone() if fetch else None
            else:
                result = cursor.fetchall() if fetch else None
        cursor.close()
        db.commit()
        db.close()
        return result

    def username_exists(self, username) -> bool:
        if self.execute("""SELECT customer_id FROM customers
                           WHERE username = %s;""", username):
            return True
        return False

    def create_customer(self, username, password, name, email, address, store_preference):
        self.execute("""INSERT INTO Customers (username, password, name, email, address, store_preference)
                        VALUES (%s, %s, %s, %s, %s, %s);""",
                     username, password, name, email, address, store_preference, fetch=False)

    def user_login(self, username, password, employee=False) -> bool:
        attribute, table = ('customer_id', 'Customers') \
            if not employee else ('employee_id', 'Employees')
        self.user_id = self.execute(f"""SELECT {attribute} FROM {table}
                                        WHERE username = %s AND password = %s;""",
                                    username, password, single=True)
        if not self.user_id:
            return False
        else:
            self.user_id = self.user_id[0]
            return True

    def get_user_store(self, employee=False):
        attribute, table = ('store_preference', 'Customers') \
            if not employee else ('store', 'Employees')
        return self.execute(f"""SELECT {attribute} FROM {table}
                                WHERE customer_id = %s""",
                            self.user_id, single=True)[0]

    def get_sets(self, set_id=None, description=True):
        if set_id:
            item = self.execute("""SELECT * FROM Sets
                                   WHERE set_id = %s;""", set_id, single=True)
            if not item:
                raise ValueError
            else:
                return item
        elif description:
            return self.execute("""SELECT set_id, name, description
                                   FROM Sets
                                   WHERE active = TRUE;""")
        else:
            return self.execute("""SELECT set_id, name
                                   FROM Sets
                                   WHERE active = TRUE;""")

    def get_bricks(self, brick_id=None):
        if brick_id:
            brick = self.execute("""SELECT * FROM Bricks
                                    WHERE brick_id = %s;""", brick_id, single=True)
            if not brick:
                raise ValueError
            else:
                return brick
        else:
            return self.execute("""SELECT brick_id, description FROM Bricks 
                                   WHERE active = TRUE;""")

    def get_set_price(self, set_id):
        price = self.execute("""SELECT SUM(quantity * price)
                                FROM Sets_Bricks
                                INNER JOIN Bricks 
                                ON Sets_Bricks.brick_id = Bricks.brick_id
                                WHERE set_id = %s;""", set_id, single=True)
        return round(price[0], 2)

    def get_set_count(self, set_id):
        return self.execute("""SELECT SUM(quantity) FROM Sets_Bricks
                               WHERE set_id = %s;""", set_id, single=True)[0]

    def get_set_inventory(self, set_id):
        result = self.execute("""SELECT inventory FROM Stores_Sets
                                 WHERE store_id = %s AND set_id = %s;""",
                              self.get_user_store(), set_id, single=True)
        return result[0] if result else 0

    def get_brick_inventory(self, brick_id):
        result = self.execute("""SELECT inventory FROM Stores_Bricks
                                 WHERE store_id = %s AND brick_id = %s;""",
                              self.get_user_store(), brick_id,
                              single=True)
        return result[0] if result else 0

    def modify_cart(self, item_id, quantity):
        self.execute('ModifyCartSets' if item_id < 10000 else 'ModifyCartBricks',
                     self.user_id, item_id, quantity,
                     procedure=True)

    def get_cart(self):
        cart_id = self.execute("""SELECT order_id FROM Customer_Orders
                                  WHERE customer_id = %s AND status = 'Cart';""",
                               self.user_id, single=True)[0]
        return self.execute("""
                  SELECT Sets.set_id, name, quantity, price
                  FROM Customer_Orders_Sets
                  INNER JOIN Sets
                  ON Customer_Orders_Sets.set_id = Sets.set_id
                  INNER JOIN (SELECT set_id, SUM(quantity * price) as price
                              FROM Sets_Bricks
                              INNER JOIN Bricks 
                              ON Sets_Bricks.brick_id = Bricks.brick_id
                              GROUP BY set_id)
                              AS Sets_Prices
                  ON Sets.set_id = Sets_Prices.set_id
                  WHERE order_id = %s
                  UNION
                  SELECT Bricks.brick_id, description, quantity, price
                  FROM Customer_Orders_Bricks
                  INNER JOIN Bricks
                  ON Customer_Orders_Bricks.brick_id = Bricks.brick_id
                  WHERE order_id = %s;""", cart_id, cart_id)

    def get_payments(self):
        return self.execute("""SELECT payment_id, SUBSTRING(card_number, 13, 4), billing_address
                  FROM Payments
                  WHERE customer_id = %s
                  AND active = TRUE;""", self.user_id)

    def checkout(self, payment_id):
        total = sum(quantity * price for *_, quantity, price
                    in self.get_cart())
        self.execute('CartToOrder', self.user_id, payment_id,
                     self.get_user_store(), total, procedure=True)

    def get_customer_orders(self, order_id=None):
        if order_id:
            return self.execute("""SELECT name, quantity FROM customer_orders_sets
                      INNER JOIN sets
                      ON customer_orders_sets.set_id = sets.set_id
                      WHERE order_id = %s
                      UNION
                      SELECT description, quantity FROM customer_orders_bricks
                      INNER JOIN bricks
                      ON customer_orders_bricks.brick_id = bricks.brick_id
                      WHERE order_id = %s;""", order_id, order_id)
        else:
            return self.execute("""SELECT order_id, order_timestamp, total_price, status, delivery_timestamp
                      FROM customer_orders 
                      WHERE customer_id = %s AND status <> 'Cart'
                      ORDER BY order_timestamp;""", self.user_id)

    def add_payment_option(self, card, exp_date, address):
        self.execute("""INSERT INTO Payments (customer_id, card_number, exp_date, billing_address)
                        VALUES (%s, %s, %s, %s)""",
                     self.user_id, card, exp_date, address, fetch=False)

    def get_stores(self, store_id=None):
        if store_id:
            return self.execute("""SELECT address FROM Stores
                                   WHERE store_id = %s;""",
                                store_id, single=True)[0]
        else:
            return self.execute("""SELECT store_id, address FROM Stores
                                   WHERE active = TRUE;""")

    def set_store_preference(self, store_id: int):
        self.execute("""UPDATE Customers
                        SET store_preference = %s
                        WHERE customer_id = %s""",
                     store_id, self.user_id, fetch=False)

    def get_shipping_address(self):
        return self.execute("""SELECT address FROM customers
                               WHERE customer_id = %s;""",
                            self.user_id, single=True)[0]

    def set_shipping_address(self, address: str):
        self.execute("""UPDATE Customers
                        SET address = %s
                        WHERE customer_id = %s;""",
                     address, self.user_id, fetch=False)

    def create_sale(self, sale_items: dict, credit_card: str):
        total_price = sum(item['quantity'] * item['price'] for item in sale_items.values())
        db = connect(**self.credentials)
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO Store_Sales (store_id, employee_id, total_price, credit_card)
               VALUES (%s, %s, %s, %s);""",
            (self.get_user_store(), self.user_id, total_price, credit_card if credit_card else None))

        sets, bricks = [], []
        for item_id, item in sale_items.items():
            (sets if item_id < 10000 else bricks).append(
                    (cursor.lastrowid, item_id, item['quantity']))

        cursor.executemany(
            """INSERT INTO Store_Sales_Sets
               VALUES (%s, %s, %s)""", sets)
        cursor.executemany(
            """INSERT INTO Store_Sales_Bricks
               VALUES (%s, %s, %s)""", bricks)
        cursor.close()
        db.commit()
        db.close()
