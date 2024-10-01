create table warehouses
(
    ware_id      integer generated always as identity,
    ware_name    varchar(50)  not null,
    ware_street  varchar(100) not null,
    ware_city    varchar(50)  not null,
    ware_country varchar(50)  not null,
    ware_zipcode varchar(20)  not null,
    ware_budget  double precision,
    primary key (ware_id),
    constraint warehouse_unique
        unique (ware_name, ware_street, ware_city, ware_country)
);

create table suppliers
(
    supplier_id      integer generated always as identity,
    supplier_name    varchar(50)  not null,
    supplier_street  varchar(100) not null,
    supplier_city    varchar(50)  not null,
    supplier_country varchar(50)  not null,
    supplier_zipcode varchar(20)  not null,
    primary key (supplier_id),
    constraint suppliers_unique
        unique (supplier_name, supplier_street, supplier_city, supplier_country)
);

create table parts
(
    part_id    integer generated always as identity,
    part_name  varchar(50)      not null,
    part_price double precision not null,
    part_type  varchar(50)      not null,
    primary key (part_id),
    constraint part_unique
        unique (part_name, part_type)
);

create table racks
(
    rack_id       integer generated always as identity,
    rack_capacity integer not null,
    rack_stock    integer not null,
    part_id       integer not null,
    ware_id       integer not null,
    constraint rack_unique
        unique (part_id, ware_id),
    constraint fk_rack_ware
        foreign key (ware_id) references warehouses,
    constraint fk_rack_part
        foreign key (part_id) references parts,
    constraint capacity_check
        check (rack_capacity >= rack_stock)
);

create table transactions
(
    trans_id   integer generated always as identity,
    trans_type varchar(50)               not null,
    trans_date date default CURRENT_DATE not null,
    user_id    integer                   not null,
    ware_id    integer                   not null,
    rack_id    integer                   not null,
    trans_time time default CURRENT_TIMESTAMP,
    primary key (trans_id),
    constraint fk_trans_ware
        foreign key (ware_id) references warehouses
);

create table trans_incoming
(
    incoming_id    integer generated always as identity,
    trans_id       integer not null,
    trans_qty      integer not null,
    trans_part     integer not null,
    trans_supplier integer not null,
    primary key (incoming_id),
    constraint fk_incoming_trans
        foreign key (trans_id) references transactions,
    constraint fk_incoming_part
        foreign key (trans_part) references parts,
    constraint fk_incoming_supp
        foreign key (trans_supplier) references suppliers
);

create table trans_outgoing
(
    outgoing_id     integer generated always as identity,
    trans_id        integer not null,
    trans_qty       integer not null,
    trans_part      integer not null,
    trans_recipient integer not null,
    primary key (outgoing_id),
    constraint fk_outgoing_trans
        foreign key (trans_id) references transactions,
    constraint fk_outgoing_part
        foreign key (trans_part) references parts,
    constraint fk_outgoing_supp
        foreign key (trans_recipient) references suppliers
);

create table trans_exchange
(
    exchange_id         integer generated always as identity,
    trans_id            integer not null,
    trans_qty           integer not null,
    trans_part          integer not null,
    trans_ware_supplier integer not null,
    supplier_user_id    integer not null,
    primary key (exchange_id),
    constraint fk_exchange_trans
        foreign key (trans_id) references transactions,
    constraint fk_exchange_part
        foreign key (trans_part) references parts,
    constraint fk_exchange_origin
        foreign key (trans_ware_supplier) references warehouses
);

create table supplies
(
    supplies_id integer generated always as identity,
    supplier_id integer not null,
    part_id     integer not null,
    stock       integer not null,
    primary key (supplies_id),
    constraint supplies_unique
        unique (supplier_id, part_id),
    constraint fk_supplies_supp
        foreign key (supplier_id) references suppliers,
    constraint fk_supplies_part
        foreign key (part_id) references parts
);

create table users
(
    user_id    integer generated always as identity,
    user_name  varchar(50)  not null,
    user_lname varchar(50)  not null,
    user_email varchar(100) not null,
    user_pass  varchar(50)  not null,
    ware_id    integer      not null,
    primary key (user_id),
    unique (user_email),
    constraint fk_user_warehouse
        foreign key (ware_id) references warehouses
);

