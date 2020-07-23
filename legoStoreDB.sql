CREATE database LegoCo


CREATE TABLE Store (
	storeID int NOT NULL,
	address varchar(255) NOT NULL,
	managerID int NOT NULL,
	PRIMARY KEY (storeID)
);

CREATE TABLE Customer (
	customerID int NOT NULL,
	email varchar(255)NOT NULL UNIQUE,
	username varchar(255) NOT NULL UNIQUE,
	password varchar(255) NOT NULL,
	name varchar(255) NOT NULL,
	address varchar(255) NOT NULL,
	storePref int, 
	PRIMARY KEY (customerID),
	FOREIGN KEY (storePref) REFERENCES Store (storeID)
);

CREATE TABLE Payments (
	cardNumber int NOT NULL,	
	customerID int, 
	cardType varchar(255) NOT NULL,
	expDate varchar(255) NOT NULL,
	billingAddress varchar(255) NOT NULL,
	active char NOT NULL,
	PRIMARY KEY (cardNumber),
	FOREIGN KEY (customerID) REFERENCES Customer (customerID)
);

CREATE TABLE onlineOrders (
	orderID int NOT NULL, 
	customerID int,
	cardNumber int, 
	orderTimestamp varchar(255) NOT NULL,
	deliveryTimestamp varchar(255) NOT NULL,
	status varchar(255) NOT NULL,
	totalPrice float NOT NULL,				/*derived*/
	PRIMARY KEY (orderID),
	FOREIGN KEY (customerID) REFERENCES Customer (customerID),
	FOREIGN KEY (cardNumber) REFERENCES Payments (cardNumber)
);

CREATE TABLE Employees (
	employeeID int NOT NULL, 
	name varchar(255) NOT NULL,
	storeID int, 
	PRIMARY KEY (employeeID),
	FOREIGN KEY (storeID) REFERENCES Store (storeID)
);

CREATE TABLE inStoreSales (
	saleID int NOT NULL, 
	storeID int,
	employeeID int,
	saleTimestamp varchar (255) NOT NULL,
	totalPrice float NOT NULL,				/*derived*/
	PRIMARY KEY (saleID),
	FOREIGN KEY (storeID) REFERENCES Store (storeID),
	FOREIGN KEY (employeeID) REFERENCES Employees (employeeID)
);

CREATE TABLE legoSets (
	setID int NOT NULL,
	description varchar (1023),
	price float NOT NULL,					/*derived*/
	PRIMARY KEY (setID)
);

CREATE TABLE Bricks (
	partID int NOT NULL, 
	description varchar (1023),
	price float NOT NULL,
	PRIMARY KEY (partID)
);

CREATE TABLE StoreSets (
	storeID int,
	setID int,
	inventory int NOT NULL,
	availableInventory int NULL,
	FOREIGN KEY (storeID) REFERENCES Store (storeID),
	FOREIGN KEY (setID) REFERENCES legoSets (setID)
);

CREATE TABLE StoreBricks (
	storeID int,
	partID int,
	inventory int NOT NULL,
	availableInventory int NULL,
	FOREIGN KEY (storeID) REFERENCES Store (storeID),
	FOREIGN KEY (partID) REFERENCES Bricks (partID)
);

CREATE TABLE SaleSets (
	saleID int,
	setID int,
	quantity int NOT NULL,
	FOREIGN KEY (saleID) REFERENCES inStoreSales (saleID),
	FOREIGN KEY (setID) REFERENCES legoSets (setID)
);

CREATE TABLE OrderSets (
	orderID int,
	setID int,
	quantity int NOT NULL,
	FOREIGN KEY (orderID) REFERENCES onlineOrders (orderID),
	FOREIGN KEY (setID) REFERENCES legoSets (setID)
);

CREATE TABLE SaleBricks (
	saleID int,
	partID int,
	quantity int NOT NULL,
	FOREIGN KEY (saleID) REFERENCES inStoreSales (saleID),
	FOREIGN KEY (partID) REFERENCES Bricks (partID)
);

CREATE TABLE OrderBricks (
	orderID int,
	partID int,
	quantity int NOT NULL,
	FOREIGN KEY (orderID) REFERENCES onlineOrders (orderID),
	FOREIGN KEY (partID) REFERENCES Bricks (partID)
);

CREATE TABLE Supplier (
	supplierID int NOT NULL,
	name varchar(255) NOT NULL,
	PRIMARY KEY (supplierID)
);

CREATE TABLE StoreOrder (
	storeOrderID int NOT NULL,
	storeID int,
	supplierID int,
	orderTimestamp varchar(255) NOT NULL,
	deliveryTimestamp varchar(255) NOT NULL,
	status varchar(255) NOT NULL,
	PRIMARY KEY (storeOrderID),
	FOREIGN KEY (storeID) REFERENCES Store (storeID),
	FOREIGN KEY (supplierID) REFERENCES Supplier (supplierID)
);

CREATE TABLE StoreOrderBricks (
	storeOrderID int,
	partID int,
	quantity int NOT NULL,
	FOREIGN KEY (storeOrderID) REFERENCES StoreOrder (storeOrderID),
	FOREIGN KEY (partID) REFERENCES Bricks (partID)
);

CREATE TABLE StoreOrderSets (
	storeOrderID int,
	setID int,
	quantity int NOT NULL,
	FOREIGN KEY (storeOrderID) REFERENCES StoreOrder (storeOrderID),
	FOREIGN KEY (setID) REFERENCES legoSets (setID)
);

CREATE TABLE CustomerOrderReturn (
	orderID int,
	reason varchar(255),
	timestamp varchar(255) NOT NULL,
	FOREIGN KEY (orderID) REFERENCES onlineOrders (orderID)	
);

CREATE TABLE StoreSaleReturn (
	orderID int,
	reason varchar(255),
	timestamp varchar(255) NOT NULL,
	FOREIGN KEY (orderID) REFERENCES inStoreSales (saleID)	
);

CREATE TABLE SetBricks (
	setID int,
	brickID int,
	quantity int,
	FOREIGN KEY (setID) REFERENCES legoSets (setID),
	FOREIGN KEY (brickID) REFERENCES Bricks (partID)
);