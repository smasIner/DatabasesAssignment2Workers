# DatabasesAssignment2Workers
# DatabasesAssignment2Workers
1) 
Index: 
B-Tree - by default
Query:
SELECT * FROM customers WHERE id = '550243';
Total cost (8.44):
QUERY PLAN                                                         
----------------------------------------------------------------------------------------------------------------------------
 Index Scan using customers_pkey on customers  (cost=0.42..8.44 rows=1 width=121) (actual time=2.491..2.495 rows=1 loops=1)
   Index Cond: (id = '550243'::bigint)
 Planning Time: 3.515 ms
 Execution Time: 2.525 ms
(4 rows)
Python elapsed time:
B-tree on "SELECT * FROM customers WHERE id = '550243'" query 0:00:00.003545 - (seconds)


2)
Index: 
Hash - CREATE INDEX ON customers USING Hash (id)
Query:
SELECT * FROM customers WHERE id = '550243'
Total cost (8.02):
QUERY PLAN                                                          
------------------------------------------------------------------------------------------------------------------------------
 Index Scan using customers_id_idx on customers  (cost=0.00..8.02 rows=1 width=121) (actual time=0.020..0.021 rows=1 loops=1)
   Index Cond: (id = '550243'::bigint)
 Planning Time: 2.995 ms
 Execution Time: 0.046 ms
(4 rows)
Python elapsed time:
Hash on "SELECT * FROM customers WHERE id = '550243'" query 0:00:00.002858 - (seconds)

3)
Index:
GIN - CREATE INDEX ON customers USING gin (to_tsvector('english', review));  
Query:
SELECT review                                                                                                                                                      FROM customers                                                                                                                                                                                     WHERE to_tsvector('english', review) @@ to_tsquery('english', 'husband');
Total cost (12655.72):
QUERY PLAN                                                                
-----------------------------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on customers  (cost=58.75..12655.72 rows=5000 width=32) (actual time=4.164..11.629 rows=8549 loops=1)
   Recheck Cond: (to_tsvector('english'::regconfig, review) @@ '''husband'''::tsquery)
   Heap Blocks: exact=6938
   ->  Bitmap Index Scan on customers_to_tsvector_idx  (cost=0.00..57.50 rows=5000 width=0) (actual time=2.384..2.384 rows=8549 loops=1)
         Index Cond: (to_tsvector('english'::regconfig, review) @@ '''husband'''::tsquery)
 Planning Time: 0.350 ms
 Execution Time: 12.553 ms
 Python elapsed time:
 GIN on "SELECT review  FROM customers WHERE to_tsvector('english', review) @@ to_tsquery('english', 'husband');" query 0:00:00.088801 - (seconds)
 
4) 
Index: 
BRIN - CREATE INDEX ON customers USING brin(name);  
Query(disabled seqscan to show performance):
SET enable_seqscan TO 'OFF';
select name from customers where name = 'Julie Davis';
Total cost (8.44):
 QUERY PLAN                                                                  
---------------------------------------------------------------------------------------------------------------------------------------------
 Gather  (cost=1018.02..25737.35 rows=5000 width=32) (actual time=2.175..92.678 rows=34 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   ->  Parallel Bitmap Heap Scan on customers  (cost=18.02..24237.35 rows=2083 width=32) (actual time=8.785..79.844 rows=11 loops=3)
         Recheck Cond: (name = 'Julie Davis'::text)
         Rows Removed by Index Recheck: 333322
         Heap Blocks: lossy=8082
         ->  Bitmap Index Scan on customers_name_idx  (cost=0.00..16.77 rows=1000000 width=0) (actual time=1.250..1.250 rows=190110 loops=1)
               Index Cond: (name = 'Julie Davis'::text)
 Planning Time: 1.064 ms
 Execution Time: 92.756 ms
(11 rows)
Python elapsed time:
BRIN on "select name from customers where name = 'Julie Davis';" query 0:00:00.081118 (seconds)


5)
Index:
GIST - CREATE EXTENSION pg_trgm; CREATE INDEX ON customers USING gist(address gist_trgm_ops);
Query:
SELECT address, similarity(address, 'USS Brown') AS sml                                                                                                                         FROM customers                                                                                                                                                                                     WHERE address % 'USS Brown'                                                                                                                                                                        ORDER BY sml DESC                                                                                                                                                                                  LIMIT 10;
Total cost(17930.04):
QUERY PLAN                                                                       
-------------------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=17930.01..17930.04 rows=10 width=36) (actual time=327.136..327.139 rows=10 loops=1)
   ->  Sort  (cost=17930.01..17955.01 rows=10000 width=36) (actual time=327.134..327.135 rows=10 loops=1)
         Sort Key: (similarity(address, 'USS Brown   '::text)) DESC
         Sort Method: top-N heapsort  Memory: 25kB
         ->  Bitmap Heap Scan on customers  (cost=1221.91..17713.91 rows=10000 width=36) (actual time=324.989..327.063 rows=362 loops=1)
               Recheck Cond: (address % 'USS Brown'::text)
               Heap Blocks: exact=362
               ->  Bitmap Index Scan on customers_address_idx  (cost=0.00..1219.41 rows=10000 width=0) (actual time=324.931..324.931 rows=362 loops=1)
                     Index Cond: (address % 'USS Brown'::text)
 Planning Time: 0.258 ms
 Execution Time: 327.251 ms
Python elapsed time:
GIST on very long query 0:00:05.524049 (seconds)