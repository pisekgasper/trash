import pandas as pd
from csv import DictReader
import psycopg2

conn = psycopg2.connect("dbname=sloveniantrash user=postgres password=admin")
# set up a cursor to work with db
cur = conn.cursor()

# ta del je za naselja
with open('C:/Users/Nik/Documents/fri/3. letnik/MT/Modul1-podatki/NA.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)

    for row in csv_dict_reader:
        cur.execute("INSERT INTO naselja (id, name, o_id) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;", [row["na_id"], row["na_name"], row["o_id"]])

# ta del je za obcine
with open('C:/Users/Nik/Documents/fri/3. letnik/MT/Modul1-podatki/OB_VSE.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)

    for row in csv_dict_reader:
        cur.execute("INSERT INTO obcine (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;", [row["o_id"], row["o_name"]])

# ta del je za ulice
with open('C:/Users/Nik/Documents/fri/3. letnik/MT/Modul1-podatki/UL_VSE.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)

    for row in csv_dict_reader:
        cur.execute("INSERT INTO ulice (id, name, o_id) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;", [row["u_id"], row["u_name"], row["o_id"]])

# commit changes to db
conn.commit()

# close connection and cursor
cur.close()
conn.close()