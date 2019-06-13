# Semi-automatic Certificate Signing Request generator.

## How to use?

- make the CSR Subject.

  e.g.) 
  ```
  "CN=www.example.com, OU=Example Unit, O=Example Company, ST=Tokyo, C=JP"
  ```

- Run.(need Double quote) 

  ```
  $ python main.py "CN=www.example.com, OU=Example Unit, O=Example Company, ST=Tokyo, C=JP"
  ```

- Print your csr strings and saved files.
  ```
   ./csrgen/
          ./[CN].csr
          ./[CN].key
  ```

## Requirement

- CentOS, Ubuntu, Other linux system..
- Python 3.4+
- openssl
