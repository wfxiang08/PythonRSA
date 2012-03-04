@echo off


openssl genrsa -out rsa_private_key.pem 1024



openssl rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem



openssl pkcs8 -topk8 -inform PEM -in rsa_private_key.pem -outform PEM -nocrypt