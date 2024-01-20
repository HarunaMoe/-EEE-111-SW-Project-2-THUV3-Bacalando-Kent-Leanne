from GCalcAppEntry import GradesEntry
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import json

class GCalcDb:
    """
    - simple database to store GradesEntry objects
    """    

    def __init__(self, init=False, dbName='GCalcDb.db'):

        # CSV filename         
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.jsonFile = self.dbName.replace('.db', '.json')
        print(self.jsonFile)

        # initialize container of database entries 
        self.dbList = []
        print('TODO: __init__')

        

    def get_grades(self): ###fetch_employees
  
        print('TODO: get_grades')
        tupleList = self.dbList
        return tupleList

    def add_class(self, clcode, subj, units, gpercent): ### insert_employee

        newEntry = GradesEntry(clcode = clcode, subj = subj, units=units, gpercent=gpercent)
        self.dbList.append((newEntry.clcode, newEntry.subj, newEntry.units, newEntry.gpercent))

        print('TODO: add_class')

    def delete_class(self, clcode):
    
        j = 0
        for i in range(len(self.dbList)):
            if clcode == self.dbList[i][0]:
                j = i
        
        self.dbList.pop(j)

        print('TODO: delete_employee')

    def update_class(self, new_subject, new_units, new_gpercent, clcode):

        for i in range(len(self.dbList)):
            if clcode == self.dbList[i][0]:
                clc_og = self.dbList[i][0]
                self.dbList[i] = (clc_og, new_subject, new_units, new_gpercent)

    def get_gpoint(self, gper):
        gpercent = int(gper)
        if gpercent>=95 and gpercent<=100:
            gpoint = '1.00'
        elif gpercent>=91 and gpercent<95:
            gpoint = '1.25'
        elif gpercent>=87 and gpercent<91:
            gpoint = '1.50'
        elif gpercent>=85 and gpercent<87:
            gpoint = '1.75'
        elif gpercent>=80 and gpercent<85:
            gpoint = '2.00'
        elif gpercent>=75 and gpercent<80:
            gpoint = '2.25'
        elif gpercent>=70 and gpercent<75:
            gpoint = '2.50'
        elif gpercent>=65 and gpercent<70:
            gpoint = '2.75'
        elif gpercent>=60 and gpercent<65:
            gpoint = '3.00'
        elif gpercent>=50 and gpercent<60:
            gpoint = '4.00'
        else:
            gpoint = '5.00'
        
        return gpoint

    def get_gwa(self):
        gwa = 0
        total_u = 0
        for entry in self.dbList:
                gpoint = self.get_gpoint(entry[3])
                gwa = gwa+(float(gpoint)*float(entry[2]))
                total_u += float(entry[2])
        
        gwa = gwa/total_u
        gwa = round(gwa, 3)
        return gwa
    
    
    def display_csv_data(self, path):
        with open(path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            self.dbList = []  # Clear the current data
            x=1
            for row in csv_reader:
                if x!=1:
                    self.dbList.append((row[0], row[1], row[2], row[3]))
                x+=1


    def import_csv(self):
        file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.display_csv_data(file_path) == False

    def export_csv(self):
 
        with open(self.csvFile, "w") as filehandle:
            gwa = self.get_gwa()
            x=1
            filehandle.write(f"Class Code,Subject,Units,Grade Percentage,Grade Point,GWA\n")
            for entry in self.dbList:
                gpoint = self.get_gpoint(entry[3])
                entry = entry+(gpoint, '') 
                if x==1:
                    filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]}, {entry[4]}, {gwa}\n")
                else:
                    filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]}, {entry[4]}\n")
                x+=1
        print('TODO: export_csv')
    
    def export_json(self):
        data_list = []
        gwa = self.get_gwa()
    
        for entry in self.dbList:
            gpoint = self.get_gpoint(entry[3])
            entry = entry + (gpoint, '')
            data_list.append({
                "Class Code": entry[0],
                "Subject": entry[1],
                "Units": entry[2],
                "Grade Percentage": entry[3],
                "Grade Point": entry[4],
            })

        current_gwa = {"Current Gwa": gwa}
        json_data = {"Database": data_list}

        with open(self.jsonFile, "w") as json_file:
            json.dump(current_gwa, json_file)
            json.dump(json_data, json_file, indent=4)
        
        print('TODO: export_json')


    def class_exists(self, clcode):

        for entry in self.dbList:
            if clcode == entry[0]:
                return True
            
        return False
    
    