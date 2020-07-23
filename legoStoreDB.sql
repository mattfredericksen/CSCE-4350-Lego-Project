-- CREATE database LegoCo;


CREATE TABLE Stores (
	store_id INT NOT NULL AUTO_INCREMENT,
	address VARCHAR(256) NOT NULL,
	manager_id INT,
    active BOOLEAN NOT NULL DEFAULT TRUE,
	  /* because we don't want to lose a
	     store's history if the store is closed */
    PRIMARY KEY (store_id)
);

CREATE TABLE Employees (
    employee_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    store_id INT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (store_id) REFERENCES Stores (store_id)
);

ALTER TABLE Stores
ADD FOREIGN KEY (manager_id) REFERENCES Employees (employee_id);

CREATE TABLE Bricks (
	brick_id INT NOT NULL AUTO_INCREMENT,
	description VARCHAR(128) NOT NULL,
    price FLOAT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
	PRIMARY KEY (brick_id),
    CHECK (price > 0.0)
);

-- Attempt to prevent Bricks & Sets IDs from overlapping
ALTER TABLE Bricks AUTO_INCREMENT=10000;

CREATE TABLE Sets (
	set_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL,
	description VARCHAR(512) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
	PRIMARY KEY (set_id)
);

ALTER TABLE Sets AUTO_INCREMENT=1000;

CREATE TABLE Sets_Bricks (
	set_id INT NOT NULL,
	brick_id INT NOT NULL,
	quantity INT NOT NULL,
	FOREIGN KEY (set_id) REFERENCES Sets (set_id),
	FOREIGN KEY (brick_id) REFERENCES Bricks (brick_id),
    PRIMARY KEY (set_id, brick_id),
    CHECK (quantity > 0)
);

CREATE TABLE Stores_Bricks (
	store_id INT NOT NULL,
	brick_id INT NOT NULL,
	inventory INT NOT NULL,
	FOREIGN KEY (store_id) REFERENCES Stores (store_id),
	FOREIGN KEY (brick_id) REFERENCES Bricks (brick_id)
    /* no checks here because we don't want to
       cause issues if inventory goes negative */
);

CREATE TABLE Stores_Sets (
	store_id INT NOT NULL,
	set_id INT NOT NULL,
	inventory INT NOT NULL,
	FOREIGN KEY (store_id) REFERENCES Stores (store_id),
	FOREIGN KEY (set_id) REFERENCES Sets (set_id)
    /* no checks here because we don't want to
       cause issues if inventory goes negative */
);

CREATE TABLE Customers (
	customer_id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(128) NOT NULL UNIQUE,
	username VARCHAR(128) NOT NULL UNIQUE,
	password VARCHAR(128) NOT NULL,
	name VARCHAR(128) NOT NULL,
	address VARCHAR(256) NOT NULL,
	store_preference INT NOT NULL,
    PRIMARY KEY (customer_id),
	FOREIGN KEY (store_preference) REFERENCES Stores (store_id)
);

CREATE TABLE Payments (
	customer_id INT NOT NULL,
	card_number CHAR(16) NOT NULL,
	exp_date DATE NOT NULL,
	billing_address VARCHAR(256) NOT NULL,
	active BOOLEAN NOT NULL DEFAULT TRUE,
		/* because this data should be retained in case a customer
           removes this payment method and then cancels an order,
           so we can still perform the refund */
	FOREIGN KEY (customer_id) REFERENCES Customers (customer_id),
	PRIMARY KEY (customer_id, card_number)
);

CREATE TABLE Customer_Orders (
	order_id INT NOT NULL AUTO_INCREMENT,
	customer_id INT NOT NULL,
	card_number CHAR(16) NOT NULL,
    store_id INT NOT NULL,
	order_timestamp TIMESTAMP,
	delivery_timestamp TIMESTAMP,
	status VARCHAR(16) NOT NULL,
	total_price FLOAT NOT NULL,
	PRIMARY KEY (order_id),
	FOREIGN KEY (customer_id, card_number)
        REFERENCES Payments (customer_id, card_number),
    CHECK (delivery_timestamp IS NULL OR
           delivery_timestamp > order_timestamp),
    CHECK (status IN ('Processing', 'Shipping',
                      'Delivered', 'Cancelled',
                      'Returned', 'Cart')),
    CHECK (total_price > 0.0)
);

CREATE TABLE Customer_Order_Returns (
	order_id INT NOT NULL,
	reason VARCHAR(256),
	return_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
	FOREIGN KEY (order_id) REFERENCES Customer_Orders (order_id),
    PRIMARY KEY (order_id)
);

CREATE TABLE Customer_Order_Bricks (
	order_id INT NOT NULL,
	brick_id INT NOT NULL,
	quantity INT NOT NULL,
	FOREIGN KEY (order_id) REFERENCES Customer_Orders (order_id),
	FOREIGN KEY (brick_id) REFERENCES Bricks (brick_id),
    PRIMARY KEY (order_id, brick_id),
    CHECK (quantity > 0)
);

CREATE TABLE Customer_Order_Sets (
	order_id INT NOT NULL,
	set_id INT NOT NULL,
	quantity INT NOT NULL,
	FOREIGN KEY (order_id) REFERENCES Customer_Orders (order_id),
	FOREIGN KEY (set_id) REFERENCES Sets (set_id),
    PRIMARY KEY (order_id, set_id),
    CHECK (quantity > 0)
);

CREATE TABLE Store_Sales (
	sale_id INT NOT NULL AUTO_INCREMENT,
	store_id INT NOT NULL,
	employee_id INT NOT NULL,
	sale_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
	total_price FLOAT NOT NULL,
    credit_card CHAR(16),
	PRIMARY KEY (sale_id),
	FOREIGN KEY (store_id) REFERENCES Stores (store_id),
	FOREIGN KEY (employee_id) REFERENCES Employees (employee_id),
    CHECK (total_price > 0.0)
);

CREATE TABLE Store_Sales_Returns (
	sale_id INT NOT NULL,
	reason VARCHAR(256),
	return_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
	FOREIGN KEY (sale_id) REFERENCES Store_Sales (sale_id),
    PRIMARY KEY (sale_id)
);

CREATE TABLE Store_Sales_Bricks (
	sale_id INT NOT NULL,
	brick_id INT NOT NULL,
	quantity INT NOT NULL,
	FOREIGN KEY (sale_id) REFERENCES Store_Sales (sale_id),
	FOREIGN KEY (brick_id) REFERENCES Bricks (brick_id),
    PRIMARY KEY (sale_id, brick_id),
    CHECK (quantity > 0)
);

CREATE TABLE Store_Sales_Sets (
	sale_id INT NOT NULL,
	set_id INT NOT NULL,
	quantity INT NOT NULL,
	FOREIGN KEY (sale_id) REFERENCES Store_Sales (sale_id),
	FOREIGN KEY (set_id) REFERENCES Sets (set_id),
    PRIMARY KEY (sale_id, set_id),
    CHECK (quantity > 0)
);

CREATE TABLE Suppliers (
	supplier_id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(128) NOT NULL,
	PRIMARY KEY (supplier_id)
);

CREATE TABLE Store_Orders (
	order_id INT NOT NULL AUTO_INCREMENT,
	store_id INT NOT NULL,
	supplier_id INT NOT NULL,
	order_timestamp TIMESTAMP,
	delivery_timestamp TIMESTAMP,
	status VARCHAR(16) NOT NULL,
	PRIMARY KEY (order_id),
	FOREIGN KEY (store_id) REFERENCES Stores (store_id),
	FOREIGN KEY (supplier_id) REFERENCES Suppliers (supplier_id),
    CHECK (status IN ('Ordered', 'Delivered', 'Cancelled'))
);

CREATE TABLE Store_Orders_Bricks (
	order_id INT NOT NULL,
	brick_id INT NOT NULL,
	quantity INT NOT NULL,
	FOREIGN KEY (order_id) REFERENCES Store_Orders (order_id),
	FOREIGN KEY (brick_id) REFERENCES Bricks (brick_id),
    PRIMARY KEY (order_id, brick_id),
    CHECK (quantity > 0)
);

CREATE TABLE Store_Orders_Sets (
	order_id INT NOT NULL,
	set_id INT NOT NULL,
	quantity INT NOT NULL,
	FOREIGN KEY (order_id) REFERENCES Store_Orders (order_id),
	FOREIGN KEY (set_id) REFERENCES Sets (set_id),
    CHECK (quantity > 0)
);
