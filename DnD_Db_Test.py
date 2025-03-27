import pyodbc

# Connect to the database
db = pyodbc.connect("DRIVER={SQL Server};"
                    "SERVER=MSI/SQLEXPRESS;"
                    "DATABASE=DnD_Tests;"
                    "Trusted_Connection=yes;")

cursor = db.cursor()
cursor.execute("SELECT * FROM dbo.Spells")

for row in cursor:
    print(row)

