from csv import DictReader
import psycopg2

host = '91.236.1.204'
dbname = 'sloveniantrash'
user = 'postgres'
password = 'admin'
conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
# set up a cursor to work with db
cur = conn.cursor()

# ta del je za naselja
with open('C:/Users/Nik/Documents/fri/3. letnik/MT/Modul1-podatki/NA_UTF.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)

    for row in csv_dict_reader:
        cur.execute("INSERT INTO naselja (id, name, o_id) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;", [row["na_id"], row["na_name"].encode('cp1250').decode(), row["o_id"]])

# ta del je za obcine
with open('C:/Users/Nik/Documents/fri/3. letnik/MT/Modul1-podatki/OB_UTF.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)

    for row in csv_dict_reader:
        cur.execute("INSERT INTO obcine (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;", [row["o_id"], row["o_name"].encode('cp1250').decode()])

# ta del je za ulice
with open('C:/Users/Nik/Documents/fri/3. letnik/MT/Modul1-podatki/UL_UTF.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)

    for row in csv_dict_reader:
        cur.execute("INSERT INTO ulice (id, name, o_id) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;", [row["u_id"], row["u_name"].encode('cp1250').decode(), row["o_id"]])

# commit changes to db
conn.commit()

# close connection and cursor
cur.close()
conn.close()