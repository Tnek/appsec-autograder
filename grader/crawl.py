from bs4 import BeautifulSoup as bs
import requests

r = requests.get("http://127.0.0.1:5000/register")
soup = bs(r.text, "html.parser")

uname_form = soup.find("input", id="uname")
print(str(uname_form))
assert uname_form is not None, "Could not find uname input"
