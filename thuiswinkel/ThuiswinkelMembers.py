# Project CrimeBusterBot
# Dutch Open Hackathon 2018
#
# Retrieve all thuiswinkel waarborg members
#
# written by: R.Garsthagen
# coded for Python v3
import requests
import time


def GetMemberDetails(link):
    memberUrl = "https://www.thuiswinkel.org" + link
    m = requests.get(memberUrl)
    if m.status_code == 200:
        namestart = m.text.find("<h1>") + 4
        nameend = m.text.find("</h1>",namestart)
        membername = m.text[namestart:nameend]
        catstring = "<span>Categorieën:</span>"
        catstart = m.text.find(catstring, nameend)
        if catstart > 0:
            catstart = catstart + len(catstring)
            catend = m.text.find("</div>",catstart)
            categorie = m.text[catstart:catend].strip()
        else:
            categorie = ""
            catend = nameend
        webstring = "Website:</strong>"
        webstart = m.text.find(webstring,catend)
        webstart = m.text.find("blank\">", webstart) + 7
        webend = m.text.find("</a>",webstart)
        website = m.text[webstart:webend]
        print (webstart,webend)
        emailstart = m.text.find("fromCharCode(",webend)
        if emailstart > 0:
            emailstart = emailstart + 13
            emailend = m.text.find("));",emailstart)
            emailraw = m.text[emailstart:emailend].split(",")
            emaildecode = ""
            for c in emailraw:
                c = c.strip()
                c = c.strip("(")
                c = c.strip(")")
                vals = c.split("+")
                char = int(vals[0].strip()) + int(vals[1].strip())
                emaildecode = emaildecode + chr(char)
        else:
            emailstart = m.text.find("E-mailadres:",webend)
            emailend = m.text.find("\"",emailstart)
            emaildecode = m.text[emailstart:emailend]
            
        decodestart = emaildecode.find("mailto:")
        if decodestart > 0:
            decodestart = decodestart + 7
            decodeend = emaildecode.find("\"",decodestart)
            email = emaildecode[decodestart:decodeend]
        else:
            email = ""
            emailend = webend
             
        telstring = "Telefoonnummer:</strong>"
        telstart = m.text.find(telstring,emailend)
        if telstart > 0:
            telstart = telstart + len(telstring)
            telend = m.text.find("<br />",telstart)
            telraw = m.text[telstart:telend]
            tel = telraw.strip()
        else:
            tel = ""
            telend = emailend
            

        addstring = "<strong>Vestigingsadres:</strong>"
        addstart = m.text.find(addstring,telend)
        if addstart > 0:
            addstart = addstart + len(addstring)
            addend = m.text.find("<br />",addstart)
            addraw = m.text[addstart:addend]
            address = addraw.strip()
        else:
            address = ""
            
        
        details = link + "\t" + membername + "\t" + categorie + "\t" + website + "\t" + email + "\t" + tel + "\t" + address
    else:
        details = link + ""
    return details

    

baseUrl = "https://www.thuiswinkel.org/ledenlijst/leden-zoeken?showall=true&showhomepage=false&itemsperpage=50&page={}"

page = 1
totalcount = 0
EndOfMembers = False

mfilename = "ThuisWinkel_memberinfo.txt"
mfile = open(mfilename, "w")

while not EndOfMembers:

    url = baseUrl.format(str(page))
    r = requests.get(url)
    if page == 1:
        TotalStart = r.text.find("<h2>Resultaten</h2>")
        Nstart = r.text.find("<h3>", TotalStart) + 4
        Nend = r.text.find("</h3>",Nstart)
        Nlen = Nend-Nstart
        NumberofMembers = int(r.text[Nstart:Nend].split(" ")[0])
        print(NumberofMembers)

    
    # Get all member detail links
    count =0
    pos = 0
    startString = "<div data-equalizeheights=\"footer\">"
    endString = "title"

    while True:
        b = r.text.find(startString,pos)
        if b > 0:
            b = b + len(startString)
            e = r.text.find(endString,b)
            linkraw = r.text[b:e]
            link = linkraw.split("\"")[1]
            count = count + 1
            totalcount = totalcount + 1
            pos = e
            print ("{}: {}".format(totalcount,link))
            details = GetMemberDetails(link)
            print ("{}: {}".format(totalcount,details))
            mfile.write(details + "\n")
        else:
            print ("next page")
            break

    if count != 50:
        EndOfMembers = True
    else:
        page = page + 1

mfile.close()

        
        
            
    


    
    
    





