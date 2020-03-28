import requests
from bs4 import BeautifulSoup
import pandas

base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="

r = requests.get(base_url + str(0) + ".html", headers={
        'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})


list_details = []

c = r.content
soup = BeautifulSoup(c, "html.parser")

page_nr = soup.find_all("a",{"class": "Page"})[-1].text

# print(page_nr)

for page in range(0, int(page_nr) * 10, 10):
    # url = base_url + str(page)
    r = requests.get(base_url + str(page) + ".html", headers={
        'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})

    # print(url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    # print(soup.prettify())
    all = soup.find_all("div", {"class": "propertyRow"})
    # print(all)

    for i in range(1, len(all)):
        d = {}
        all_price = all[i].find_all("h4", {"class": "propPrice"})[0].text
        all_price = all_price.strip()
        # print(all_price)
        d["Price"] = all_price
        # print(type(all_h4))
        all_address_0 = all[i].find_all("span", {"class": "propAddressCollapse"})[0].text
        all_address_1 = all[i].find_all("span", {"class": "propAddressCollapse"})[1].text
        # print(all_address_0)
        # print(all_address_1)
        d["Address"] = all_address_0 + " " + all_address_1

        try:
            all_beds = all[i].find_all("span", {"class": "infoBed"})[0].text
            all_beds_number = (all[i].find_all("span", {"class": "infoBed"}))[0].find("b").text
        except:
            all_beds = "No Data Available"
            all_beds_number = "No Data Available"

        try:
            all_infosqft = all[i].find_all("span", {"class": "infoSqFt"})[0].text
            all_infosqft_number = (all[i].find_all("span", {"class": "infoSqFt"}))[0].find("b").text
        except:
            all_infosqft = "No Data Available"
            all_infosqft_number = "No Data Available"

        try:
            all_full_baths = all[i].find_all("span", {"class": "infoValueFullBath"})[0].text
            all_full_baths_number = (all[i].find_all("span", {"class": "infoValueFullBath"}))[0].find("b").text
        except:
            all_full_baths = "No Data Available"
            all_full_baths_number = "No Data Available"

        try:
            all_half_baths = all[i].find_all("span", {"class": "infoValueHalfBath"})[0].text
            all_half_baths_number = (all[i].find_all("span", {"class": "infoValueHalfBath"}))[0].find("b").text

        except:
            all_half_baths = "No Data Available"
            all_half_baths_number = "No Data Available"

        # print(all_beds)
        # print(all_beds_number)
        d["Beds"] = all_beds_number
        # print(all_infosqft)
        # print(all_infosqft_number)
        d["Area"] = all_infosqft_number
        # print(all_full_baths)
        # print(all_full_baths_number)
        d["Full Baths"] = all_full_baths_number
        # print(all_half_baths)
        # print(all_half_baths_number)
        d["Half Baths"] = all_half_baths_number

        for column_group in all[i].find_all("div", {"class": "columnGroup"}):
            # print(column_group)
            for feature_group, feature_name in zip(
                    column_group.find_all("span", {"class": "featureGroup"}),
                    column_group.find_all("span", {"class": "featureName"})):
                # print(feature_group.text)
                # print(feature_name.text)
                # print(type(feature_group))
                # print(type(feature_name))

                if "Lot Size" in feature_group.text:
                    # print(feature_name.text)
                    d["Lot SIze"] = feature_name.text
        #print(d)
        list_details.append(d)
    # print()
#print(list_details)

df = pandas.DataFrame(list_details)
df.to_csv("Output.csv")

print(df)
