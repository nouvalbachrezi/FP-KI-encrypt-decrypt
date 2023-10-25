from Crypto.Cipher import DES
from secrets import token_bytes #untuk menghasilkan kunci enkripsi yang digunakan oleh algoritma DES

key = token_bytes(8)

def encrypt(msg):
    cipher = DES.new(key, DES.MODE_EAX)
    nonce = cipher.nonce 
    encrypted_text, tag = cipher.encrypt_and_digest(msg.encode('ascii')) 
    return nonce, encrypted_text, tag

def decrypt(nonce, encrypted_text, tag): #masukan
    cipher = DES.new(key, DES.MODE_EAX, nonce=nonce)#noncenya digunakan untuk menentukan nilai nonce yang akan digunakan dalam operasi enkripsi atau dekripsi. 
    decrypted_text = cipher.decrypt(encrypted_text)

    try:
        cipher.verify(tag)
        return decrypted_text.decode('ascii')
    except ValueError:
        return False

while True:
    choice = input('Encrypt or Decrypt? (E/D): ').upper() # agar pemrosesan input tidak bersifat case-sensitive.

    if choice == 'E':
        message = input('Enter a message to encrypt: ')
        nonce, encrypted_text, tag = encrypt(message) #Fungsi encrypt() dipanggil dengan menggunakan pesan yang dimasukkan oleh pengguna sebagai argumen. Fungsi ini mengembalikan tiga nilai: nonce (numerical once), teks terenkripsi, dan tag. Nilai-nilai ini disimpan dalam variabel nonce, encrypted_text, dan tag berturut-turut.
        print(f'Encrypted text: {encrypted_text.hex()}')
        print(f'Nonce: {nonce.hex()}')
        print(f'Tag: {tag.hex()}')
    elif choice == 'D':
        try:
            encrypted_text = bytes.fromhex(input('Enter the encrypted text (dalam bentuk hexadecimal): ')) # mengonversi string hexadecimal menjadi objek bytes
            nonce = bytes.fromhex(input('Enter the nonce (dalam bentuk hexadecimal): '))
            tag = bytes.fromhex(input('Enter the tag (dalam bentuk hexadecimal): '))
            decrypted_text = decrypt(nonce, encrypted_text, tag)
            if decrypted_text:
                print(f'Decrypted text: {decrypted_text}')
            else:
                print('Decryption failed or message is corrupted!')
        except ValueError:
            print('Invalid input format. Please enter hexadecimal values without spaces.')
    else:
        print('Invalid choice. Please enter E or D.')
