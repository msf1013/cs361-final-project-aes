# AES implementation in Python

## cs361-final-project-aes

Final Project: AES implementation
Name: Mario Sergio Fuentes Juarez and Vishal Gullapalli

## Description

The scripts in this repository implement the AES encryption and decryption
procedures defined in https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf

Our implementation specifically uses the ECB mode, and conforms to the standard
algorithms in FIPS 197.

## How to use

a) The program was written in Python 3.6, and tested in Windows and Ubuntu platforms.
   All libraries are standard language libraries, so no special imports or installation
   are needed.   
   
   The program can be executed in the following way:

```shell
> python aes.py --keysize <keysize> --keyfile <keyfile> --inputfile <inputfile> --outputfile <outputfile> --mode <mode>
```

b) The program has 5 arguments which must be supplied via command line:

   1) keysize: An integer, either 128 or 256, representing the key size in bits.
   2) keyfile: Name of file containing the key.
   3) inputfile: Name of file containing input plaintext/ciphertext to process,
                 depending on whether mode is encrypt/decrypt.
   4) outputfile: Name of file where the output plaintext/ciphertext will be produced,
                  depending on whether mode is encrypt/decrypt.
   5) mode: A string, either 'encrypt' or 'decrypt'.

Sample call:

```shell
> python aes.py --keysize 128 --keyfile key --inputfile plaintext --outputfile ciphertext --mode encrypt
```
