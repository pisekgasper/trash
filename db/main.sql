/* pSQL script that creates a "sloveniantrash" data base */

CREATE TABLE sender (
    id bigint PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE receiver (
    id bigint PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE transporter (
    id bigint PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE evl (
    evl_id SERIAL PRIMARY KEY,
    sender_id bigint NOT NULL,
    receiver_id bigint NOT NULL,
    transporter_id bigint NOT NULL,
    sender_status varchar(100),
    receiver_status varchar(100),
    dat_oddaje date NOT NULL,
    kraj_oddaje text,
    lokacija_oddaje text,
    parcele_oddaja text,
    dat_prejem_zav date,
    kraj_prejema text,
    lokacija_prejema text,
    parcele_prejem text,
    wol_num varchar(10) NOT NULL,
    naziv_odpadka text,
    nevaren boolean,
    kol_kg decimal,
    emb_shema text,
    svece boolean,
    dejavnost_nast text,
    izvor_odpadka text,
    predviden_postopek text,
    evl_status varchar(100),
    ind_sprejeto boolean
);

CREATE TABLE obcine (
    id bigint PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE naselja (
    id bigint PRIMARY KEY,
    name text NOT NULL,
    o_id bigint NOT NULL
);