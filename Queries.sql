-- An Admin sets the "Reorder Point" for a specific product at a specific location to define when an alert should be triggered.
-- Configuration Function

set @newpoint = 15;
set @targetid = 1;

update inventory 
set reorderpoint = @newpoint 
where inventoryid = @targetid;

-- When the system (or an admin manually) detects that StockLevel is less than or equal to the ReorderPoint, a record is inserted into the LowStockAlert table
-- Notification Function 
set @prodid = 1;
set @invid = 1;
set @alertstatus = 'active';

insert into lowstockalert (productid, inventoryid, alertdate, status)
values (@prodid, @invid, now(), @alertstatus);


-- contract removal
set @cid = 1;
delete from contract where contractid = @cid;

-- search user by role 
set @roleinput = 'admin';
select username, email from user where role = @roleinput;

-- Mark Order as Received (Update)
-- When a delivery arrives, you need to update the status and the received date simultaneously.

set @target_order = 1;
set @receive_date = curdate();

update orders 
set orderstatus = 'received', receiveddate = @receive_date 
where orderid = @target_order; 