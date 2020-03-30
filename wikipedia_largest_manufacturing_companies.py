from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_largest_manufacturing_companies_by_revenue"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# print(soup)

table = soup.find('table', {'class': "wikitable sortable plainrowheads"}).find('tbody')
# print(table)

rows = table.find_all('tr')

# print(rows)

columns = [v.text for v in rows[0].find_all('th')]

# print(columns)

df = pd.DataFrame(columns=columns)

for i in range(1, len(rows)):
    tds = rows[i].find_all("td")

    # print(tds)

    if len(tds) == 4:
        values = [tds[0].text, tds[1].text, '', tds[2].text, tds[3].text.replace('\n', '').replace('\xa0', '')]
    else:
        values = [td.text.replace('\n', '').replace('\xa0', '') for td in tds]

    df = df.append(pd.Series(values, index=columns), ignore_index=True)

    print(df)

df.to_csv("wikipedia_largest_companies.csv", index=False)