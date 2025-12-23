use ecommerce;

drop view if exists lowstockalerts;
create view lowstockalerts as
select productid, location, stocklevel, reorderpoint
from inventory
where stocklevel <= reorderpoint;

drop view if exists pendingorders;
create view pendingorders as
select orderid, supplierid, ordereddate, orderstatus
from orders
where orderstatus = 'pending';

drop view if exists supplierinfo;
create view supplierinfo as
select p.name as product_name, p.sku, s.name as supplier_name, ps.unitcost
from products p, suppliers s, productsupplier ps
where p.productid = ps.productid and s.supplierid = ps.supplierid;

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