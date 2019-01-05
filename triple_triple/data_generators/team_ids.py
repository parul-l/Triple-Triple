def get_team_ids(team_data):
    team_ids = {}
    team_ids_rev = {}

    for item in team_data['resultSets'][0]['rowSet']:
        team_ids[item[0]] = item[1]
        team_ids_rev[item[1]] = item[0]

    return team_ids, team_ids_rev
