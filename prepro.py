from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
import re
import string
from konek import Tampil as tampil

class PreProcessing():
    def PreProcess(dokumen):
        case = PreProcessing.Case_Folding(dokumen)
        token = PreProcessing.Tokenizing(case)
        stopword = PreProcessing.Stopword(case)
        stemming = PreProcessing.Stemming(stopword)
        return stemming
        
    def Case_Folding(query):
        #folder = "Hadits Bukhari-Muslim/"
        #query = "hadits tentang"
        #data_hadits = tampil.Tampdbil_Hadis()
        #data_tes = open(folder + data_hadits[0][2], "r").read()
        lower_case = query.lower()
        removing_number = re.sub(r"\d+", "", lower_case)
        hapus_tanda_baca = removing_number.translate(str.maketrans("","",string.punctuation))
        hasil = hapus_tanda_baca.strip()
        return hasil

    def Tokenizing(doc):
        tes = doc.split()
        return tes

    def Stopword(doc):
        stop_factory = StopWordRemoverFactory().get_stop_words()
        more_stopword = ['ini', 'itu', 'the']
        data = stop_factory + more_stopword
        dictionary = ArrayDictionary(data)
        data_str = StopWordRemover(dictionary)
        dokumen = data_str.remove(doc)
        return dokumen

    def Stemming(doc):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        doc = stemmer.stem(doc)
        return doc

#folder = "Hadits Bukhari-Muslim/"
        #query = "hadits tentang"
#data_hadits = tampil.Tampil_Hadis()
#for i in range(len(data_hadits)):
 #   data_tes = open(folder + data_hadits[i][2], "r").read()
  #  data_tes = PreProcessing.PreProcess(data_tes)
   # tampil.Update_Hadis(data_hadits[i][0], data_tes)
#print("Selesai")
#print(data_tes) 
