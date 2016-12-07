import triple_triple.plot_team_revenue_payroll_wins as plt_payroll

if __name__ == '__main__':
    base_url = "http://stats.nba.com/stats/leaguedashteamstats"
    params = {
        'Conference': '',
        'DateFrom': '',
        'DateTo': '',
        'Division': '',
        'GameScope': '',
        'GameSegment': '',
        'LastNGames': '0',
        'LeagueID': '00',
        'Location': '',
        'MeasureType': 'Base',
        'Month': '0',
        'OpponentTeamID': '0',
        'Outcome': '',
        'PORound': '0',
        'PaceAdjust': 'N',
        'PerMode': 'PerGame',
        'Period': '0',
        'PlayerExperience': '',
        'PlayerPosition': '',
        'PlusMinus': 'N',
        'Rank': 'N',
        'Season': '2015-16',
        'SeasonSegment': '',
        'SeasonType': 'Regular Season',
        'ShotClockRange': '',
        'StarterBench': '',
        'TeamID': '0',
        'VsConference': '',
        'VsDivision': ''
    }

    revenue_url = 'http://www.forbes.com/ajax/list/' + \
        'data?year=2016&uri=nba-valuations&type=organization'

    team_stats = plt_payroll.get_nbastats_team_data(base_url, params)
    win_percent = plt_payroll.get_win_percentage(team_stats)
    team_payroll = plt_payroll.get_team_payroll_data(years_from_current_year=0)
    revenue_data = plt_payroll.get_revenue_data(revenue_url)
    team_revenue = plt_payroll.get_team_revenue(revenue_data)

    payroll_and_wins = plt_payroll.combine_dicts(team_payroll, win_percent)
    revenue_and_wins = plt_payroll.combine_dicts(team_revenue, win_percent)

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

    plt_payroll.plot_data(payroll_and_wins, plot_details_payroll)
    plt_payroll.plot_data(payroll_and_wins, plot_details_revenue)
