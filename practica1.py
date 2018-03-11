#!/usr/bin/python3
"""
Simple HTTP Server: shortenrs URLs

Rodrigo Pacheco Martinez-Atienza
r.pachecom @ urjc.es
SAT subject (Universidad Rey Juan Carlos)
"""


import webapp
from urllib.parse import unquote


URL_NUMBER = {}
NUMBER_URL = {}
LAST_URL = 0

def its_kown_resource(input_str):
    try:
        input_number = int(input_str.split("/")[1])
        if input_number in NUMBER_URL:
            return input_number
        else:
            return 0    # Number not in dictionary
    except:
        return 0        # Not even a number

def current_url_links():
    global URL_NUMBER, NUMBER_URL, LAST_URL
    html_code = "<p><h2>Shortened URLS:</h2></p>"
    if LAST_URL > 0:
        for url in URL_NUMBER:
            html_code += ("<p><a href=" + url + ">" + str(URL_NUMBER[url]) + "</a>" + " -- " +
                             "<a href=" + url + ">" + url + "</a></p>")
    else:
        html_code += "Not any URL shortened yet. What are you waiting for?"
    return(html_code)


def check_url(url):
    url = unquote(url)
    if url.startswith("http://") or url.startswith("https://"):
        return(url)
    else:
        return("http://" + url)

def add_url(url):
    global URL_NUMBER, NUMBER_URL, LAST_URL
    if url in URL_NUMBER:
        return(url, str(URL_NUMBER[url]))
    else:
        LAST_URL = LAST_URL + 1
        URL_NUMBER[url] = LAST_URL
        NUMBER_URL[LAST_URL] = url
        return(url, str(LAST_URL))


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
	                              """<form method=post accept-charset="utf-8">
	                                 URL:<br>
	                                 <input type="text" name="URL" value="www.realmadrid.com"><br>
	                                 <input type="submit" value="Submit">
	                                 </form>""" +
                                     current_url_links() +
	                               "</body></html>")
            elif its_kown_resource(parsedRequest[1]):
                return("200 OK", "<html><body><h1>HOLAAAAAAAAA</h1></body></html>")
            else:
                return("404 NOT Found", "<html><body><h1> Resource NOT Found</h1>" +
	                                    "<p>Go to <a href=http://localhost:1234/> home page</a></h1>" + 
                                        " to check URLs already shortened</p></body></html>")
        elif parsedRequest[0] == "POST":
            checked = check_url(parsedRequest[2])
            added = add_url(checked)
            return("200 OK", "<html><body><h1>Shortened URL: </h1>" +
                             "<a href=" + added[0] + ">" + added[1] + "</a></h1>" + " -- "
                             "<a href=" + added[0] + ">" + added[0] + "</a></h1>" +
                             "<p><a href=http://localhost:1234/>Back to start page</a></h1></p>" +
                             "</body></html>")
        else:
            return("404 NOT Found", "<html><body><h1> Resource NOT Found</h1>" +
                                    "<p>Usage: localhost:1234/</p></body></html>")

if __name__ == "__main__":
    myApp = URL_shortener("localhost", 1234)
