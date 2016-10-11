from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')

HEADERS = {
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/45.0.2454.101 Safari/537.36'),
   'referer': 'http://stats.nba.com/player/'
}

def get_nbastats_team_data(base_url, params):
    response = requests.get(base_url, params=params, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        print(response.status_code)

def get_win_percentage(data):
    win_percent = {}
    team_stats = data['resultSets'][0]['rowSet']

    for i in range(len(team_stats)):
        if team_stats[i][1] == 'Los Angeles Clippers':
            win_percent['los angeles clippers'] = team_stats[i][5]
        elif team_stats[i][1] == 'Los Angeles Lakers':
            win_percent['los angeles lakers'] = team_stats[i][5]
        elif team_stats[i][1] == 'Portland Trail Blazers':
            win_percent['portland'] = team_stats[i][5]
        else:
            key = team_city_only(team_stats[i][1]).strip().lower()
            win_percent[key] = team_stats[i][5]

    return win_percent

def get_revenue_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        print(response.status_code)

def get_team_revenue(revenue_data):
    team_revenue = {}

    for i in range(len(revenue_data)):
        if revenue_data[i]['uri'] == 'los-angeles-lakers':
            team_revenue['los angeles lakers'] = revenue_data[i]['revenue']
        elif revenue_data[i]['uri'] == 'los-angeles-clippers':
            team_revenue['los angeles clippers'] = revenue_data[i]['revenue']
        elif revenue_data[i]['uri'] == 'portland-trail-blazers':
            team_revenue['portland'] = revenue_data[i]['revenue']
        else:
            key = team_city_only_revenue(revenue_data[i]['uri'])
            team_revenue[key] = revenue_data[i]['revenue']

    return team_revenue

def get_team_payroll_data(years_from_current_year=0):
    url = "http://hoopshype.com/salaries/"
    response = requests.get(url)

    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    table = soup.find('table', \
                    {'class': 'hh-salaries-ranking-table hh-salaries-table-sortable responsive'})

     # search text for revenue data
    team_payroll=[]
    for row in table.findAll('td'):
        team_payroll.append(row.text)

    # get rid of white spaces
    for i in range(len(team_payroll)):
        team_payroll[i]=team_payroll[i].strip()

    # info starts at idx = 9
    # most recent year: idx+1
    # second most recent year: idx+2, etc.
    team_payroll_dict = {}
    for i in range(9, len(team_payroll), 8):
        value = money_integer(team_payroll[i + (years_from_current_year+1)])
        if team_payroll[i] == 'LA Lakers':
            team_payroll_dict['los angeles lakers'] = value
        elif team_payroll[i] == 'LA Clippers':
            team_payroll_dict['los angeles clippers'] = value
        else:
            team_payroll_dict[team_payroll[i].lower()] = value

    return team_payroll_dict

def plot_data(combined_dict, plot_details_list):
    # plot_details_list = [scale, plot_color, title, source, xlabel,
    #                      ylabel, save_fig_title]

    x_values = []
    y_values = []

    for values in combined_dict.values():
        x_values.append(values[0])
        y_values.append(values[1])

    x_values_array = np.array(x_values)
    scale = plot_details_list[0]
    x_values_scaled = x_values_array/scale

    fig, ax = plt.subplots(1,1, figsize=(6, 6))
    ax.plot(x_values_scaled, y_values, plot_details_list[1])

    fig.suptitle(plot_details_list[2], fontsize=12, fontweight='bold')
    plt.text(73, 0.005, plot_details_list[3])
    ax.set_xlabel(plot_details_list[4])
    ax.set_ylabel(plot_details_list[5])

    fig.savefig(plot_details_list[6])
    plt.show()

def combine_dicts(d1, d2):
    dicts = [d1, d2]
    d = {}
    for k in d1.iterkeys():
        d[k] = tuple(d[k] for d in dicts)
    return d

def team_city_only(string):
    space_index = string[::-1].index(' ')
    parse = string[::-1][space_index:]
    return parse[::-1]

def team_city_only_revenue(string):
    string = string.replace('-', ' ')
    space_index = string[::-1].index(' ')
    parse = string[::-1][space_index + 1:]
    return parse[::-1]

def money_integer(amount):
    amount = amount[1:]
    return int(amount.replace(',', ''))

###########################
###########################

if __name__ == '__main__':
    base_url = "http://stats.nba.com/stats/leaguedashteamstats"
    params = {
        'Conference':'',
        'DateFrom':'',
        'DateTo':'',
        'Division':'',
        'GameScope':'',
        'GameSegment':'',
        'LastNGames':'0',
        'LeagueID':'00',
        'Location':'',
        'MeasureType': 'Base',
        'Month':'0',
        'OpponentTeamID':'0',
        'Outcome':'',
        'PORound':'0',
        'PaceAdjust':'N',
        'PerMode':'PerGame',
        'Period':'0',
        'PlayerExperience':'',
        'PlayerPosition':'',
        'PlusMinus':'N',
        'Rank':'N',
        'Season':'2015-16',
        'SeasonSegment':'',
        'SeasonType':'Regular Season',
        'ShotClockRange':'',
        'StarterBench':'',
        'TeamID':'0',
        'VsConference':'',
        'VsDivision':''
    }

    revenue_url = 'http://www.forbes.com/ajax/list/' + \
        'data?year=2016&uri=nba-valuations&type=organization'

    team_stats = get_nbastats_team_data(base_url, params)
    win_percent = get_win_percentage(team_stats)
    team_payroll  = get_team_payroll_data(years_from_current_year=0)
    revenue_data = get_revenue_data(revenue_url)
    team_revenue = get_team_revenue(revenue_data)

    payroll_and_wins = combine_dicts(team_payroll, win_percent)
    revenue_and_wins = combine_dicts(team_revenue, win_percent)

    plot_details_payroll = [
        1000000.0,
        'ro',
        'NBA Season Win Percentages versus Team Payroll (2016-17)',
        '(Source:http://hoopshype.com/salaries/)',
        'Team Payroll (in millions)',
        'Season Win Percentage',
        'Wins_vs_Team_Payroll.png'
    ]

    plot_details_revenue = [
        1.0,
        'bo',
        'NBA Season Win Percentages versus Team Revenue (2016-17)',
        '(Source:http://www.forbes.com/nba-valuations/list/)',
        'Team Revenue (in millions)',
        'Season Win Percentage',
        'Wins_vs_Team_Revenue.png'
    ]

    plot_data(payroll_and_wins, plot_details_payroll)
    plot_data(payroll_and_wins, plot_details_revenue)
