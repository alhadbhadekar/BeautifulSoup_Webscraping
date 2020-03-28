import requests
from bs4 import BeautifulSoup

headers = {'User-agent': 'Mozilla/5.0 Firefox/72.0'}
r = requests.get("https://pythonhow.com/example.html", headers=headers)

c = r.content

print(c)

soup = BeautifulSoup(c, "html.parser")

print(soup.prettify())

all_divs = soup.find_all("div", {"class": "cities"})

print()
print()
print(all_divs)

for i in range(len(all_divs)):
    all_h2 = all_divs[i].find_all("h2")[0].text
    all_p = all_divs[i].find_all("p")[0].text
    # print()
    print()
    print("length of all_h2: ", len(all_h2))
    print(all_h2)
    print(all_p)
