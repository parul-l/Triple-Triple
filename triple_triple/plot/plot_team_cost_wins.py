from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


plt.style.use('ggplot')

HEADERS = {
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/45.0.2454.101 Safari/537.36'),
    'referer': 'http://stats.nba.com/player/'
}


def get_json_data(base_url, params):
    response = requests.get(base_url, params=params, headers=HEADERS)

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()


def get_scraping_data_list(url):
    response = requests.get(url)

    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    table_class = 'hh-salaries-ranking-table ' \
                  'hh-salaries-table-sortable responsive'
    table = soup.find(
        'table',
        {'class': table_class})

    data_list = []
    # searches text for salary data
    for row in table.findAll('td'):
        data_list.append(row.text)

    # gets rid of white spaces
    for i in range(len(data_list)):
        data_list[i] = data_list[i].strip()

    return data_list


def money_integer(amount):
    amount = amount[1:]
    return int(amount.replace(',', ''))


def data_list_to_dict(data_list, idx_start=9, idx_step=8):
    data_dict = {}
    for i in range(idx_start, len(data_list), idx_step):
        # value as a list in case I decide to add other years
        value = [
            money_integer(data_list[i + 1]),
        ]
        data_dict[data_list[i].lower()] = value

    return data_dict


def create_dataframe_from_dict(data_dict, col_names):
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    return df.rename(columns=col_names)


def convert_win_loss_to_tuple(raw_list):
    for i in range(len(raw_list)):
        if raw_list[i] is not None:
            split_list = raw_list[i].split('-')
            raw_list[i] = np.array([int(split_list[0]), int(split_list[1])])

    return raw_list


def get_monthly_win_loss_dict(data):
    monthly_win_loss_dict = {}
    for team in data['resultSets'][0]['rowSet']:
        monthly_win_loss_dict[team[3].lower()] = \
            convert_win_loss_to_tuple(team[-12:])

    return monthly_win_loss_dict


def get_cost_per_win(salary, win_loss):
    total_games = np.sum(win_loss)
    win_so_far = win_loss[0]
    cost_so_far = (salary / 82.) * total_games

    return cost_so_far / win_so_far


def plot_cost_win():
    teams = df_team_salary_win_loss.index.values
    scale = 1000000.0
    cost_wins = df_team_salary_win_loss.cost_per_win.values / scale
    cost_game = df_team_salary_win_loss['2016_17_salary'] / (82. * scale)

    N = 30
    ind = np.arange(N)
    width = 0.35
    fig, ax = plt.subplots(1,1, figsize=(15, 16))
    rects1 = ax.bar(ind, cost_wins, width, color='r')
    rects2 = ax.bar(ind + width, cost_game, width, color='b')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('cost (millions)')
    ax.set_title(
        'NBA Team Costs for 2016-2017 Season',
        fontsize=12,
        fontweight='bold'
    )
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(teams, rotation=45)

    ax.legend((rects1[0], rects2[0]), ('cost per win', 'cost per game'))

    ax.annotate(
        '(Source:http://hoopshype.com/salaries/) \n (http://stats.nba.com/)',
        xy=(1, 0.9),
        xycoords='axes fraction',
        fontsize=8,
        xytext=(-5, 5),
        textcoords='offset points',
        ha='right', va='top')

    plt.savefig('Team_cost_win.png')
    plt.tight_layout()
    plt.show()


if '__name__' == '__main__':

    # Get team salaries
    team_salary_url = 'http://hoopshype.com/salaries/'
    team_salary_list = get_scraping_data_list(url=team_salary_url)
    team_salaries_dict = data_list_to_dict(
        data_list=team_salary_list,
        idx_start=9,
        idx_step=8)

    # correct for clippers and lakers
    team_salaries_dict['los angeles lakers'] = \
        team_salaries_dict.pop('la lakers')
    team_salaries_dict['los angeles clippers'] = \
        team_salaries_dict.pop('la clippers')

    # create DataFrame
    df_team_salary = create_dataframe_from_dict(
        data_dict=team_salaries_dict,
        col_names={0: '2016_17_salary'}
    )

    # Get team wins
    nba_base_url = 'http://stats.nba.com/stats/leaguestandingsv3'
    params = {
        'LeagueID': '00',
        'Season': '2016-17',
        'SeasonType': 'Regular Season'
    }

    data = get_json_data(nba_base_url, params)
    monthly_win_loss_dict = get_monthly_win_loss_dict(data)

    # correct for clippers and lakers
    monthly_win_loss_dict['los angeles lakers'] = \
        monthly_win_loss_dict.pop('los angeles')
    monthly_win_loss_dict['los angeles clippers'] = \
        monthly_win_loss_dict.pop('la')

    month_cols = {
        0: 'January',
        1: 'February',
        2: 'March',
        3: 'April',
        4: 'May',
        5: 'June',
        6: 'July',
        7: 'August',
        8: 'September',
        9: 'October',
        10: 'November',
        11: 'December'
    }

    df_win_loss = create_dataframe_from_dict(
        data_dict=monthly_win_loss_dict,
        col_names=month_cols
    )

    df_win_loss_total = df_win_loss.sum(axis=1)

    # join df_team_salary and df_win_loss_total
    df_team_salary_win_loss = pd.concat(
        [df_team_salary, df_win_loss_total],
        axis=1
    )

    # get cost/win
    df_team_salary_win_loss['cost_per_win'] = \
        df_team_salary_win_loss.apply(
            lambda row:
            get_cost_per_win(row['2016_17_salary'], row[0]),
            axis=1
        )

    # plot
    plot_cost_win()
