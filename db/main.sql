/* pSQL script that creates a "sloveniantrash" data base */


CREATE DATABASE "sloveniantrash"
  WITH OWNER "postgres"
  ENCODING 'UTF8'
  TEMPLATE template0
  LC_COLLATE = 'sl_SI.UTF-8'
  LC_CTYPE = 'sl_SI.UTF-8';

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
    ind_sprejeto boolean,
    obcina_oddaja bigint,
    obcina_prejem bigint
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

CREATE TABLE ulice (
    id bigint PRIMARY KEY,
    name text NOT NULL,
    o_id bigint NOT NULL
);


UPDATE evl e1 SET obcina_oddaja = (SELECT o.id from evl e, obcine o, ulice u, naselja n WHERE LOWER(e.lokacija_oddaje) LIKE LOWER(u.name) || '%' AND LOWER(e.lokacija_oddaje) LIKE '%' || LOWER(n.name) AND u.o_id = o.id AND n.o_id = o.id AND e.evl_id = e1.evl_id LIMIT 1);

/* poizvedba za tezo po mesecih v nekem letu */
SELECT DATE_PART('month',dat_oddaje) AS  mesec,
       sum(kol_kg) AS teza
FROM evl
WHERE DATE_PART('year',dat_oddaje) = '2021'
GROUP BY mesec;

/* poizvedba za oddane odpadke posiljatelja */
SELECT sum(kol_kg) as izvozi 
FROM evl
WHERE sender_id = 5472261000;

/* poizvedba za sprejete odpadke sprejemnika */
SELECT sum(kol_kg) as uvozi 
FROM evl
WHERE receiver_id = 5005647000;

/* poizvedba za prevozene odpadke transporterja */
SELECT sum(kol_kg) as prevozi 
FROM evl
WHERE transporter_id = 1810065000;

/* poizvedba za st. evl po obcinah */
SELECT o.name, e.obcina_oddaja, count(e.evl_id) AS st_evl 
FROM evl e inner join obcine o ON o.id = e.obcina_oddaja 
WHERE obcina_oddaja IS NOT NULL 
GROUP BY e.obcina_oddaja, o.name 
ORDER BY st_evl DESC;

/* poizvedba po kolicini v letu 20XY groupano po obcinah */
/* IZVOZ 2021 */
    SELECT e.obcina_oddaja AS Obcina, SUM(e.kol_kg) as Kolicina 
    FROM evl e 
    WHERE DATE_PART('year', e.dat_oddaje) = '2021' 
    GROUP BY e.obcina_oddaja;
/* UVOZ */
    SELECT e.obcina_prejem AS Obcina, SUM(e.kol_kg) as Kolicina 
    FROM evl e 
    WHERE DATE_PART('year', e.dat_oddaje) = '2021' 
    GROUP BY e.obcina_oddaja;