import sys
import httplib
import re
import itertools
from igraph import *

url = "http://news.ycombinator.com"
depth = 2
search = "python"

# get the parameters or use defaults
if (len(sys.argv) > 1):
	url = sys.argv[1]	

if (len(sys.argv) > 2):
	depth = int(sys.argv[2])

if (len(sys.argv) > 3):
	search = sys.argv[3]

processed = []
trobat = []

def crearxarxa(g):
	titol = ''
	nom = raw_input("\nPlease, enter the name of the file to be saved\n")
	if nom.__len__ > 1:
		titol = nom
	else:
		print 'Error. Specify a name for the file'
	
	try:
	    re = g.write_pajek(titol+".net")
	except IOError:
	    print 'Error', re
	else:
	    print 'ok\n'

	return

def dibuixar(g,trobat):
	print '\nWant to display the graph?\n'
	op = raw_input("yes,no\n")

	if op == "yes":
		plot(g,vertex_label=trobat,bbox=(0, 0, 2500, 2500))
	else:
		exit()
	return


def searchURL(url, depth, search, g, prof, urlant):
	# only do http links
	if (url.startswith("http://") and (not url in processed)):
		processed.append(url)
		
		url = url.replace("http://", "", 1)
		
		# split out the url into host and doc
		host = url
		path = "/"

		urlparts = url.split("/")
		if (len(urlparts) > 1):
			host = urlparts[0]
			path = url.replace(host, "", 1)

		# make the first request
		print "crawling host: " + host + " path: " + path
		conn = httplib.HTTPConnection(host)

		try: #Control d'errors
			req = conn.request("GET", path)
			res = conn.getresponse()

			# find the links
			contents = res.read()
			m = re.findall('href="(.*?)"', contents)

			#ref = depth - (depth-1)
			
			if (search in contents): #si el contingut esta dins del website
				if prof == depth: #afegir el primer node
					print 'Trobat concepte al hub'
					print 'prof i depth:',prof,depth
					g.add_vertex(name=str(url),id=str(url))
					trobat.append(url)
					urlant = url
				else:
					print "Found " + search + " at " + url
					trobat.append(url)
					g.add_vertex(name=str(url),id=str(url))
					print 'url:',url
					print 'urlant:',urlant
					g.add_edge((str(urlant)),(str(url)))
					#busquem a la url que te en comu la paraula
					urlant = url

			print str(depth) + ": processing " + str(len(m)) + " links"
			for href in m: #per tots els enllacos del web
				# do relative urls
				if (href.startswith("/")):
					href = "http://" + host + href


				# follow the links
				if (depth > 0):
					#num+=1
					print "profunditat:",depth,'_______'
					searchURL(href, depth-1, search, g, prof, urlant)

		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror) 
	
		except ValueError:
			print "Could not convert data to an integer."
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise


	else:
		print "skipping " + url
		
g = Graph(1)
g.delete_vertices(0) #esborro el node inicial


urlant='' 
prof = depth
num=0
searchURL(url, depth, search, g, prof, urlant)

print g

crearxarxa(g)

print 'trobat:',trobat

dibuixar(g,trobat) #mostrar graph

