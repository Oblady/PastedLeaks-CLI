#!/usr/bin/env python
#
# PastedLeaks CLI
# (c) 2012 Oblady
# @author : Adrien LUCAS
# Based on http://reflets.info/monkey-tools-reflets-vous-offre-pastedleaks/
#
## Original source code : ###
# Goofile v1.5
# Coded by Thomas (G13) Richards 
# My Website: http://www.g13net.com
# Project Page: http://code.google.com/p/goofile
# TheHarvester used for inspiration
# A many thanks to the Edge-Security team!
# ### 
# 

import string
import httplib
import sys
import re
import getopt

print " PastedLeaks CLI"
print "    based on Goofile by T.Richards"
print "    and http://reflets.info/monkey-tools-reflets-vous-offre-pastedleaks/"
print "  https://github.com/Oblady/PastedLeaks-CLI/"
print " ---\n\n"

global result
result =[]

def usage():
	print "PastedLeaks CLI"
	print "usage: pastedleaks terms"
	print "example: ./pastedleaks.py \"terms\" \"of interest\""
	sys.exit()

def run(userSearch):
	#h = httplib.HTTP('www.google.com')
	h = httplib.HTTPS('encrypted.google.com')
	h.putrequest('GET',"/search?num=500&q="+ userSearch +"+site:pastebin.com+OR+site:friendpaste.com+OR+site:pastebay.com+OR+site:pastebin.ca")
	h.putheader('Host', 'encrypted.google.com')
	#h.putheader('Host', 'www.google.com')
	h.putheader('User-agent', 'Internet Explorer 6.0 ')
	h.putheader('Referrer', 'www.g13net.com')
	h.endheaders()
	returncode, returnmsg, headers = h.getreply()
	data=h.getfile().read()
	data=re.sub('<b>','',data)
	for e in ('>','=','<','\\','(',')','"','http',':','//'):
		data = string.replace(data,e,' ')
	
	r1 = re.compile('[a-zA-Z0-9]*paste[a-zA-Z0-9]*\.c[oma]+/[a-zA-Z0-9_-]{2,}')
	res = r1.findall(data)
	
	return res 
	

def search(argv):

	userSearch = '+'.join(argv)
	if len(userSearch) < 3:
		usage()

	print "Searching for "+ userSearch
	print "========================================\n"

	print "Pasted data found:"
	print "===================="

	res = run(userSearch)

	for x in res:
		if result.count(x) == 0:
			result.append(x)
			
	t=0
	if result==[]:
		print "No results were found"
	else:
		for x in result:
			x= re.sub('<li class="first">','',x)
			x= re.sub('</li>','',x)
			print "http://"+x
			t+=1
	print "===================="
	print "Total found: "+str(t)+"\n"
	

if __name__ == "__main__":
        try: search(sys.argv[1:])
	except KeyboardInterrupt:
		print "Search interrupted by user.."
	except:
		sys.exit()

