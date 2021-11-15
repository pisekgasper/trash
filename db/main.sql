/* pSQL script that creates a "sloveniantrash" data base */

CREATE TABLE sender (
    id integer PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE receiver (
    id integer PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE transporter (
    id integer PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE evl (
    evl_id integer PRIMARY KEY,
    sender_id integer NOT NULL,
    receiver_id integer NOT NULL,
    transporter_id integer NOT NULL,
    sender_status varchar(100),
    receiver_status varchar(100),
    dat_oddaje date NOT NULL,
    kraj_oddaje text,
    lokacija_oddaje text,
    parcele_oddaja text,
    dat_prejem_zav date, -- v primeru zavrnitve odpadkov
    kraj_prejema text,
    lokacija_prejema text,
    parcele_prejem text,
    wol_num varchar(10) NOT NULL, -- glede na to kodo lahko pogledamo tip odpadkov
    naziv_odpadka text,
    nevaren boolean,
    kol_kg integer, -- kolicina odpadkov v kg
    emb_shema text,
    svece boolean,
    dejavnost_nast text,
    izvor_odpadka text,
    predviden_postopek text,
    evl_status varchar(100),
    ind_sprejeto boolean
);