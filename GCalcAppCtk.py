from GCalcDb import GCalcDb
from GCalcGuiCtk import GCalcGuiCtk

def main():
    db = GCalcDb(init=False, dbName='GCalcDb.db')
    app = GCalcGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()