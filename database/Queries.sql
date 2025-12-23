insert into product (name, sku, description, price, vatrate) values
('laptop', 'sku001', '15-inch business laptop', 1200.00, 15),
('mouse', 'sku002', 'wireless mouse', 25.00, 15),
('keyboard', 'sku003', 'mechanical keyboard', 80.00, 15);

insert into supplier (name, email, phone, address, minordervalue, currency) values
('techsupplier ltd', 'contact@techsupplier.com', '01012345678', 'cairo', 500.00, 'egp'),
('officegear inc', 'sales@officegear.com', '01198765432', 'giza', 300.00, 'egp');

insert into inventory (productid, stocklevel, reorderpoint) values
(1, 20, 5),
(2, 100, 20),
(3, 50, 10);

insert into orders (supplierid, orderstatus, ordereddate, receiveddate) values
(1, 'pending', '2025-01-10', null),
(2, 'received', '2025-01-01', '2025-01-05');

insert into orderitem (orderid, productid, quantity, receivedquantity) values
(1, 1, 10, 0),
(1, 2, 50, 0),
(2, 3, 20, 20);


insert into lowstockalert (productid, inventoryid, alertdate, status) values
(1, 1, now(), 'active'),
(3, 3, now(), 'resolved');


insert into contract (supplierid, startdate, enddate, createdat, penalties) values
(1, '2025-01-01', '2026-01-01', now(), 'late delivery fee'),
(2, '2025-02-01', '2026-02-01', now(), 'quality penalty');

insert into user (username, email, passwordhash, supplierid, role) values
('admin1', 'admin@ims.com', 'hashed_password_1', null, 'admin'),
('supplier1', 'supplier@techsupplier.com', 'hashed_password_2', 1, 'supplier');

insert into productsupplier (productid, supplierid, unitcost, leadtimedays) values
(1, 1, 1000.00, 7),
(2, 1, 15.00, 5),
(3, 2, 60.00, 10);

select * from contract 
where supplierid = 1 and enddate >= curdate();