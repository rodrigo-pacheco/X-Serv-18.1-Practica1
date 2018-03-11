#!/usr/bin/python3
"""
Simple HTTP Server: shortenrs URLs

Rodrigo Pacheco Martinez-Atienza
r.pachecom @ urjc.es
SAT subject (Universidad Rey Juan Carlos)
"""


import webapp

def check_url(url):
    if url.startswith("http://") or url.startswith("https://"):
        return(url)
    else:
        return("http://" + url)

class URL_shortener(webapp.webApp):
    def parse(self, request):
        try:
            method = request.split()[0]
            resource = request.split()[1]
            url = request.split()[-1]
            url = url.split("=")[-1]
            return(method, resource, url)
        except:
            return("", "")

    def process(self, parsedRequest):
        if parsedRequest[0] == "GET":
            if parsedRequest[1] == "/":
                return ("200 OK", "<html><body><h1>" +
	                              """<form method=post>
	                                 URL:<br>
	                                 <input type="text" name="URL" value="www.realmadrid.com"><br>
	                                 <input type="submit" value="Submit">
	                                 </form>""" +
	                               "</body></html>")
            else:
                return("404 NOT Found", "<html><body><h1> Resource NOT Found</h1>" +
	                                    "<p>Usage: localhost:1234/</p></body></html>")
        elif parsedRequest[0] == "POST":
            checked = check_url(parsedRequest[2])
            # added = add_url(checked)
            return("200 OK", "<html><body><h1>Shortened URL: </h1>" +
                             checked + "</body></html>")
        else:
            return("404 NOT Found", "<html><body><h1> Resource NOT Found</h1>" +
                                    "<p>Usage: localhost:1234/</p></body></html>")

if __name__ == "__main__":
    myApp = URL_shortener("localhost", 1234)
