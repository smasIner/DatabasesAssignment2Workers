import psycopg2
from faker import Faker
from timeit import default_timer as timer
from datetime import timedelta


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
start = timer()
cur.execute("SELECT * FROM customers WHERE id = '550243'")
end = timer()
print("B-tree on \"SELECT * FROM customers WHERE id = '550243'\" query", timedelta(seconds=end-start))

cur.execute("CREATE INDEX ON customers USING Hash(id)")
start = timer()
cur.execute("SELECT * FROM customers WHERE id = '550243'")
end = timer()
print("Hash on \"SELECT * FROM customers WHERE id = '550243'\" query", timedelta(seconds=end-start))

start = timer()
cur.execute("SELECT review  FROM customers WHERE to_tsvector('english', review) @@ to_tsquery('english', 'husband');")
end = timer()
print("GIN on \"SELECT review  FROM customers WHERE to_"
      "tsvector('english', review) @@ to_tsquery('english', 'husband');\" query", timedelta(seconds=end-start))

cur.execute("SET enable_seqscan TO 'OFF';")
start = timer()
cur.execute("select name from customers where name = 'Julie Davis';")
end = timer()
cur.execute("SET enable_seqscan TO 'ON';")
print("BRIN on \"select name from customers where name = 'Julie Davis';\" query", timedelta(seconds=end-start))

start = timer()
cur.execute("SELECT address, similarity(address, 'USS Brown   ') AS sml                                                                                                                         FROM customers                                                                                                                                                                                     WHERE address % 'USS Brown'                                                                                                                                                                        ORDER BY sml DESC                                                                                                                                                                                  LIMIT 10;")
end = timer()
print("GIST on very long query", timedelta(seconds=end-start))

conn.close()
