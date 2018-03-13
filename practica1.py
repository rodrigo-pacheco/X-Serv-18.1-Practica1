#!/usr/bin/python3
"""
Simple HTTP Server: shortenrs URLs

Rodrigo Pacheco Martinez-Atienza
r.pachecom @ alumnos.urjc.es
SAT subject (Universidad Rey Juan Carlos)
"""

hyperlink = """<a href={}>{}</a>"""
form = """<html><body><h1>
        <form method=post accept-charset="utf-8">URL:<br>
        <input type="text" name="URL" value="www.realmadrid.com"><br>
        <input type="submit" value="Submit"></form> {}
        </body></html>"""

init_page = "http://localhost:1234/"

import webapp
import os.path
import collections
from urllib.parse import unquote


URL_NUMBER = collections.OrderedDict()
NUMBER_URL = collections.OrderedDict()
LAST_URL = -1                               # It will be earlier incremented tan assigned (Start at 0)
FILE_PATH = "./init_urls.csv"


def save_in_file(number, url):
    file = open(FILE_PATH, "a")
    file.write(str(number) + "," + url + "\r\n")


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
    html_code = "<p><h2>Shortened URLS:</h2></p>"
    if LAST_URL > -1:
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


def add_url(url, already_added):
    global URL_NUMBER, NUMBER_URL, LAST_URL
    if not(already_added):
        url = url + "\n"
    if url in URL_NUMBER:
        return(url, str(URL_NUMBER[url]))
    else:
        LAST_URL = LAST_URL + 1
        URL_NUMBER[url] = LAST_URL
        NUMBER_URL[LAST_URL] = url
        if not(already_added):                   # 0 When not in .txt file, other number when in file
            save_in_file(LAST_URL, url)
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
                return ("200 OK", form.format(current_url_links()))
            elif its_kown_resource(parsedRequest[1]):
                return("302 Redirect", "<html><body>" +
                                       "<head><meta http-equiv=\"refresh\" content=\"0;URL=" +
                                       NUMBER_URL[its_kown_resource(parsedRequest[1])] +
                                       "\"/></head></body></html>")
            else:
                return("404 NOT Found", "<html><body><h1> Resource NOT Found</h1>" +
                                        hyperlink.format(init_page, "Back to start page") +
                                        "</body></html>")
        elif parsedRequest[0] == "POST" and len(parsedRequest[2]) > 0:
            checked = check_url(parsedRequest[2])
            added = add_url(checked, 0)         # 0 because URL not in .txt file yet
            redirURL = init_page + added[1]
            return("200 OK", "<html><body><h1>Shortened URL: </h1>" + "<p>"  +
                             hyperlink.format(redirURL, added[1]) + " -- " +
                             hyperlink.format(added[0], added[0]) + "</p>" +
                             hyperlink.format(init_page, "Back to start page") +
                             "</body></html>")
        else:
            return("404 NOT Found", "<html><body><h1> Resource NOT Found</h1>" +
                                    "<p>Usage: localhost:1234/number</p>" +
                                    hyperlink.format(init_page, "Click to start page") +
                                    "</body></html>")

if __name__ == "__main__":
    global LAST_URL
    if os.path.exists(FILE_PATH):
        file = open(FILE_PATH, "r")
        for line in file:
            try:
                LAST_URL = int(line.split(",")[0]) - 1  # -1 because in add_url number is increased by 1
                add_url(line.split(",")[1], 1)          # 1 Because URL already in .txt file
            except ValueError:
                print("init_urls.csv format not supported." +
                      "Could not parse line: " + line + "\r"
                      "Usage: number,url\n")
    else:
        file = open(FILE_PATH, "w+")
        os.chmod(FILE_PATH, 0o777)

    file.close
    print(URL_NUMBER)
    myApp = URL_shortener("localhost", 1234)
