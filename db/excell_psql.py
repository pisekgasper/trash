import pandas as pd
import numpy as np
from csv import DictReader
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
from datetime import datetime
from time import gmtime, strftime

register_adapter(np.int64, AsIs)

# connect to db
path = "C:/Users/Nik/Documents/fri/3. letnik/MT/Modul1-podatki/EVL2021.xlsx"
sheet = "Export Worksheet"
dbname = 'sloveniantrash'
user = 'postgres'
password = 'admin'
conn = psycopg2.connect(dbname=dbname, user=user, password=password)
print("[%s] CONNECTED" % strftime("%H:%M:%S", gmtime()))

# set up a cursor to work with db
cur = conn.cursor()

print("[%s] READING FILE" % strftime("%H:%M:%S", gmtime()))
# select all from file
df = pd.read_excel(path, sheet_name=sheet, engine='openpyxl')
df.fillna('', inplace=True)
print("[%s] DONE READING" % strftime("%H:%M:%S", gmtime()))

print("[%s] INSERTING ALL" % strftime("%H:%M:%S", gmtime()))

index = df.index
rows = len(index)

# select data from data and insert into db
for i in range(rows):
    sender_id = df.loc[i, "sender_id"]
    receiver_id = df.loc[i, "receiver_id"]
    transporter_id = df.loc[i, "transporter_id"]
    sender_status = df.loc[i, "sender_status"]
    receiver_status = df.loc[i, "receiver_status"]
    dat_oddaje = df.loc[i, "dat_oddaje"]
    kraj_oddaje = df.loc[i, "kraj_oddaje"]
    lokacija_oddaje = df.loc[i, "lokacija_oddaje"]
    parcele_oddaja = df.loc[i, "parcele_oddaja"]
    dat_prejem_zav = df.loc[i, "dat_prejem_zav"]
    kraj_prejema = df.loc[i, "kraj_prejema"]
    lokacija_prejema = df.loc[i, "lokacija_prejema"]
    parcele_prejem = df.loc[i, "parcele_prejem"]
    wol_num = df.loc[i, "wol_num"]
    naziv_odpadka = df.loc[i, "naziv_odpadka"]
    nevaren = df.loc[i, "nevaren"]
    kol_kg = df.loc[i, "kol_kg"]
    emb_shema = df.loc[i, "emb_shema"]
    svece = df.loc[i, "svece"]
    dejavnost_nast = df.loc[i, "dejavnost_nast"]
    izvor_odpadka = df.loc[i, "izvor_odpadka"]
    predviden_postopek = df.loc[i, "predviden_postopek"]
    evl_status = df.loc[i, "evl_status"]
    ind_sprejeto = df.loc[i, "ind_sprejeto"]

    sender_id = int(sender_id)
    receiver_id = int(receiver_id)
    transporter_id = int(transporter_id)

    if sender_status == '':
        sender_status = None
    
    if receiver_status == '':
        receiver_status = None

    dto = datetime.strptime(dat_oddaje, '%d.%m.%y')
    dat_oddaje = dto.strftime('%Y-%m-%d')

    if kraj_oddaje == '':
        kraj_oddaje = None

    if kraj_oddaje == '':
        kraj_oddaje = None

    if parcele_oddaja == '':
        parcele_oddaja = None

    if dat_prejem_zav != '':
        dto = datetime.strptime(dat_prejem_zav, '%d.%m.%y')
        dat_prejem_zav = dto.strftime('%Y-%m-%d')
    else:
        dat_prejem_zav = None

    if kraj_prejema == '':
        kraj_prejema = None

    if lokacija_prejema == '':
        lokacija_prejema = None

    if parcele_prejem == '':
        parcele_prejem = None
    
    if naziv_odpadka == '':
        naziv_odpadka = None

    if nevaren == '*':
        nevaren = True
    else:
        nevaren = False

    if kol_kg != '': 
        kol_kg = float(kol_kg)
    else:
        kol_kg = None

    if emb_shema == '':
        emb_shema = None

    if svece == 'D':
        svece = True
    else:
        svece = False

    if dejavnost_nast == '':
        dejavnost_nast = None

    if izvor_odpadka == '':
        izvor_odpadka = None

    if predviden_postopek == '':
        predviden_postopek = None

    if evl_status == '':
        evl_status = None
    
    if ind_sprejeto == 'D':
        ind_sprejeto = True
    else:
        ind_sprejeto = False

    cur.execute("INSERT INTO sender (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;", [sender_id, df.loc[i, "s_name"]])
    cur.execute("INSERT INTO receiver (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;", [receiver_id, df.loc[i, "r_name"]])
    cur.execute("INSERT INTO transporter (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;", [transporter_id, df.loc[i, "t_name"]])

    cur.execute("INSERT INTO evl (sender_id, receiver_id, transporter_id, sender_status, receiver_status, dat_oddaje, kraj_oddaje, lokacija_oddaje, parcele_oddaja, dat_prejem_zav, kraj_prejema, lokacija_prejema, parcele_prejem, wol_num, naziv_odpadka, nevaren, kol_kg, emb_shema, svece, dejavnost_nast, izvor_odpadka, predviden_postopek, evl_status, ind_sprejeto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", [sender_id, receiver_id, transporter_id, sender_status, receiver_status, dat_oddaje, kraj_oddaje, kraj_oddaje, parcele_oddaja, dat_prejem_zav, kraj_prejema, lokacija_prejema, parcele_prejem, wol_num, naziv_odpadka, nevaren, kol_kg, emb_shema, svece, dejavnost_nast, izvor_odpadka, predviden_postopek, evl_status, ind_sprejeto])


# commit changes to db
conn.commit()

# close connection and cursor
cur.close()
conn.close()

print("[%s] DONE ALL" % strftime("%H:%M:%S", gmtime()))
