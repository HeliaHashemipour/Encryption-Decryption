import pyaes
import pbkdf2

import binascii
import secrets
import os


def read_key():
    saltedKeyFile = open("SaltedKey.txt", "rb")
    key = saltedKeyFile.read()
    key = binascii.unhexlify(key)
    saltedKeyFile.close()

    ivFile = open("iv.txt", "r")
    iv = ivFile.read()
    ivFile.close()

    return key, int(iv)


def encrypt():
    key, iv = read_key()
    aes = pyaes.AESModeOfOperationCTR(
        key, pyaes.Counter(iv))

    file = open("PlainText.txt", "r")
    plaintext = file.read()
    file.close()

    ciphertext = aes.encrypt(plaintext)
    print('Encrypted Text:', binascii.hexlify(
        ciphertext))  # print the ciphertext

    file = open("Encrypted.txt", "wb")
    file.write(binascii.hexlify(ciphertext))
    file.close()


def decrypt():
    key, iv = read_key()

    cipherTextFile = open('Encrypted.txt', 'rb')
    cipherText = cipherTextFile.read()
    cipherTextFile.close()

    aes2 = pyaes.AESModeOfOperationCTR(
        key, pyaes.Counter(iv))

    cipherText = binascii.unhexlify(cipherText)
    decrypted = aes2.decrypt(cipherText)
    print('Decrypted Text:', decrypted)

    file = open("Decrypted.txt", "w")
    file.writelines(str(decrypted))
    file.close()


def create_key():
    file = open("Key.txt", "r")
    keyValue = file.read()
    file.close()

    salt = os.urandom(16)
    key = pbkdf2.PBKDF2(keyValue, salt).read(32)

    file = open("SaltedKey.txt", "wb")
    file.write(binascii.hexlify(key))
    file.close()

    iv = secrets.randbits(256)
    file = open("iv.txt", "w")
    file.writelines(str(iv))
    file.close()


if __name__ == '__main__':
    while True:
        print("1.Create key\n2.Encrypt\n3.decrypt\n4.exit")
        inputString = input("Enter you input: ")
        if inputString == '1':
            create_key()
        elif inputString == '2':
            encrypt()
        elif inputString == '3':
            decrypt()
        elif inputString == '4':
            break
