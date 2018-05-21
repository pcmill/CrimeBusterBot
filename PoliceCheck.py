# Project CrimeBusterBot
# Dutch Open Hackathon 2018
#
# Query the Dutch Police website to validate if a website, name or number is flagged as 'bogus'
#
# written by: R.Garsthagen
# coded for Python v3


import json
import requests

def CheckURL(search):
    url = "https://www.politie.nl/aangifte-of-melding-doen/controleer-handelspartij.html?_hn:type=action&_hn:ref=r189_r1_r1_r1&query={}"
    finalurl = url.format(search)
    r = requests.post(finalurl)
    alert = "<div class=\"error blok-onderkant-1\" role=\"alert\">"
    noalert = "<div class=\"success blok-onderkant-1\">"

    checkstatus = 0
    try:
        if (r.status_code == 200):
            if alert in r.text:
                # ALERT - site might be bogus
                checkstatus = 1
            elif noalert in r.text:
                # Nothing bad found 
                checkstatus = 2
            else:
                # Error, no respons
                checkstatus = 3
        else:
            # error
            checkstatus = 3
    except:
        checkstatus = 3

    return checkstatus


#Example bogus link
print (CheckURL("www.rtm-info.nl"))

#example normal link
print (CheckURL("www.nu.nl"))









