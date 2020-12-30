import re
import string
import json
from prepro import PreProcessing as preprocessing
from konek import Tampil as tampil
from jaccard import jaccard

class bigram():
    def urut(query):  
        result = []
        for idx in range(len(query) - 1):
            result.append(query[idx : idx + 2])
        return result

    def proses(test_str):
        kata_pengganti = ""
        katadasar = tampil.Tampil_KataDasar()
        #katadasar = json.JSONDecoder().decode(katadasar)
        katadasar = [i[0] for i in katadasar ]
        query = preprocessing.PreProcess(test_str)
        query = query.split()
        hasil = []
        for i in range(len(query)):
            if query[i] in katadasar:
                hasil.append(query[i])
            else:
                word = bigram.urut(query[i])
                nilai = 0
                for j in range(len(katadasar)):
                    kata_urut = bigram.urut(katadasar[j])                    
                    nilai_tertinggi = jaccard.compute_jaccard_similarity_score(word, kata_urut)
                    if nilai_tertinggi > nilai:
                        print(kata_urut)
                        print(nilai_tertinggi)
                        nilai = nilai_tertinggi
                        kata_pengganti = katadasar[j]
                hasil.append(kata_pengganti)
        #print(katadasar[2])
        #hasil.append(bigram.urut(query[i]))
        spasi = " "
        hasil = spasi.join(hasil)
        return hasil
        
#print(bigram.tes("hukum makan"))
