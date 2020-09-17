from bs4 import BeautifulSoup


with open("example.html", encoding="utf8") as fp:
    soup = BeautifulSoup(fp, features="html.parser")
