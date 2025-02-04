
#import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

#url
first_part_url="https://chicago.craigslist.org/search/chicago-il/cta?"
URL=first_part_url+"lat=41.7434&lon=-87.7104&search_distance=60"
page=requests.get(URL)

url_list=[]

#create a soup
soup = BeautifulSoup(page.content,'html.parser')
results = soup.find(class_='rows')

car_elems = results.find_all('li',class_='result-row')

#extract urls from first page

for car_elem in car_elems:
    url_elem=car_elem.find('a',class_='result-title hdrlnk')['href']
    url_list.append(url_elem)


#extract url from subsequent pages
for i in range(1,25):

    next_url="s="+str(120*i)+"&"
    URL=first_part_url+next_url+"lat=41.7434&lon=-87.7104&search_distance=60"
    page=requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='rows')
    car_elems = results.find_all('li',class_='result-row')
    for car_elem in car_elems:
        url_elem=car_elem.find('a',class_='result-title hdrlnk')['href']
        url_list.append(url_elem)
        
print(len(url_list))

#store urls in a file
df = pd.DataFrame(url_list)
df.columns=["URL"]
writer = pd.ExcelWriter('URL_List_v1.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='urlList', index=False)
writer.save()