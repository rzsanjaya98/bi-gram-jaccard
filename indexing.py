import os
import json
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from konek import Tampil as tampil
from prepro import PreProcessing as preprocessing

def urut(tokens):
    result = [x.lower().strip('-').strip(';').strip(',').strip('.').strip('"').strip('(').strip(')').strip(':').strip('?') for x in tokens.split()]
    result.sort()
    
    return result

def urut2(tokens):
    result = [x.lower().strip('-').strip(',').strip(';').strip('.').strip('"').strip('(').strip(')').strip(':').strip('?') for x in tokens]
    result.sort()
    
    return result

def createDictionary():
   wordsAdded = {}
   cwd = os.getcwd()
   data = tampil.Tampil_Hadis()
   folder = "Hadits Bukhari-Muslim/"
   fileList = []
   for i in range(len(data)):
      fileList.append(data[i][2])

   for file in fileList:
      
      with open(folder+file, 'r') as f:

         words = f.read()
         words = preprocessing.PreProcess(words)
         words = urut(words)
         words = urut2(words)
         for word in words:
            if word not in wordsAdded.keys():
               wordsAdded[word] = [f.name]
            else:
                if file not in wordsAdded[word]:
                  wordsAdded[word] += [f.name]
                  
   #return wordsAdded
   with open('indexing.txt', 'w') as json_file:
       json.dump(wordsAdded, json_file)

#def writeToFile(words):
    
            
#print(createDictionary())
createDictionary()
