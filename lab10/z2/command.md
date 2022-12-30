```terminal
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem sha256 -days 365 -nodes
```
- `req`  - komenda do generacji CSR.
- `-newkey rsa:4096` - generacja 4096 bitowego prywathnego klucza RSA,
- `-keyout key.pem` - specyfikacja do jakiego pliku należy zrzucić klucz,
- `-out cert.pem` - specyfikacja do jakiego pliku należy zrzucić cert.pem.
- `sha256` - algorytm funkcji skrótu,
- `-days 365` - na ile dni powinno być ważne,
- `-nodes` - `no DES` indykacja, że nie chcę być pytany o passphrase