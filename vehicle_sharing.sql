create table Station
(
    name     TEXT
        constraint Station_pk
            primary key,
    street   TEXT,
    postcode TEXT,
    city     TEXT,
    constraint address
        unique (street, postcode, city)
);


create Table VehicleClass
(
    vcid   text
        constraint VehicleClass_pk primary key,
    vcame  text
        constraint VehicleClass_pk2 unique,
    length real,
    width  real,
    height real
);

create table Customer
(
    cid       TEXT
        constraint Customer_pk
            primary key,
    firstName TEXT,
    lastName  TEXT,
    vcid      TEXT
        constraint Customer_VehicleClass_vcid_fk
            references VehicleClass
            on update cascade on delete restrict,
    constraint name
        unique (firstName, lastName)
);

create table Vehicle
(
    vcid            TEXT
        constraint Vehicle_VehicleClass_vcid_fk
            references VehicleClass
            on update cascade on delete restrict,
    sname           TEXT
        constraint Vehicle_Station_name_fk
            references Station,
    num             integer,
    last_check_date TEXT,
    type            integer,
    constraint Vehicle_pk
        primary key (vcid, sname, num)
);

create table Car
(
    vcid      text,
    sname     text,
    num       integer,
    plate_num integer,
    constraint Car_Vehicle_vcid_sname_num_fk
        foreign key (vcid, sname, num) references Vehicle
            on update cascade on delete cascade,
    constraint Car_pk primary key (vcid, sname, num)

);


create TABLE Reservation
(
    vcid          text,
    sname         text,
    num           integer,
    cid           TEXT,
    startDateTime text,
    endDateTime   text,
    status        int,
    constraint Reservation_pk primary key (vcid, sname, num, cid, startDateTime),
    constraint Reservation_Customer_fk foreign key (cid) references Customer on delete cascade on delete cascade,
    constraint Reservation_Vehicle_fk foreign key (vcid, sname, num) references Vehicle on delete restrict on update restrict
);

create TABLE FinishedReservation
(
    vcid          text,
    sname         text,
    num           integer,
    cid           TEXT,
    startDateTime text,
    distance      real,
    cost          real,
    constraint FinishedReservation_pk primary key (vcid, sname, num, cid, startDateTime),
    constraint FinishedReservation_Reservation_fk foreign key (vcid, sname, num, cid, startDateTime) references Customer on delete cascade on delete cascade
);








