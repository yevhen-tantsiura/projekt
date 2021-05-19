import pypyodbc
import azurecred
from datetime import datetime

class AzureDB:
    dsn='DRIVER='+azurecred.AZDBDRIVER+';SERVER='+azurecred.AZDBSERVER+';DATABASE='+azurecred.AZDBNAME+';UID='+azurecred.AZDBUSER+';PWD='+ azurecred.AZDBPW
    
    def __init__(self):
        self.conn = pypyodbc.connect(self.dsn)
        self.cursor = self.conn.cursor()
    
    def finalize(self):
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()
    
    def azureAddData(self, name, mail, text):
        date = datetime.utcnow() 
        self.cursor.execute("INSERT INTO data (name, mail, text, date) values (?,?,?,?)", [name, mail, text, date])
        self.conn.commit()

    def azureGetData(self):
        try:
            self.cursor.execute("SELECT * FROM data ORDER BY id DESC")
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit (1)
    
    def azureDeleteData(self, id):
        self.cursor.execute("DELETE FROM data WHERE id=?", [id])
        self.conn.commit()
    
    def azureEditData(self, text, id):
        date = datetime.utcnow()
        self.cursor.execute("UPDATE data SET text=?, date=? WHERE id=?", [text, date, id])
        self.conn.commit()
    
    def azureGetDataid(self, id):
        try:
            self.cursor.execute("SELECT * FROM data WHERE id=?", [id])
            data = self.cursor.fetchall()
            return data
        except pypyodbc.DatabaseError as exception:
            print('Failed to execute query')
            print(exception)
            exit (1)