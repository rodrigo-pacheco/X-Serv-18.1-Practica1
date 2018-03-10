#!/usr/bin/python3
"""
Simple HTTP Server: shortenrs URLs

Rodrigo Pacheco Martinez-Atienza
r.pachecom @ urjc.es
SAT subject (Universidad Rey Juan Carlos)
"""


import webapp

class URL_shortener(webapp.webApp):
    def parse(self, request):
        try:
            method = request.split()[0]
            resource = request.split()[1]
            print("Method: "  method)
            print("Resource: " + resource)
            return(method, resource)
        except:
            return('', '')

    def process(self, parsedRequest):
        print("Ahí va ---------------")
        print(parsedRequest[0])
        if parsedRequest[0] == 'GET':
            return ("200 OK", "<html><body><h1>" +
                              """<form>
                                    URL:<br>
                                    <input type="text" name="URL" value="www.realmadrid.com"><br>
                                    <input type="submit" value="Submit">
                                 </form>""" +
                              "</body></html>")
        else:
            return("404 NOT Found", "<html><body><h1> Resource NOT Found</h1>" +
                                    "<p>Usage: localhost:1234/GET/</p></body></html>")                     

if __name__ == "__main__":
    myApp = URL_shortener("localhost", 1234)
