#https://kresna-devara.medium.com/cryptography-data-encryption-standard-des-e23aac8d5896

def circular_shift_left(binaries, shift): 
    cut = binaries[:shift]
    res = binaries[shift:] + cut
    return res

def key_generator(key): 

    def permutation(initial_key, perm_choice):
        return [initial_key[i - 1] for i in perm_choice]#perm index 1

    def split_key(initial_key):
        return initial_key[:28], initial_key[28:]# mkarena tidak menggunakan lsb

    def generate_sub_keys(initial_key):
        # menghasilkan subkey berdasarkan.
        sub_keys = []
        for i in range(16):
            c, d = split_key(initial_key)
            c = circular_shift_left(c, shift_schedule[i])
            d = circular_shift_left(d, shift_schedule[i])
            initial_key = c + d 
            sub_key = permutation(initial_key, perm_choice_2)
            sub_keys.append(sub_key)
        return sub_keys

    shift_schedule = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    perm_choice_1 = [57,49,41,33,25,17,9,
                     1,58,50,42,34,26,18,
                     10,2,59,51,43,35,27,
                     19,11,3,60,52,44,36,
                     63,55,47,39,31,23,15,
                     7,62,54,46,38,30,22,
                     14,6,61,53,45,37,29,
                     21,13,5,28,20,12,4]
    perm_choice_2 = [14,17,11,24,1,5,
                     3,28,15,6,21,10,
                     23,19,12,4,26,8,
                     16,7,27,20,13,2,
                     41,52,31,37,47,55,
                     30,40,51,45,33,48,
                     44,49,39,56,34,53,
                     46,42,50,36,29,32]
    sub_keys = []

    key_binaries = ''.join(format(ord(char), '08b') for char in key)# Setiap karakter dalam key mengonversinya menjadi biner 8-bit
    key_binaries = permutation(key_binaries, perm_choice_1)
    sub_keys = generate_sub_keys(key_binaries)#untuk menghasilkan 16 subkeys

    return sub_keys

def initial_permutation(binaries): 
    # melakukan permutasi awal pada blok biner.
    initial_permutation = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,
                           62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,
                           57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,
                           61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
    result = ['a' for i in range(64)]#M List ini akan digunakan untuk menyimpan hasil permutasi.
    for i in range(len(initial_permutation)):#Melakukan iterasi sebanyak panjang tabel permutasi initial_permutation (yaitu 64 kali)
        result[i] = binaries[initial_permutation[i] - 1]#di isi variabel bineies ada posisi yang ditentukan oleh tabel permutasi initial_permutation
    res = ''.join(result)#Menggabungkan semua elemen dalam list result menjadi satu string biner. Hasilnya adalah blok biner yang telah mengalami permutasi awal.
    return res 

def final_permutation(binaries): 
    # melakukan permutasi akhir pada blok biner.
    final_permutation = [40,8,48,16,56,24,64,32,
                         39,7,47,15,55,23,63,31,
                         38,6,46,14,54,22,62,30,
                         37,5,45,13,53,21,61,29,
                         36,4,44,12,52,20,60,28,
                         35,3,43,11,51,19,59,27,
                         34,2,42,10,50,18,58,26,
                         33,1,41,9,49,17,57,25]
    result = ['a' for i in range(64)]
    for i in range(len(final_permutation)):
        result[i] = binaries[final_permutation[i] - 1]
    res = ''.join(result)
    return res

def s_box(binaries):
    # melakukan substitusi dengan tabel S-box sesuai dengan algoritma DES.
    s_boxes = [
        [
            [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
            [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
            [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
            [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
        ],
        [
            [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
            [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
            [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
            [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
        ],
        [
            [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
            [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
            [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
            [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
        ],
        [
            [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
            [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
            [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
            [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
        ],
        [
            [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
            [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
            [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
            [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
        ],
        [
            [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
            [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
            [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
            [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
        ],
        [
            [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
            [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
            [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
            [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
        ],
        [
            [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
            [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
            [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
            [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
        ]
    ]
#untuk mengganti blok-blok bit dalam data enkripsi dengan blok-blok bit yang baru.
    result = ''
    for i in range(0, len(binaries), 6):#Setiap iterasi mengambil blok 6 bit dari variabel binaries
        tmp = binaries[i:i + 6]#Memotong blok 6 bit dari variabel binaries untuk diolah.
        row = int(tmp[0] + tmp[5], 2)#Mengonversi dua bit pertama dan dua bit terakhir dari tmp menjadi bilangan desimal. Dua bit pertama dan dua bit terakhir digunakan untuk menentukan baris (row) dalam tabel S-box.
        col = int(tmp[1:5], 2)#Mengonversi empat bit tengah dari tmp menjadi bilangan desimal. Empat bit tengah digunakan untuk menentukan kolom (column) dalam tabel S-box.
        temp = bin(s_boxes[i//6][row][col])[2:]#Mengambil nilai dari tabel S-box menggunakan baris (row) dan kolom (col) yang telah ditentukan.  Ini dilakukan karena dalam implementasi DES, kita hanya membutuhkan 4 bit hasil konversi S-box.
        #menghasilkan indeks baris yang benar dalam tabel S-box.
        if len(temp) == 4:#: Memeriksa panjang dari temp. Jika panjangnya 4, artinya nilai dari S-box adalah 4 bit.
            result += temp
        else:
            result += (4 - len(temp) % 4) * '0' + temp # maka perlu menambahkan padding 0 di depan sehingga panjangnya menjadi 4
    return result

def feistel(binaries, rounds, sub_keys):
    # mewakili putaran Feistel pada algoritma DES.
    expansion_table = [32,1,2,3,4,5,
                       4,5,6,7,8,9,
                       8,9,10,11,12,13,
                       12,13,14,15,16,17,
                       16,17,18,19,20,21,
                       20,21,22,23,24,25,
                       24,25,26,27,28,29,
                       28,29,30,31,32,1]
    straight_permutation_table = [16,7,20,21,29,12,28,17,
                                  1,15,23,26,5,18,31,10,
                                  2,8,24,14,32,27,3,9,
                                  19,13,30,6,22,11,4,25]
    
    expanded = ['a' for i in range(48)]# Membuat list expanded yang berisi 48 elemen dengan nilai awal 'a'. List ini digunakan untuk menyimpan hasil ekspansi dari blok 32-bit selama proses Feistel.
    for i in range(len(expansion_table)):
        expanded[i] = binaries[expansion_table[i] - 1]
    expanded_binaries = ''.join(expanded)#Menggabungkan semua elemen dalam list expanded menjadi satu string biner

    tmp = ''
    for i in range(len(expanded_binaries)):
        #Menambahkan hasil XOR dari dua bit pada posisi yang sama dalam expanded_binaries dan subkunci dari sub_keys pada putaran rounds ke dalam tmp.
        tmp += str(ord(expanded_binaries[i]) ^ ord(sub_keys[rounds][i]))
    temp = s_box(tmp)#subtitusi dengan s_box
    res = ['a' for i in range(32)]
    for i in range(len(straight_permutation_table)):
        res[i] = temp[straight_permutation_table[i] - 1]
    result = ''.join(res)#Menggabungkan semua elemen dalam list res menjadi satu string biner. Hasilnya adalah blok 32-bit yang telah mengalami permutasi lurus.
    return result

def DES_encrypt(text, key):
    sub_keys = key_generator(key)# digunakan untuk menghasilkan subkunci yang diperlukan untuk algoritma DES berdasarkan kunci awal key.
   #Teks dimodifikasi agar memiliki panjang yang merupakan kelipatan 8 dengan menambahkan spasi jika perlu. Ini memastikan bahwa teks dapat dibagi menjadi blok-blok 8 karakter.
    if len(text) % 8 != 0:
        text += ' ' * (8 - len(text) % 8)
   #Teks dibagi menjadi blok-blok 8 karakter yang akan dienkripsi secara terpisah.     
    list_of_plaintext = [text[i:i + 8] for i in range(0, len(text), 8)]

    ciphertext = ''
    for chunk in list_of_plaintext:# Loop ini digunakan untuk mengambil setiap blok 8 karakter
        binaries = ''.join(format(ord(char), '08b') for char in chunk)# mengonversi nilai ASCII tersebut menjadi representasi biner 8-bit.
        binaries = initial_permutation(binaries)#Blok biner yang dihasilkan kemudian melewati proses permutasi
        left = binaries[:32]
        right = binaries[32:]
        for i in range(16):
            temp_right = right
            right = feistel(right, i, sub_keys)  # Pemanggilan fungsi feistel dengan tiga argumen (right, i, dan sub_keys)
            #Operasi XOR dilakukan antara blok kiri sebelumnya (left) dengan blok kanan yang baru diubah (right).Operasi XOR dilakukan untuk menghasilkan blok kanan berikutnya.
            right2 = ''.join(str(ord(left[j]) ^ ord(right[j])) for j in range(len(right))) 
            left = temp_right#Blok kiri diperbarui dengan nilai blok kanan sebelumnya
            right = right2#Blok kanan diperbarui dengan nilai hasil operasi XOR (right2)
        final = right + left#digabungkan kembali
        result = final_permutation(final)# Blok 64-bit hasil dari penggabungan blok kiri dan kanan melewati proses permutasi akhir 
        #Baris kode ini bertanggung jawab untuk mengonversi blok 64-bit yang telah dienkripsi (result) ke dalam bentuk string karakter yang akan dihasilkan sebagai blok teks ciphertext
        #substring dari result yang diambil dari indeks i hingga i + 8
        #int(..., 2), yang mengartikan string biner ke bilangan bulat
        ciphertext_chunk = ''.join([chr(int(result[i:i + 8], 2)) for i in range(0, len(result), 8)])
        ciphertext += ciphertext_chunk#Blok ciphertext yang dihasilkan pada langkah sebelumnya ditambahkan ke variabe
    
    print("Ciphertext: " + ciphertext)
    print("Ciphertext hex encoded: " + ciphertext.encode('utf-8').hex())
    #Baris ini mencetak teks "Ciphertext hex encoded: " diikuti oleh nilai ciphertext yang diubah menjadi format heksadesimal. Pertama, ciphertext diubah menjadi byte menggunakan metode .encode('utf-8'). Kemudian, hasilnya diubah menjadi format heksadesimal menggunakan metode .hex(). Ini memberikan representasi heksadesimal dari ciphertext.

def DES_decrypt(ciphertext, key):
    sub_keys = key_generator(key)
    if len(ciphertext) % 8 != 0:
        ciphertext += ' ' * (8 - len(ciphertext) % 8)
    list_of_ciphertext = [ciphertext[i:i + 8] for i in range(0, len(ciphertext), 8)]

    decrypted_text = ''
    for chunk in list_of_ciphertext:
        binaries = ''.join(format(ord(char), '08b') for char in chunk)
        binaries = initial_permutation(binaries)
        left = binaries[:32]
        right = binaries[32:]
        for i in range(15, -1, -1):
           temp_right = right
           right = feistel(right, i, sub_keys)
           right2 = ''.join(str(ord(left[j]) ^ ord(right[j])) for j in range(len(right)))
        left = temp_right
        right = right2
        final = right + left
        result = final_permutation(final)
        decrypted_chunk = ''.join([chr(int(result[i:i + 8], 2)) for i in range(0, len(result), 8)])
        decrypted_text += decrypted_chunk.rstrip(' ')  # menghapus spasi yang mungkin ditambahkan pada enkripsi
    
    print("Plaintext yang sudah didekripsi:", decrypted_text)

import sys

if len(sys.argv) != 3: #memeriksa jumlah argumen yang diberikan saat menjalankan skrip. 
    print("Usage: python des.py <plaintext/ciphertext> <key>")
else:
    text = sys.argv[1]
    key = sys.argv[2]
    if len(key) != 8:
        print("Key harus terdiri dari 8 karakter.")
    else:
        if text.isalpha():  # memastikan teks hanya mengandung huruf
            DES_encrypt(text, key)
        elif all(c in "0123456789abcdefABCDEF" for c in text):  # memastikan ciphertext adalah hex encoded
            # Skrip mendekode ciphertext menjadi string menggunakan 
            text = bytes.fromhex(text).decode('utf-8')
            DES_decrypt(text, key)
        else:
            print("Input tidak valid. Gunakan hanya huruf untuk plaintext dan hex digits untuk ciphertext.")
while True:
    print("Pilih mode:")
    print("1. Enkripsi")
    print("2. Dekripsi")
    print("3. Keluar")
    choice = int(input("Masukkan pilihan (1/2/3): "))

    if choice == 1:
        print("Masukan plaintext: ")
        plaintext = input()
        print("Masukan key (8 karakter): ")
        key = input()
        DES_encrypt(plaintext, key)

    elif choice == 2:
        print("Masukan ciphertext: ")
        ciphertext = input()
        print("Masukan key (8 karakter): ")
        key = input()
        DES_decrypt(ciphertext, key)

    elif choice == 3:
        print("Terima kasih, program telah selesai.")
        break  # Keluar dari loop

    else:
        print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")
