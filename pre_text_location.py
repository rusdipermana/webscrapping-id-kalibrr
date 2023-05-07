import string

# Buat daftar kata-kata kunci
# key_words = {'jakarta': ['jakarta', 'jk'],
#              'barat': ['barat', 'west'],
#              'utara': ['utara', 'north'],
#              'selatan': ['selatan', 'south', 'south jakarta'],
#              'timur': ['timur', 'east'],
#              'pusat': ['pusat', 'central'],
#              'tanggerang': ['tanggerang']
#              }

# Fungsi untuk mengubah nilai
def change_value(text):
    # Lakukan text preprocessing
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())
    
    # # Pisahkan menjadi kata-kata
    # words = text.split()
    
    # # Hapus kata-kata 'pusat', 'selatan', 'timur', 'barat', 'utara' yang ada di depan kota
    # keywords = ['pusat', 'selatan', 'timur', 'barat', 'utara']
    # new_words = []
    # for i, word in enumerate(words):
    #     if word not in keywords and i == 0:
    #         new_words.append(word)
    #     elif word in keywords and words[i-1] not in keywords:
    #         continue
    #     else:
    #         new_words.append(word)
    
    # # Ganti kata-kata yang ada di dalam daftar kata-kata kunci
    # for i, word in enumerate(new_words):
    #     for key, values in key_words.items():
    #         if word in values:
    #             new_words[i] = key
    #             break
                
    # # Gabungkan kembali kata-kata menjadi sebuah string
    # new_text = ' '.join(words)
    
    return new_text