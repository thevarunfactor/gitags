import requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl
import time
import csv
# Define the URL of the website you want to scrape
base_url = "https://search.ipindia.gov.in/GIRPublic/Application/Details/"

# Loop through all the pages you want to scrape
dfmain = pd.DataFrame()
df = pd.DataFrame()
lis={}
#There are 1055 GI tag pages as of Feb 7, 2022: registered, rejected, being examined etc.
for page_num in range(1,1055):
    # Construct the URL for the current page
    page_url = base_url + str(page_num)

    # Send a request to the website and get the response
    response = requests.get(page_url, verify=False)
    
    #Add sleep so that you don't overload the server
    time.sleep(10)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response with Beautiful Soup
        soup = BeautifulSoup(response.text, "html.parser")
    
        #In the response, find all tables of a particular class 
        table = soup.find('table', class_='tableData responsiveTable')
        
        # Collecting Ddata
        lis = {}
        #Find rows
        for row in table.tbody.find_all('tr'):    
            # Find all data for each column
            columns = row.findAll('td')
            #Store data in list as key, value
            lis[columns[0].text.strip()]=columns[1].text.strip()
    else:
        # If the request was not successful, print an error message
        print("Failed to scrape page {page_num}")
    #Append the new GI data row to data frame
    df=df.append(lis,ignore_index=True)

#Write dataframe into CSV
df.to_csv("D:/GI.csv")
  
