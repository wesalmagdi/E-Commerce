DROP DATABASE IF EXISTS ecommerce;
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

create table product (
    productid int auto_increment primary key,
    name varchar(100),
    sku varchar(50),
    description varchar(1000),
    price float,
    vatrate float
);

create table supplier (
    supplierid int auto_increment primary key,
    name varchar(100),
    email varchar(100),
    phone varchar(11),
    address varchar(50),
    minordervalue float,
    currency varchar(10)
);

create table inventory (
    inventoryid int auto_increment primary key,
    productid int not null,
    stocklevel int,
    reorderpoint int,
    constraint productid
foreign key (productid)references product(productid)
on delete cascade
on update cascade
);

create table orders(
    orderid int auto_increment primary key,
    supplierid int not null,
    orderstatus varchar(50),
    ordereddate date,
    receiveddate date,
    constraint supplierid
foreign key (supplierid)references supplier(supplierid)
on delete restrict
on update cascade
);

create table orderitem (
    orderid int not null,
    productid int not null,
    quantity int,
    receivedquantity int default 0,
    primary key (orderid, productid),
    constraint orderid
    foreign key (orderid) references orders(orderid)
on delete cascade
on update cascade,
    constraint productid_orderitem
foreign key (productid) references product(productid)
on delete restrict
on update cascade
);


create table lowstockalert (
    alertid int auto_increment primary key,
    productid int not null,
    inventoryid int not null,
    alertdate datetime,
    status varchar(50),
    constraint productid_lsa
foreign key (productid) references product(productid)
on delete cascade
on update cascade,
    constraint inventoryid_lsa
foreign key (inventoryid) references inventory(inventoryid)
on delete cascade
on update cascade
);


create table contract (
    contractid int auto_increment primary key,
    supplierid int not null,
    startdate date,
    enddate date,
    createdat datetime,
    penalties varchar(50),
    constraint supplierid_contract
foreign key (supplierid) references supplier(supplierid)
on delete cascade
on update cascade
);

create table user(
    userid int auto_increment primary key,
    username varchar(50),
    email varchar(100),
    passwordhash varchar(200),
    supplierid int,
    role enum('admin','supplier'),
    constraint supplierid_user
foreign key (supplierid) references supplier(supplierid)
on delete set null
on update cascade
);

create table productsupplier (
    productid int not null,
    supplierid int not null,
    unitcost float,
    leadtimedays int,
    primary key (productid, supplierid),
    constraint productid_ps
foreign key (productid) references product(productid)
on delete cascade
on update cascade,
    constraint supplierid_ps
foreign key (supplierid) references supplier(supplierid)
on delete cascade
on update cascade
);
