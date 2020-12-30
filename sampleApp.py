try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
    from tkinter.ttk import Entry
    from tkinter import*
    from tkinter import ttk
    from konek import Tampil as tampil
    import json
    from prepro import PreProcessing as preprocessing
    from jaccard import jaccard
    from PIL import ImageTk ,Image
    from bigram import bigram
    import time    
    from time import sleep
    from threading import Thread as Thread1
    import threading
    
    
except ImportError:
    import Tkinter as tk     # python 2 
    import tkFont as tkfont  # python 2

global time_x
time_x = 0

class myThread (threading.Thread):
    def __init__(self, threadID, value, target=None, args=()  ):
        threading.Thread.__init__(self )
        self.threadID = threadID
        self._target = target
        self._args = args
        self.value = value
    def run(self):
        print ( ( "Starting " + self.value ) )
        if self._target is not None:
            typo, rank, waktu_proses1 = proses_Pencarian(self.value)
            self._return = self._target( "selesai", rank, waktu_proses1, typo )

    def join(self) :
        threading.Thread.join(self)
        return "Hasil"

def proses_Pencarian(value):
        waktu_awal = time.time()
        waktu_prepro_a = time.time()
        query = preprocessing.PreProcess(value) #Preprocessing query
        waktu_prepro_b = time.time()
        waktu_proses_pre = waktu_prepro_b - waktu_prepro_a
        print("Waktu Proses PrePro query "+str(waktu_proses_pre))

        waktu_bigram_a = time.time()
        value = bigram.proses(query) #Bigram query
        waktu_bigram_b = time.time()
        waktu_proses_bigram = waktu_bigram_b - waktu_bigram_a
        print("Waktu Proses bigram query "+str(waktu_proses_bigram))
        
        typo = ''
        if value != query:
           typo = value

        value = value.split() #Bagi perkata hasil typo/query
        f = open('indexing.json',) 
        indexing = json.load(f)

        #Mengecek query di indexing
        hasil = []
        for i in range(len(value)):
            if value[i] in indexing:
                hasil = hasil + indexing[value[i]]
        f.close()

        doc = []
        for x in range(len(hasil)):
            if hasil[x] not in doc:
                doc.append(hasil[x])

        #Ambil Data dari Database sesuai dengan dokumen yang cocok dengan query
        data = []
        dokumen = tampil.Tampil_Hadis()
        for k in range(len(doc)):
            for l in range(len(dokumen)):
                init = "Hadits Bukhari-Muslim/"+dokumen[l][2]
                #print(init)
                if doc[k] == init:
                    data.append(dokumen[l])

        #Menghitung nilai jaccard similarity tiap dokumen terhadap query
        waktu_jaccard_a = time.time()
        rank = []
        folder = "Hadits Bukhari-Muslim/"
        for j in range(len(data)):
            alamat = folder+data[j][2]
            words = jaccard.urut(data[j][3])
            nilai = jaccard.compute_jaccard_similarity_score(value, words)
            result = [alamat, nilai]
            rank.append(result)
        waktu_jaccard_b = time.time()
        waktu_proses_jaccard = waktu_jaccard_b - waktu_jaccard_a
        print("Waktu Proses jaccard "+str(waktu_proses_jaccard))

        #sorting dokumen        
        rank = sorted(rank, key=lambda x: x[1], reverse=True)
        waktu_akhir = time.time()
        waktu_proses1 = waktu_akhir - waktu_awal

        return typo, rank, waktu_proses1

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)
        #self._frame = None
        #self.switch_frame(StartPage)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Beranda, Hadits, Tentang):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Beranda")
        
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    #def switch_frame(self, frame_class):
        #new_frame = frame_class(self)
        #if self._frame is not None:
            #self._frame.destroy()
        #self._frame = new_frame
        #self._frame.pack()

class Beranda(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #frame = tk.Frame().pack()
        topframe = tk.Frame(self)
        topframe.pack(side="top", fill="x")
        menuframe = tk.Frame(self)
        menuframe.pack(anchor="center")   
        searchframe = tk.Frame(self)
        searchframe.pack(anchor="center")
        textjudul = """APLIKASI PENCARIAN HADIS RIWAYAT IMAM AL-BUKHARI"""
        bgimage = Image.open(r'C:\xampp\htdocs\Sistem Pencarian Hadis\mm3.jpeg')
        bgimage = bgimage.resize((1400, 230), Image.ANTIALIAS)
        bg = ImageTk.PhotoImage(bgimage)
        #logo = tk.PhotoImage(file="python_logo_small.gif")
        judul = tk.Label(topframe, compound = tk.CENTER, text=textjudul, font=('Tw Cen MT Condensed Extra Bold', 20, "bold"), image = bg, fg = "honeydew2")
        judul.image = bg
        judul.pack(side="top")
        #judul.grid(row="0", column="0", columnspan="3")
        bt_beranda = tk.Button(menuframe, text="BERANDA",font=("Bahnschrift SemiBold",10, "bold") ,bg="honeydew2",fg = "black",
                 command=lambda: controller.show_frame("Beranda"))
                 #command=lambda: master.switch_frame(PageOne)).pack(side="left")
        bt_hadits = tk.Button(menuframe, text="HADIS",font=("Bahnschrift SemiBold",10, "bold") ,bg="honeydew2",fg = "black",
                  #command=lambda: master.switch_frame(PageTwo)).pack(side="left")
                command=lambda: controller.show_frame("Hadits"))
        bt_tentang = tk.Button(menuframe, text="TENTANG",font=("Bahnschrift SemiBold",10, "bold") ,bg="honeydew2",fg = "black",
                  #command=lambda: master.switch_frame(PageTwo)).pack(side="left")
                command=lambda: controller.show_frame("Tentang"))
        bt_beranda.grid(row="0", column="0")
        bt_hadits.grid(row="0", column="1")
        bt_tentang.grid(row="0", column="2")
        entryCari = Entry(searchframe)
        entryCari.grid(ipadx=250, ipady=5, pady=20, padx=5)
        bt_cari = tk.Button(searchframe, text = "Cari ",font=("arial black",10) ,bg="honeydew2", fg = "black",
                            command=lambda: self.aksi_cari(entryCari.get()))
                            #command=lambda: threading.Thread(target=self.Tampil_Pencarian(entryCari.get())).start())
                            #command=lambda: self.tes(entryCari.get()))
        bt_cari.grid(row=0, column=1, padx=5)

        loadingFrame = tk.Frame(self)
        loadingFrame.pack(anchor="center")
        self.loading_text = tk.StringVar()
        loading = tk.Label(loadingFrame, textvariable=self.loading_text, font=('Helvetica 10 bold italic'))
        loading.pack()

        typoFrame = tk.Frame(self)
        typoFrame.pack(anchor="center")
        self.typo_text = tk.StringVar()
        typo = tk.Label(typoFrame, textvariable=self.typo_text, font=('Helvetica 10 bold italic'))
        typo.pack()
        
        
        hasilFrame = tk.Frame(self)
        canvas = tk.Canvas(hasilFrame)
        scrollbar = tk.Scrollbar(hasilFrame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all"), width=890
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        hasilFrame.pack()
        canvas.pack(side="left", fill="both")
        scrollbar.pack(side="right", fill="y")

        timeFrame = tk.Frame(self)
        timeFrame.pack(anchor="center")
        self.time_text = tk.StringVar()
        time = tk.Label(timeFrame, textvariable=self.time_text, font=('Helvetica 10'))
        time.pack()
        
    def selesai(self, value, rank, waktu_proses1, typo):
        self.loading_text.set( ( value ) )
        #Menampilkan dokumen
        if rank:
            for i in range(len(rank)):
                tampilDoc = open(rank[i][0], "r").read()
                text = Text(self.scrollable_frame, width=110, height=5)
                text.grid(row=i+1, column=0)
                text.insert(INSERT, tampilDoc)
        else:
           self.typo_text.set("Data tidak ditemukan")

        self.time_text.set("Waktu pencarian adalah "+str(waktu_proses1)+" Detik")
        if typo:
            self.typo_text.set("Mungkin yang anda maksud : "+typo)
        
    def aksi_cari(self, value):
        self.loading_text.set("Loading..")
        self.time_text.set("")
        self.typo_text.set("")
        #Mengosongkan label jika terisi
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        thread1 = myThread( threadID=1, value=value, target=self.selesai )
        thread1.start()
    
class Hadits(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #frame = tk.Frame().pack()
        topframe = tk.Frame(self)
        topframe.pack(side="top", fill="x")
        menuframe = tk.Frame(self)
        menuframe.pack(anchor="center")   
        searchframe = tk.Frame(self)
        searchframe.pack(anchor="center")
        textjudul = """APLIKASI PENCARIAN HADIS RIWAYAT IMAM AL-BUKHARI"""
        bgimage = Image.open(r'C:\xampp\htdocs\Sistem Pencarian Hadis\mm3.jpeg')
        bgimage = bgimage.resize((1400, 230), Image.ANTIALIAS)
        bg = ImageTk.PhotoImage(bgimage)
        #logo = tk.PhotoImage(file="python_logo_small.gif")
        judul = tk.Label(topframe, compound = tk.CENTER, text=textjudul, font=('Tw Cen MT Condensed Extra Bold', 20, "bold"), image = bg, fg = "honeydew2")
        judul.image = bg
        judul.pack(side="top")
        #judul.grid(row="0", column="0", columnspan="3")
        bt_beranda = tk.Button(menuframe, text="BERANDA",font=("Bahnschrift SemiBold",10) ,bg="honeydew2",fg = "black",
                 command=lambda: controller.show_frame("Beranda"))
                 #command=lambda: master.switch_frame(PageOne)).pack(side="left")
        bt_hadits = tk.Button(menuframe, text="HADIS",font=("Bahnschrift SemiBold",10) ,bg="honeydew2",fg = "black",
                  #command=lambda: master.switch_frame(PageTwo)).pack(side="left")
                command=lambda: controller.show_frame("Hadits"))
        bt_tentang = tk.Button(menuframe, text="TENTANG",font=("Bahnschrift SemiBold",10) ,bg="honeydew2",fg = "black",
                  #command=lambda: master.switch_frame(PageTwo)).pack(side="left")
                command=lambda: controller.show_frame("Tentang"))
        bt_beranda.grid(row="0", column="0")
        bt_hadits.grid(row="0", column="1")
        bt_tentang.grid(row="0", column="2")
        comboframe = tk.Frame(self)
        comboframe.pack(anchor="center")
        results = tampil.Tampil_Judul_Bab()
        arcomb=[]
        
        for i in range(len(results)):
            arcomb.append(results[i][1])
   
        mynumber = tk.StringVar()
        combobox = ttk.Combobox(comboframe, width = 15 , textvariable = mynumber)
        combobox['values'] = arcomb
        combobox.grid(column = 1, row = 0, ipadx=100, ipady=5, pady=50, padx=20)
        bt_combo = tk.Button(comboframe, text="Cari",font=("arial black",10) ,bg="honeydew2",fg = "black",
                             command=lambda: self.Tampil_Combo(combobox.get()))
        bt_combo.grid(row="0", column="2")
        
        hasilFrame = tk.Frame(self)
        canvas = tk.Canvas(hasilFrame)
        scrollbar = tk.Scrollbar(hasilFrame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all"), width=890
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        hasilFrame.pack()
        canvas.pack(side="left", fill="both")
        scrollbar.pack(side="right", fill="y")

        #style = ttk.Style(self)
        #style.configure('Treeview', rowheight=100)

    def Tampil_Combo(self, value):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        #self.scrollable_frame = None
        folder = "Hadits Bukhari-Muslim/"
        hasil = tampil.Tampil_Hadis_PerBAB(value)
        #listBox = ttk.Treeview(hasilFrame, columns=cols, show='headings')
        for i in range(len(hasil)):
            tampilDoc = open(folder + hasil[i][2], "r").read()
            text = Text(self.scrollable_frame, width=110, height=5)
            text.grid(row=i+1, column=0)
            text.insert(INSERT, tampilDoc)
        
        
class Tentang(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #frame = tk.Frame().pack()
        topframe = tk.Frame(self)
        topframe.pack(side="top", fill="x")
        menuframe = tk.Frame(self)
        menuframe.pack(anchor="center")   
        searchframe = tk.Frame(self)
        searchframe.pack(anchor="center")
        textjudul = """APLIKASI PENCARIAN HADIS RIWAYAT IMAM AL-BUKHARI"""
        bgimage = Image.open(r'C:\xampp\htdocs\Sistem Pencarian Hadis\mm3.jpeg')
        bgimage = bgimage.resize((1400, 230), Image.ANTIALIAS)
        bg = ImageTk.PhotoImage(bgimage)
        #logo = tk.PhotoImage(file="python_logo_small.gif")
        judul = tk.Label(topframe, compound = tk.CENTER, text=textjudul, font=('Tw Cen MT Condensed Extra Bold', 20, "bold"), image = bg, fg = "honeydew2")
        judul.image = bg
        judul.pack(side="top")
        #judul.grid(row="0", column="0", columnspan="3")
        bt_beranda = tk.Button(menuframe, text="BERANDA",font=("Bahnschrift SemiBold",10) ,bg="honeydew2",fg = "black",
                 command=lambda: controller.show_frame("Beranda"))
                 #command=lambda: master.switch_frame(PageOne)).pack(side="left")
        bt_hadits = tk.Button(menuframe, text="HADIS",font=("Bahnschrift SemiBold",10) ,bg="honeydew2",fg = "black",
                  #command=lambda: master.switch_frame(PageTwo)).pack(side="left")
                command=lambda: controller.show_frame("Hadits"))
        bt_tentang = tk.Button(menuframe, text="TENTANG",font=("Bahnschrift SemiBold",10) ,bg="honeydew2",fg = "black",
                  #command=lambda: master.switch_frame(PageTwo)).pack(side="left")
                command=lambda: controller.show_frame("Tentang"))
        bt_beranda.grid(row="0", column="0")
        bt_hadits.grid(row="0", column="1")
        bt_tentang.grid(row="0", column="2")

        var = tk.Frame(self)
        var.pack(anchor="c")

        canv = tk.Frame(self, width=360, height=414)
        canv.pack(anchor="c")
        image = Image.open(r'C:\xampp\htdocs\Sistem Pencarian Hadis\hh.jpg')
        # The (450, 350) is (height, width)
        image = image.resize((200, 250), Image.ANTIALIAS)
        foto = ImageTk.PhotoImage(image)
        my_img = Label(canv, image = foto)
        my_img.image = foto
        my_img.grid(rowspan=11, column=0)

        sinopsis= Label(canv, text="Penulis : Muhammad Makmun-Abha, .-Rifki Hadi, .I.")
        sinopsis1= Label(canv, text="Penerbit : Mutiara Media")
        sinopsis2= Label(canv, text="Buku ini berisi kumpulan hadis riwayat Bukhari dan Muslim yang disusun secara tematik.")
        sinopsis3= Label(canv, text="Isinya merujuk pada terjemah kitab Mukhtashar Ibn Abi Jamrah lil Bukhari (ringkasan kitab")
        sinopsis4= Label(canv, text="Shahih al-Bukhari), yang dilengkapi dengan terjemah hadis-hadis semakna yang terdapat dalam")
        sinopsis5= Label(canv, text="kitab Shahih Muslim. Memuat tema-tema penting yang paling dicari sehari-hari,seperti hadis-hadis")
        sinopsis6= Label(canv, text="yang berkaitan dengan turunnya wahyu, akidah, iman, dan Islam, hadis tentang ilmu, shalat,")
        sinopsis7= Label(canv, text="sedekah, hibah, dan infak, hadis tentang haji, jihad, nikah, kurban, kematian, alam kubur")
        sinopsis8= Label(canv, text="dan hari akhir, hadis tentang zikir dan doa, qadha dan qadar, hadis tentang makanan halal")
        sinopsis9= Label(canv, text="dan haram, bekerja, wirausaha, dan transaksi, hadis tentang penyakit dan obat, pemimpin,")
        sinopsis10= Label(canv, text="mimpi, hak dan kasih sayang, dan hadis-hadis dengan tema lainnya.")
                            
        sinopsis.grid(row=0, column=1)
        sinopsis1.grid(row=1, column=1)
        sinopsis2.grid(row=2, column=1)
        sinopsis3.grid(row=3, column=1)
        sinopsis4.grid(row=4, column=1)
        sinopsis5.grid(row=5, column=1)
        sinopsis6.grid(row=6, column=1)
        sinopsis7.grid(row=7, column=1)
        sinopsis8.grid(row=8, column=1)
        sinopsis9.grid(row=9, column=1)
        sinopsis10.grid(row=10, column=1)
        
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
