import pymysql.cursors

class Tampil():
    def Tampil_Judul_Bab():
        # Open database connection
        db = pymysql.connect("localhost","root","","db_hadits" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # Prepare SQL query to INSERT a record into the database.
        sql = "SELECT * FROM tb_judulbab"
        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Fetch all the rows in a list of lists.
           results = cursor.fetchall()
           return results
           #for row in results:
            # fname = row[0]
           #  lname = row[1]
              #Now print fetched result
            # print ("fname = %s,lname = %s" % \
                   # (fname, lname))
        
        except:
           print ("Error: unable to fetch data")

        # menutup koneksi ke server
        db.close()

    def Tampil_Hadis_PerBAB(judul):
        #judul = "Hadits Tentang Wahyu"
        db = pymysql.connect("localhost","root","","db_hadits" )
        cursor = db.cursor()
        sql = """SELECT * FROM tb_hadits WHERE judul_bab = %s"""
        try:
            cursor.execute(sql, (judul,))
            results = cursor.fetchall()
            return results
        except:
           print ("Error: unable to fetch data")

        db.close()

    def Tampil_Hadis():
        db = pymysql.connect("localhost","root","","db_hadits" )
        cursor = db.cursor()
        sql = "SELECT * FROM tb_hadits"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except:
            print ("Error: unable to fetch data")

        db.close()

    def Tampil_KataDasar():
        db = pymysql.connect("localhost","root","","db_hadits" )
        cursor = db.cursor()
        sql = "SELECT katadasar FROM tb_katadasar"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except:
            print ("Error: unable to fetch data")

        db.close()

    def Update_Hadis(id, text):
        db = pymysql.connect("localhost","root","","db_hadits" )
        cursor = db.cursor()
        sql_update_query = """ UPDATE tb_hadits
                SET textpreprocessing = %s
                WHERE id = %s """
        data = (text, id)
        try:
            cursor.execute(sql_update_query, data)
            db.commit()
            #print (cursor.execute(sql_update_query, data))
            #print ("Data Berhasil di Update")
        except:
            print ("Error: unable to update data")

        db.close()

#print(Tampil.Tampil_KataDasar())
