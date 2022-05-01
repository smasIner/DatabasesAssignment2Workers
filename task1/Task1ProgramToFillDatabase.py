import psycopg2
from faker import Faker


"""
TO USE THIS PROGRAM YOU NEED TO:
1) !pip install faker
2) !pip install psycopg2-binary 
3) Substitute your own parameters
"""

fake = Faker()
conn = psycopg2.connect(database="Assignment2Ex", user="postgres", password="Osuisthebestgame", host="127.0.0.1",
                        port="5432")
cur = conn.cursor()
for i in range(1000000):
    id = i + 1
    name = fake.name()
    address = fake.address()
    review = fake.paragraph(nb_sentences=2)
    cur.execute("INSERT INTO customers (id,name,address,review) "
                "VALUES (%s, %s, %s, %s)", (id, name, address, review))
conn.commit()
conn.close()
