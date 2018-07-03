# written for python 2!
# had issues getting mysql working for python 3 :-(

import MySQLdb
import urllib2
import sys

db = MySQLdb.connect("localhost","root","hackathon","cbb")
cursor = db.cursor()



def CheckLinks(url):
	fakes = open("fakesites_{}.txt".format(url),"w")
	countfake = 0
	db = MySQLdb.connect("localhost","root","hackathon","cbb")
	cursor = db.cursor()
	

	q = "select domain, ns from SIDN where domain like '%{}%'".format(url)
	cursor.execute(q)
	#data = cursor.fetchone()
        print ("Finding source DNS for {}".format(url))
	#ns = "ns81.domaincontrol.com"
	#for domain,ns in cursor:a
	for domain,ns in cursor:
		print ("Source is {}".format(ns))

		print ("Scanning for websites from same source, using same html template:")
		q = "select domain, ns from SIDN where ns= '{}'".format(ns)
		c2 = db.cursor()
		c2.execute(q)
		for domain,ns in c2:
			domain = domain.strip()
			#print (domain)

			# see if they contain shopping cart
			try:
			#if True:
				url = "http://www.{}.nl".format(domain)

				content = urllib2.urlopen(url).read()
				if content.find("shopping_cart") > 0 or content.find("checkout") > 0:
					fakes.write("{}\n".format(url))
					countfake = countfake + 1
					print ("{} has simular webshop template, likely bogus!".format(url))
			except:
				f = 1 # skip
			#	print ("error")
			#if countfake > 3:
			#	break
	fakes.close()

url = sys.argv[1:]

if len(url) == 1:
	url = url[0]
	print ("Background check on: {}".format(url))
	CheckLinks(url)
else:
	print ("What you want me to check")








