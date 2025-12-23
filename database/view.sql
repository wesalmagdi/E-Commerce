create view lowStockAlerts as
select ProductID, Location, StockLevel, ReorderPoint
from Inventory
where StockLevel <= ReorderPoint;

create view PendingOrders as
select OrderID, SupplierID, OrderedDate, OrderStatus
from Orders
where OrderStatus = 'Pending';

create view SupplierInfo as
select P.Name as ProductName, P.SKU, S.Name as SupplierName, PS.UnitCost
from Product P, Supplier S, ProductSupplier PS
where P.ProductID = PS.ProductID and S.SupplierID = PS.SupplierID;

create view AdminInventoryOversight as
select ProductID, Location, StockLevel
from Inventory
where StockLevel >= 0
with check option;

alter view AdminInventoryOversight as
select ProductID, Location, StockLevel, ReorderPoint
from Inventory
where StockLevel >= 0;

