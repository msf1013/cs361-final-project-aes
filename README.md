# AES implementation in Python

**CS 361 Final Project:** AES implementation

**Authors:** Mario Sergio Fuentes Juarez and Vishal Gullapalli

**Link to repository in GitHub:** https://github.com/msf1013/cs361-final-project-aes

## Description

The scripts in this repository implement the AES encryption and decryption procedures defined in https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf

Our implementation specifically uses the ECB mode, and conforms to the standard algorithms in FIPS 197.

## Implementation details

Our code almost directly implements the algorithms defined in the AES reference spec,
reading 16 bytes of input data at a time and passing that data to the conventional
encryption/decryption pipeline outlined in the reference spec. 10 rounds are run for
128 bits long keys, whereas 14 rounds are run for 256 bits long keys, and each round
consists of the following operations over the input block:

1) **Substitute bytes**: Applying a byte-by-byte transformation using a pre-computed
   look-up table.
2) **Shift rows**: By performing a cyclical shift as defined in the spec.
3) **Mix columns**: Using pre-computed look-up tables for Galois Field multiplication.
4) **Add round key**: Adding the round key to the state data block via XOR operations.

(It is worth noting that inverse operations where defined for decryption).

All of the resulting data blocks are then concatenated to produce the output
cipher/plain text.

Finally, as suggested by our previous notes, we made use of a number of pre-computed
look-up tables for the following operations:

- Bytes substitution
- Inverse bytes substitution
- Round constant word array used for key expansion
- Multiplication by 2, 3, 9, 11, 13, and 14 in the Galois Field.

## How to use

a) The program was written in Python 3.6, and tested in Windows and Ubuntu platforms.
   All libraries are standard, so no special imports or installation are needed.   
   
   The program can be executed in the following way:

```shell
> python aes.py --keysize <keysize> --keyfile <keyfile> --inputfile <inputfile> --outputfile <outputfile> --mode <mode>
```

b) The program has 5 arguments which must be supplied via command line:

   1) `keysize`: An integer, either 128 or 256, representing the key size in bits.
   2) `keyfile`: Name of file containing the key.
   3) `inputfile`: Name of file containing input plaintext/ciphertext to process,
                 depending on whether mode is encrypt/decrypt.
   4) `outputfile`: Name of file where the output plaintext/ciphertext will be produced,
                  depending on whether mode is encrypt/decrypt.
   5) `mode`: A string, either 'encrypt' or 'decrypt'.

Sample call:

```shell
> python aes.py --keysize 128 --keyfile key --inputfile plaintext --outputfile ciphertext --mode encrypt
```
