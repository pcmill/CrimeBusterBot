# load .NL zone file to database
import os
from flask import Flask
from flask import request

LoadInMemory = True
InitDB = True

if not LoadInMemory:
    import MySQLdb
    database = "cbb"
    dbusername = "cbb"
    dbpassword = "hackathon"

else:
    zoneDB= []


def InitDatabase(dbname):
    db = MySQLdb.connect(host="localhost", user=dbusername, passwd=dbpassword, db=dbname)
    cur = db.cursor()
    sql = "CREATE TABLE SIDN ( ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY , DOMAIN TEXT , NS TEXT );" 
    cur.execute(sql)
    db.commit()

  
def LoadIntoDatabase(dbname):
    db = MySQLdb.connect(host="localhost", user=dbusername, passwd=dbpassword, db=dbname)
    cur = db.cursor()

    zonefile = "/data/nl.zone"
    zfile = open(zonefile,"r")

    line = 0 
    c = 0 
    pvname = ""
    for l in zfile:
        parts = l.split("\t")
        if parts[len(parts)-2] == "NS":
       
            if parts[0] != "":
                pvname = parts[0]
                domain = parts[0]
            else:
                domain = pvname

            ns = parts[len(parts)-1].strip("\n")
            ns = ns.strip(".")
            if domain != "":
                sql = "insert into SIDN (DOMAIN, NS) values(\"{}\",\"{}\");".format(domain,ns)
                #print (sql)
                cur.execute(sql)
            
            line = line + 1
            c = c + 1
            if c  > 10000:
                print (line)
                #db.commit()
                c = 0
                #break


    zfile.close()
    db.commit()
    print ("Loaded {} records".format(line))

def LoadIntoMemory():
    global zoneDB
    
    print ("Reading zonefile into memory, please wait...")
    zonefile = "/data/nl.zone"
    zfile = open(zonefile,"r")

    line = 0
    pvname = ""
    for l in zfile:
        parts = l.split("\t")
        if parts[len(parts)-2] == "NS":

            if parts[0] != "":
                pvname = parts[0]
                domain = parts[0]
            else:
                domain = pvname

            ns = parts[len(parts)-1].strip("\n")
            ns = ns.strip(".")
            zoneDB.append([domain,ns])
            line = line + 1
            

    zfile.close()
    print ("Loaded {} records in memory".format(line))


def FindInMemory(domainname):
    global zoneDB
    r = []
    ns = ""
    for n in zoneDB:
        if n[0]==domainname:
            ns = n[1]
            break
    if ns != "":
        for n in zoneDB:
            if n[1] == ns:
                r.append(n[0])

    return r


# ======================================================
# Main program



app = Flask(__name__)

@app.route('/')
def hello():
    return "found CrimeBusterBot API server !"

@app.route('/match')
def match():
    dname = request.args.get('domain')
    data = FindInMemory(dname)
    r = ""
    for i in data:
        r = r + i + ","
    return r

if __name__ == "__main__":
        
    if not LoadInMemory:
        if InitDB:
            InitDatabase(database)
        LoadIntoDatabase(database)
    else:
        LoadIntoMemory()


    print ("Starting Webservice")

    app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))








