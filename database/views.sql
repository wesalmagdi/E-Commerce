use ecommerce;

drop view if exists lowstockalerts;
create view lowstockalerts as
select productid, stocklevel, reorderpoint
from inventory
where stocklevel <= reorderpoint;

drop view if exists pendingorders;
create view pendingorders as
select orderid, supplierid, ordereddate, orderstatus
from orders
where orderstatus = 'pending';

drop view if exists supplierinfo;
CREATE OR REPLACE VIEW supplierinfo AS 
SELECT 
    p.name AS product_name, 
    p.sku, 
    s.name AS supplier_name, 
    ps.unitcost AS base_cost,
    ps.unitcost * 1.14 AS cost_with_vat,
    ps.leadtimedays
FROM product p
JOIN productsupplier ps ON p.productid = ps.productid
JOIN supplier s ON s.supplierid = ps.supplierid;

drop view if exists admininventoryoversight;
create view admininventoryoversight as
select productid, location, stocklevel
from inventory
where stocklevel >= 0
with check option;

alter view admininventoryoversight as
select productid, location, stocklevel, reorderpoint
from inventory
where stocklevel >= 0;



drop view if exists supplierperformance;
create view supplierperformance as

select s.name as suppliername, p.name as productname, ps.leadtimedays, 'fast' as shippingspeed
from supplier s
join productsupplier ps on s.supplierid = ps.supplierid
join product p on ps.productid = p.productid
where ps.leadtimedays <= 5
union all
select s.name, p.name, ps.leadtimedays, 'average'
from supplier s
join productsupplier ps on s.supplierid = ps.supplierid
join product p on ps.productid = p.productid
where ps.leadtimedays > 5 and ps.leadtimedays <= 10
union all
select s.name, p.name, ps.leadtimedays, 'slow'
from supplier s
join productsupplier ps on s.supplierid = ps.supplierid
join product p on ps.productid = p.productid
where ps.leadtimedays > 10;

CREATE OR REPLACE VIEW product_stock AS
SELECT 
    p.productid,
    p.name AS product_name, 
    s.name AS supplier_name,
    ps.unitcost AS supplier_price, 
    (p.price * 1.14) AS cost_with_vat,
    COALESCE(i.stocklevel, 0) AS stocklevel,
    COALESCE(i.reorderpoint, 10) AS reorderpoint,
    ps.leadtimedays
FROM product p
JOIN productsupplier ps ON p.productid = ps.productid
JOIN supplier s ON ps.supplierid = s.supplierid
LEFT JOIN inventory i ON p.productid = i.productid;