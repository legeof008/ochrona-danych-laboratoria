# Szyfrowanie i deszyfrowanie algorytmem RC4
Aby sprawdzić działanie algorytmu na mniejszą skale, skryptu example.py należy skorzystać z komendy:
```python
python example.py
```
Aby skorzystać z narzędzia cli i dowiedzieć się więcej na temat jego korzystania należy użyć:
```python
python -m odsiRC4 --help
```
Aby sprawdzić testy zgodności z algorytmem `ACR4` biblioteki `Crypto.Cipher`:
```python
python -m unittest odsiRC4/test/*_test.py
```
lub wywołać skrypt ``tests.sh``.