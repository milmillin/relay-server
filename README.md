# relay-server

## Installation
 
  1. Set `MILUAI_PWD` to your password
  2. Install OpenSSL on your server if it's not already installed.
  3. Open a command prompt or terminal window and navigate to the directory where you want to generate the server.pem file.
  4. Run the following command to generate a private key:

  ```openssl genpkey -algorithm RSA -out private_key.pem```

  5. Run the following command to generate a certificate signing request (CSR):

  ```openssl req -new -key private_key.pem -out server.csr```

  6. Follow the prompts to provide the information requested for the CSR, such as your organization's information, location, and so on.

  7. Once you have completed the prompts, a CSR file named server.csr will be generated in the directory.

  8. Use the CSR to generate a self-signed certificate by running the following command:

  ```openssl x509 -req -days 365 -in server.csr -signkey private_key.pem -out server.crt```

  This will create a certificate file named server.crt.

  9. Finally, you can combine the private key and certificate into a single file, which can be used as a server.pem file:

  ```cat private_key.pem server.crt > server.pem```
