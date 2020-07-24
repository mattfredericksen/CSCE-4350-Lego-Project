from mysql.connector import connect

credentials = {
    'host': 'localhost',
    'username': 'root',
    'password': 'password',
    'database': 'lego'
}


# class ConnectionManager:
#     def __init__(self):
#         self.host = 'localhost'
#         self.username = 'root'
#         self.password = 'password'
#         self.database = 'lego'
#
#     def __enter__(self):
#         self.connection = connect(self.host, self.username,
#                                   self.password, self.database)
#         self.cursor = self.connection.cursor()
#         return self.cursor()
#
#     def __exit__(self, exc_type, exc_value, exc_traceback):
#         self.cursor.close()
#         self.connection.close()


def execute(query, *args, single=False, procedure=False):
    db = connect(**credentials)
    cursor = db.cursor()
    if procedure:
        cursor.callproc(query, args)
        result = None
    else:
        cursor.execute(query, args)
        if single:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return result


def get_store_preference(customer_id=None):
    return 1
    # return execute("""SELECT store_preference FROM Customers
    #                   WHERE customer_id = %s""",
    #                customer_id, single=True)


def get_sets(set_id=None, description=True):
    if set_id:
        return execute("""SELECT * FROM Sets
                          WHERE set_id = %s;""",
                       set_id, single=True)
    elif description:
        return execute("""SELECT set_id, name, description
                          FROM Sets
                          WHERE active = TRUE;""")
    else:
        return execute("""SELECT set_id, name
                          FROM Sets
                          WHERE active = TRUE;""")


def get_bricks(brick_id=None):
    if brick_id:
        return execute("""SELECT * FROM Bricks
                          WHERE brick_id = %s;""",
                       brick_id, single=True)
    else:
        return execute("""SELECT brick_id, description FROM Bricks 
                          WHERE active = TRUE;""")


def get_set_price(set_id):
    price = execute("""SELECT SUM(quantity * price)
                       FROM Sets_Bricks
                       INNER JOIN Bricks 
                       ON Sets_Bricks.brick_id = Bricks.brick_id
                       WHERE set_id = %s;""",
                    set_id, single=True)
    return round(price[0], 2)


def get_set_count(set_id):
    return execute("""SELECT SUM(quantity) FROM Sets_Bricks
                      WHERE set_id = %s""",
                   set_id, single=True)[0]


def get_set_inventory(store_id, set_id):
    result = execute("""SELECT inventory FROM Stores_Sets
                        WHERE store_id = %s AND set_id = %s""",
                     store_id, set_id, single=True)
    return result[0] if result else 0


def get_brick_inventory(store_id, brick_id):
    result = execute("""SELECT inventory FROM Stores_Bricks
                        WHERE store_id = %s AND brick_id = %s""",
                     store_id, brick_id, single=True)
    return result[0] if result else 0


def modify_cart(user_id, item_id, quantity, set_mode):
    execute('ModifyCartSets' if set_mode else 'ModifyCartBricks',
            user_id, item_id, quantity, procedure=True)

