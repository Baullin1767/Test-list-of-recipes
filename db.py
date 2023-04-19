import psycopg2 as p2

def connect_db():
    p2.connect(dbname = "PostgreSQL 15", host="localhost", user="postgres", password="1767")
    print('Подключился к базе')


#INSERT


#SELECT

#UPDATE

#DЕLETE