'''
This is the interface to an SQLite Database
'''

import sqlite3

class GCDbSqlite:
    def __init__(self, dbName='Classes.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Classes (
                clc TEXT PRIMARY KEY,
                subject TEXT,
                units TEXT,
                gpercent TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Classes (
                clc TEXT PRIMARY KEY,
                subject TEXT,
                units TEXT,
                gpercent TEXT)''')
        self.commit_close()

    def get_grades(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Classes')
        classes =self.cursor.fetchall()
        self.conn.close()
        return classes

    def add_class(self, clcode, subj, units, gpercent):
        self.connect_cursor()
        self.cursor.execute('INSERT OR IGNORE INTO Classes (clc, subject, units, gpercent) VALUES (?, ?, ?, ?)', (clcode, subj, units, gpercent))
        self.commit_close()

    def delete_class(self, clcode):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Classes WHERE clc = ?', (clcode,))
        self.commit_close()

    def update_class(self, new_subj, new_units, new_gpercent, clcode):
        self.connect_cursor()
        self.cursor.execute('UPDATE Classes SET subject = ?, units = ?, gpercent = ? WHERE clc = ?', (new_subj, new_units, new_gpercent, clcode))
        self.commit_close()

    def class_exists(self, clcode):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Classes WHERE clc = ?', (clcode,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.get_grades()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

#unit tests
def test_GCDb():
    iGCDb = GCDbSqlite(dbName='GCDbSql.db')
    for entry in range(10000, 10050):
        iGCDb.add_class(str(entry), 'English', '1.0', '75')
        assert iGCDb.class_exists(entry)

    all_entries = iGCDb.get_grades()
    assert len(all_entries) == 50   

    for entry in range(10000, 10030):
        iGCDb.update_class('English', '1.0', '75', str(entry))
        assert iGCDb.class_exists(entry)

    all_entries = iGCDb.get_grades()
    assert len(all_entries) == 50

    for entry in range(10000, 10010):
        iGCDb.delete_class(entry)
        assert not iGCDb.class_exists(entry) 

    all_entries = iGCDb.get_grades()
    assert len(all_entries) == 40

    print("All tests are successful!")
