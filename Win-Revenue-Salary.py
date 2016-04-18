from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np
#plt.ion()
plt.style.use('ggplot')

def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)

def combine_dicts(dict1, dict2):
    combined_dictionary = {}
    for key in (dict1.viewkeys() and dict2.keys()):
        if key in dict1: 
            combined_dictionary.setdefault(key, []).append(dict1[key])
        if key in dict2: 
            combined_dictionary.setdefault(key, []).append(dict2[key])
    
    return combined_dictionary 

def team_city_only(string):
    space_index = string[::-1].index(' ')
    parse = string[::-1][space_index:]
    return parse[::-1]   

def team_city_only_revenue(string):
    string = string.replace('-', ' ')
    space_index = string[::-1].index(' ')
    parse = string[::-1][space_index+1:]
    return parse[::-1]        
        

url = "http://hoopshype.com/salaries/"
response = requests.get(url)

data = response.text
soup = BeautifulSoup(data, 'html.parser')

#print(soup.prettify())

table = soup.find('table', {'class': 'hh-salaries-ranking-table hh-salaries-table-sortable responsive'})

salary_list=[]
for row in table.findAll('td'):
    salary_list.append(row.text)            # searches text for salary data
    
for i in range(len(salary_list)):
    salary_list[i]=salary_list[i].strip()   # gets rid of white spaces

def money_integer(amount):
    amount = amount[1:]
    return int(amount.replace(',', ''))

team_salaries = {}
for i in range(9, len(salary_list), 8):        # collect salary and teams
    value = money_integer(salary_list[i+1])
    if salary_list[i] == 'LA Lakers':
        team_salaries['los angeles lakers'] = value
    elif salary_list[i] == 'LA Clippers':
        team_salaries['los angeles clippers'] = value
    else:
        team_salaries[salary_list[i].lower()] = value

##############################
##############################
##############################

win_percent_url = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
data =  get_data(win_percent_url)
response = requests.get(win_percent_url)    

response = requests.get(win_percent_url)
if response.status_code == 200:
    data = response.json()
else:
    print(response.text)
    print(response.status_code)
            
win_percent_inter = {}    
if data is not None:
    for i in range(len(data['resultSets'][0]['rowSet'])):
        if data['resultSets'][0]['rowSet'][i][1] == 'Los Angeles Clippers':
            win_percent_inter['los angeles clippers'] = data['resultSets'][0]['rowSet'][i][5]
        elif data['resultSets'][0]['rowSet'][i][1] == 'Los Angeles Lakers':
            win_percent_inter['los angeles lakers'] = data['resultSets'][0]['rowSet'][i][5]
        else:
            key = team_city_only(data['resultSets'][0]['rowSet'][i][1])
            win_percent_inter[key] = data['resultSets'][0]['rowSet'][i][5]

win_percent = {}
for key in win_percent_inter.keys():
    if key =='Portland Trail ':
        win_percent['portland'] = win_percent_inter['Portland Trail ']
    else:    
        win_percent[key.strip().lower()] = win_percent_inter[key]

salary_win = combine_dicts(team_salaries, win_percent)


 
# ##############################
# ##############################
# ##############################

# PLOT 1 - Win Percentage versus Team Salary
x_values = []
y_values = []

for values in salary_win.values():
    x_values.append(values[0])
    y_values.append(values[1])
    
x_values_array = np.array(x_values)
scale = 1000000.0
x_values_scaled = x_values_array/scale

fig, ax = plt.subplots(1,1, figsize=(6, 6))
ax.plot(x_values_scaled, y_values, 'ro')

fig.suptitle('NBA Season Win Percentages versus Team Salary (2015-16)', fontsize=12, fontweight='bold')
plt.text(73, 0.005, '(Source:http://hoopshype.com/salaries/)')
ax.set_xlabel("Team Salary (in millions)")
ax.set_ylabel("Season Win Percentage")
#    
fig.savefig('Wins_vs_Salary.png') 
plt.show()

##############################
##############################
##############################
    
revenue_url = "http://www.forbes.com/ajax/list/data?year=2016&uri=nba-valuations&type=organization"

data_revenue_inter = get_data(revenue_url)

data_revenue = {}

for i in range(len(data_revenue_inter)):
    if data_revenue_inter[i]['uri'] == 'los-angeles-lakers':
        data_revenue['los angeles lakers'] = data_revenue_inter[i]['revenue']
    elif data_revenue_inter[i]['uri'] == 'los-angeles-clippers':
        data_revenue['los angeles clippers'] = data_revenue_inter[i]['revenue']
    elif data_revenue_inter[i]['uri'] == 'portland-trail-blazers':
        data_revenue['portland'] = data_revenue_inter[i]['revenue']
    else:
        key = team_city_only_revenue(data_revenue_inter[i]['uri'])
        data_revenue[key] = data_revenue_inter[i]['revenue']

revenue_win = combine_dicts(data_revenue, win_percent)
##############################
##############################
##############################
# PLOT 2 - Win Percentage versus Team Revenue
x_values = []
y_values = []

for values in revenue_win.values():
    x_values.append(values[0])
    y_values.append(values[1])

fig, ax = plt.subplots(1,1, figsize=(6, 6))
ax.plot(x_values, y_values, 'bo')

fig.suptitle('NBA Season Win Percentages versus Team Revenue (2015-16)', fontsize=12, fontweight='bold')
plt.text(147, 0.005, '(Source:http://www.forbes.com/nba-valuations/list/)')

ax.set_xlabel("Team Revenue (in millions)")
ax.set_ylabel("Season Win Percentage")
#    
fig.savefig('Wins_vs_Revenue.png') 
plt.show()

##############################
##############################
##############################
