-- view 1: low stock emergency report
-- This combines product info, current stock, and the supplier's contact info so the admin can take action immediately.

create view view_low_stock_report as
select 
    p.name as product_name,
    p.sku,
    i.stocklevel,
    i.reorderpoint,
    s.name as supplier_name,
    s.phone as supplier_phone
from product p
join inventory i on p.productid = i.productid
join productsupplier ps on p.productid = ps.productid
join supplier s on ps.supplierid = s.supplierid
where i.stocklevel <= i.reorderpoint;

-- view 2: supplier performance (lead times)
-- This helps the admin see which suppliers deliver the fastest.


create view view_supplier_lead_times as
select 
    s.name as supplier_name,
    p.name as product_name,
    ps.unitcost,
    ps.leadtimedays
from supplier s
join productsupplier ps on s.supplierid = ps.supplierid
join product p on ps.productid = p.productid;

-- This view identifies which contracts are about to expire, helping the admin manage renewals.
create view view_contract_status as
select 
    s.name as supplier_name,
    c.startdate,
    c.enddate,
    datediff(c.enddate, curdate()) as days_until_expiry,
    case 
        when c.enddate < curdate() then 'expired'
        else 'active'
    end as contract_status
from supplier s
join contract c on s.supplierid = c.supplierid;


-- A dedicated view for the "purchasing" screen in your GUI to show what items are currently being waited on.

create view view_pending_orders as
select 
    o.orderid,
    s.name as supplier_name,
    p.name as product_name,
    oi.quantity,
    o.ordereddate
from orders o
join supplier s on o.supplierid = s.supplierid
join orderitem oi on o.orderid = oi.orderid
join product p on oi.productid = p.productid
where o.orderstatus = 'pending'; 

-- financial report: total value of stock on hand, This report tells the admin exactly how much money is tied up in stock. It joins the product and inventory tables and calculates a new column for total value.
create view view_inventory_valuation as
select 
    p.productid,
    p.name as product_name,
    p.sku,
    i.stocklevel,
    p.price as unit_price,
    (i.stocklevel * p.price) as total_inventory_value,
    (i.stocklevel * p.price * (p.vatrate / 100)) as estimated_vat
from product p
join inventory i on p.productid = i.productid;

-- management report: supplier sourcing details
-- It helps the user decide which supplier is the most reliable based on how long they take to deliver products (leadtimedays)
create view view_supplier_performance as
select 
    s.name as supplier_name,
    s.email as contact_email,
    p.name as product_name,
    ps.unitcost,
    ps.leadtimedays as delivery_days,
    case 
        when ps.leadtimedays <= 5 then 'fast'
        when ps.leadtimedays <= 10 then 'average'
        else 'slow'
    end as shipping_speed
from supplier s
join productsupplier ps on s.supplierid = ps.supplierid
join product p on ps.productid = p.productid;