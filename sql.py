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
        return self.execute(
               """SELECT Sets.set_id, name, quantity, price
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
        return self.execute(
               """SELECT payment_id, SUBSTRING(card_number, 13, 4), billing_address
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
            return self.execute(
                   """SELECT name, quantity FROM customer_orders_sets
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

    def get_sale(self, sale_id):
        return self.execute(
               """SELECT set_id, quantity, total_price, SUBSTRING(credit_card, 13, 4)
                  FROM store_sales AS ss
                  INNER JOIN store_sales_sets AS sss
                  ON ss.sale_id = sss.sale_id
                  WHERE ss.sale_id = %s
                  UNION
                  SELECT brick_id, quantity, total_price, SUBSTRING(credit_card, 13, 4)
                  FROM store_sales AS ss
                  INNER JOIN store_sales_bricks AS ssb
                  ON ss.sale_id = ssb.sale_id
                  WHERE ss.sale_id = %s;""",
               sale_id, sale_id)

    def is_sale_returned(self, sale_id):
        return True if self.execute(
                       """SELECT * from Store_Sales_Returns
                          WHERE sale_id = %s;""",
                       sale_id, single=True)  \
               else False

    def create_return(self, sale_id, reason):
        self.execute("""INSERT INTO Store_Sales_Returns (sale_id, reason)
                        VALUES (%s, %s)""",
                     sale_id, reason, fetch=False)

    def orders_report(self):
        result = {}
        query = self.execute(
                    """SELECT COUNT(total_price), SUM(total_price), AVG(total_price) 
                       FROM customer_orders
                       WHERE status NOT IN ('Cart', 'Cancelled', 'Returned');""",
                    single=True)
        result.update({'order_count': query[0],
                       'order_total': query[1],
                       'average_price': query[2]})
        query = self.execute(
                    """SELECT SUM(quantity), AVG(quantity)
                       FROM customer_orders_bricks
                       WHERE order_id IN (SELECT order_id 
                                          FROM customer_orders
                                          WHERE status NOT IN 
                                          ('Cart', 'Cancelled', 'Returned'));""",
                    single=True)
        result.update({'brick_count': query[0],
                       'brick_average': round(query[1])})
        query = self.execute(
                    """SELECT SUM(quantity), AVG(quantity)
                       FROM customer_orders_sets
                       WHERE order_id IN (SELECT order_id 
                                          FROM customer_orders
                                          WHERE status NOT IN 
                                          ('Cart', 'Cancelled', 'Returned'));""",
                    single=True)
        result.update({'set_count': query[0],
                       'set_average': round(query[1])})
        return result

    def cancellations_report(self):
        return self.execute(
                   """SELECT COUNT(total_price), SUM(total_price) 
                      FROM Customer_Orders
                      WHERE status = 'Cancelled';""",
                   single=True)

    def best_selling_report(self):
        sets = self.execute(
                   """WITH Best_Sellers AS
                          (SELECT set_id, SUM(quantity) as sum
                           FROM Customer_Orders as c_o
                           INNER JOIN Customer_Orders_Sets as c_o_s
                           ON c_o.order_id = c_o_s.order_id              
                           WHERE c_o.status NOT IN ('Cart', 'Cancelled', 'Returned')
                           GROUP BY set_id
                           ORDER BY sum desc
                           LIMIT 3)
                      SELECT Sets.set_id, name, sum
                      FROM Sets
                      INNER JOIN Best_Sellers
                      ON Sets.set_id = Best_Sellers.set_id;""")
        bricks = self.execute(
                     """WITH Best_Sellers AS
                            (SELECT brick_id, SUM(quantity) as sum
                             FROM Customer_Orders as c_o
                             INNER JOIN Customer_Orders_Bricks as c_o_b
                             ON c_o.order_id = c_o_b.order_id
                             WHERE c_o.status NOT IN ('Cart', 'Cancelled', 'Returned')
                             GROUP BY brick_id
                             ORDER BY sum desc
                             LIMIT 3)
                        SELECT Bricks.brick_id, description, sum
                        FROM Bricks
                        INNER JOIN Best_Sellers
                        ON Bricks.brick_id = Best_Sellers.brick_id;""")
        return {'sets': sets, 'bricks': bricks}

    def most_returned_report(self):
        sets = self.execute(
            """WITH Most_Returned AS
                   (SELECT set_id, SUM(quantity) as sum
                    FROM Customer_Orders_Returns as c_o_r
                    INNER JOIN Customer_Orders_Sets as c_o_s
                    ON c_o_r.order_id = c_o_s.order_id
                    GROUP BY set_id
                    ORDER BY sum desc
                    LIMIT 3)
               SELECT Sets.set_id, name, sum
               FROM Sets
               INNER JOIN Most_Returned
               ON Sets.set_id = Most_Returned.set_id;""")
        bricks = self.execute(
            """WITH Most_Returned AS
                   (SELECT brick_id, SUM(quantity) as sum
                    FROM Customer_Orders_Returns as c_o_r
                    INNER JOIN Customer_Orders_Bricks as c_o_b
                    ON c_o_r.order_id = c_o_b.order_id
                    GROUP BY brick_id
                    ORDER BY sum desc
                    LIMIT 3)
               SELECT Bricks.brick_id, description, sum
               FROM Bricks
               INNER JOIN Most_Returned
               ON Bricks.brick_id = Most_Returned.brick_id;""")
        return {'sets': sets, 'bricks': bricks}

    
    #All below need to be checked#
        def view_stores(self):
            return self.execute("""SELECT * FROM Stores;""")
        
        def create_store(self, address, manager_id):
            self.execute("""INSERT INTO Stores (address, manager_id) 
                            VALUES (%s, %s);""", address, manager_id, fetch=false)
        
        def disable_store(self, store_id):
            self.execute("""UPDATE Stores SET active = FALSE WHERE store_id = %s;""", store_id, fetch=false)
        
        def view_employees(self):
            return self.execute("""SELECT * FROM Employees;""")
        
        def create_employee(self, name, username, password, store_id):
            self.execute("""INSERT INTO Employees (name, username, password, store_id) 
                            VALUES (%s, %s, %s, %s);""", name, username, password, store_id, fetch=false)
        
        def disable_employee(self, employee_id):
            self.execute("""UPDATE Employees SET active = FALSE WHERE employee_id = %s;""", employee_id, fetch=false)
            
        def generate_sales_report(self):
            sales = self.execute("""SELECT COUNT(sale_id) as num_sales, sum(total_price) as earnings, avg(total_price) as average_price
                                    FROM Store_Sales;""", single=true)
            employee_sales = self.execute("""SELECT name, Store_Sales.employee_id, COUNT(sale_id) as num_sales
                                             FROM Store_Sales, Employees 
                                             WHERE Employees.employee_id = Store_Sales.employee_id 
                                             group by Store_Sales.employee_id;""")
            
            return {'sales' : sales, 'employee_sales' : employee_sales}
        
        def store_returns(self):
            return self.execute("""SELECT COUNT(Store_Sales_Returns.sale_id) as num_returns, SUM(Store_Sales.total_price) as total_price_returned 
                                   FROM Store_Sales_Returns, Store_Sales 
                                   WHERE Store_Sales.sale_id = Store_Sales_Returns.sale_id;""")
        
        def inventory(self, bricks_threshold, sets_threshold):
            bricks = self.execute("""SELECT * FROM Stores_Bricks where inventory < %s;""", bricks_threshold)
            
            sets = self.execute("""SELECT * FROM Stores_Sets where inventory < %s;""", sets_threshold)
            
            return {'sets': sets, 'bricks': bricks}
