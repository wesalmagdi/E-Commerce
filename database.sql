
CREATE DATABASE IF NOT EXISTS IMS;
USE IMS;

CREATE TABLE Product (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    SKU VARCHAR(50),
    Description VARCHAR(1000),
    Price FLOAT,
    VATRate FLOAT
);

CREATE TABLE Supplier (
    SupplierID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(11),
    Address VARCHAR(50),
    MinOrderValue FLOAT,
    Currency VARCHAR(10)
);

CREATE TABLE Inventory (
    InventoryID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT NOT NULL,
    StockLevel INT,
    ReorderPoint INT,
    CONSTRAINT ProductID
	FOREIGN KEY (ProductID)REFERENCES Product(ProductID)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);

CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierID INT NOT NULL,
    OrderStatus VARCHAR(50),
    OrderedDate DATE,
    ReceivedDate DATE,
    CONSTRAINT SupplierID
	FOREIGN KEY (SupplierID)REFERENCES Supplier(SupplierID)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);

CREATE TABLE OrderItem (
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT,
    ReceivedQuantity INT DEFAULT 0,
    PRIMARY KEY (OrderID, ProductID),
    CONSTRAINT OrderID 
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
    CONSTRAINT ProductID_OrderItem
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
	ON DELETE RESTRICT
	ON UPDATE CASCADE
);


CREATE TABLE LowStockAlert (
    AlertID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT NOT NULL,
    InventoryID INT NOT NULL,
    AlertDate DATETIME,
    Status VARCHAR(50),
    CONSTRAINT ProductID_LSA
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
    CONSTRAINT InventoryID_LSA
	FOREIGN KEY (InventoryID) REFERENCES Inventory(InventoryID)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);


CREATE TABLE Contract (
    ContractID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierID INT NOT NULL,
    StartDate DATE,
    EndDate DATE,
    CreatedAt DATETIME,
    Penalties VARCHAR(50),
    CONSTRAINT SupplierID_Contract
	FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);

CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50),
    Email VARCHAR(100),
    PasswordHash VARCHAR(200),
    SupplierID INT,
    Role ENUM('Admin','Supplier'),
    CONSTRAINT SupplierID_User
	FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
	ON DELETE SET NULL
	ON UPDATE CASCADE
);

CREATE TABLE ProductSupplier (
    ProductID INT NOT NULL,
    SupplierID INT NOT NULL,
    UnitCost FLOAT,
    LeadTimeDays INT,
    PRIMARY KEY (ProductID, SupplierID),
    CONSTRAINT ProductID_PS
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
    CONSTRAINT SupplierID_PS
	FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);


INSERT INTO Product (Name, SKU, Description, Price, VATRate) VALUES
('Laptop', 'SKU001', '15-inch business laptop', 1200.00, 15),
('Mouse', 'SKU002', 'Wireless mouse', 25.00, 15),
('Keyboard', 'SKU003', 'Mechanical keyboard', 80.00, 15);

INSERT INTO Supplier (Name, Email, Phone, Address, MinOrderValue, Currency) VALUES
('TechSupplier Ltd', 'contact@techsupplier.com', '01012345678', 'Cairo', 500.00, 'EGP'),
('OfficeGear Inc', 'sales@officegear.com', '01198765432', 'Giza', 300.00, 'EGP');

INSERT INTO Inventory (ProductID, StockLevel, ReorderPoint) VALUES
(1, 20, 5),
(2, 100, 20),
(3, 50, 10);

INSERT INTO Orders (SupplierID, OrderStatus, OrderedDate, ReceivedDate) VALUES
(1, 'Pending', '2025-01-10', NULL),
(2, 'Received', '2025-01-01', '2025-01-05');

INSERT INTO OrderItem (OrderID, ProductID, Quantity, ReceivedQuantity) VALUES
(1, 1, 10, 0),
(1, 2, 50, 0),
(2, 3, 20, 20);


INSERT INTO LowStockAlert (ProductID, InventoryID, AlertDate, Status) VALUES
(1, 1, NOW(), 'Active'),
(3, 3, NOW(), 'Resolved');


INSERT INTO Contract (SupplierID, StartDate, EndDate, CreatedAt, Penalties) VALUES
(1, '2025-01-01', '2026-01-01', NOW(), 'Late delivery fee'),
(2, '2025-02-01', '2026-02-01', NOW(), 'Quality penalty');

INSERT INTO User (Username, Email, PasswordHash, SupplierID, Role) VALUES
('admin1', 'admin@ims.com', 'hashed_password_1', NULL, 'Admin'),
('supplier1', 'supplier@techsupplier.com', 'hashed_password_2', 1, 'Supplier');

INSERT INTO ProductSupplier (ProductID, SupplierID, UnitCost, LeadTimeDays) VALUES
(1, 1, 1000.00, 7),
(2, 1, 15.00, 5),
(3, 2, 60.00, 10);
