import requests
import json
from bs4 import BeautifulSoup


def get_data_bs(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')  
        return soup
    else:
        print(response.text)
        print(response.status_code)

base_url = "http://espn.go.com/nba/salaries/_/year/"
year = 2016 # If current season is 2015-16, year = 2016
page = 1

def final_url(year, page):
    url = base_url + str(year) + "/page/" + str(page) + "/seasontype/3" 
    return url
    
# Find the number of pages of salaries for each season:
def page_number(url):
    soup = get_data_bs(url)
    for word in soup.findAll(attrs = {'class': 'page-numbers'}):
        total_pages =  int(word.text.rsplit(None, 1)[-1])
    return total_pages    

def reverse_name(playername):
    index = playername.index(' ')
    name = playername[index+1:] + ', ' + playername[:index]
    return name

player_salary_interm = {}
for j in reversed(xrange(2000, 2017)):
    page = 1
    year = j
    url = final_url(year, page)
    total_pages = page_number(url) 
    
    for i in range(1, total_pages+1):
        page = i
        url = final_url(year, page) 
        soup = get_data_bs(url)

        for row in soup.findAll('tr'):
            try:
                int(row.text[0])
                # Extract the name         
                if row.text[1].isalpha():
                    name_forward = row.text.split(',', 1)[0][1:]
                    
                elif row.text[2].isalpha():         
                    name_forward = row.text.split(',', 1)[0][2:]
                
                elif row.text[3].isalpha():         
                    name_forward = row.text.split(',', 1)[0][3:] 
                
                # Extract the team
                inter = row.text.split(', ')[1] 
                team_index = inter.index('$')
                if inter[0] == 'C':
                    team = inter[1:team_index]
                    
                else:
                    team = inter[2:team_index] 

                key = reverse_name(name_forward)
                value = int(row.text.split('$')[1].replace(',', ''))
                player_salary_interm.setdefault(key, [])
                player_salary_interm[key].append([year, value, team])
                
                # Check if player's have same name. Code below only checks if players with same name overlap in their careers. ie. If the same year is present with the same name. 
                
                for key in player_salary_interm:
                    for item in player_salary_interm[key]:
                        years = []
                        years.append(item[0])
                        
                        if len(years) != len(set(years)):
                            print item
                
                # Players with 3 names (need to adjust when joining with stats)
                odd_player_names = []
                for key in player_salary_interm.keys():
                    if len(key.split()) !=2:
                        odd_player_names.append(key)               
            except:
                pass
    
               
