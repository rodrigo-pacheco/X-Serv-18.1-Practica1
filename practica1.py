#!/usr/bin/python3
"""
Simple HTTP Server: shortenrs URLs

Rodrigo Pacheco Martinez-Atienza
r.pachecom @ urjc.es
SAT subject (Universidad Rey Juan Carlos)
"""


import webapp

class randomURL(webapp.webApp):
    # def parse(self, request):
    #     try:
    #         method = received.split()[0]
    #         resource = received.split()[1]
    #         return(method, resource)
    #     except:
    #         return('', '')

    def process(self, parsedRequest):
        rnd_num = random.randint(1, 9999999)
        return ("200 OK", "<html><body><h1>" +
                          "<a href=" + str(rnd_num) + " > Dame otra</a></h1>" +
                          "</body></html>")

if __name__ == "__main__":
    myApp = URL_shortener("localhost", 1234)
