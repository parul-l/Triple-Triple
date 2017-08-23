import itertools
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
from triple_triple.simulator_analytics.action_prob_data import get_prob_df


def get_player_action_prob_data(player_name, visible=False):
    df = get_prob_df(player_name)
    trace1 = go.Bar(
        x=df.region.values,
        y=df['pass'],
        name='pass',
        visible=visible,
        marker={'color': '#82CAFF'}
    )

    trace2 = go.Bar(
        x=df.region.values,
        y=df['shoot'],
        name='shoot',
        visible=visible,
        marker={'color': '#C3FDB8'}
    )

    trace3 = go.Bar(
        x=df.region.values,
        y=df['turnover'],
        name='turnover',
        visible=visible,
        marker={'color': '#FCDFFF'}
    )

    return [trace1, trace2, trace3]


def create_visible_list(player_name, player_list):
    player_idx = player_list.index(player_name)
    # each player has 3 actions (pass, shoot, turnover)
    visible_list = [False] * 3 * len(player_list)
    idx_to_change = [player_idx * 3 + i for i in range(3)]

    # change player's data to True
    map(visible_list.__setitem__, idx_to_change, [True] * 3)

    return visible_list


def player_update_dict(player_name):
    player_dict = {
        'label': player_name,
        'method': 'update',
        'args': [
            {'visible': create_visible_list(player_name, player_list)},
            {'title': player_name + ' Regional Action Probabilities'},
        ]
    }

    return player_dict


def plot_dropdown_player_action_prob(player_list):
    data = list(
        itertools.chain.from_iterable(
            [get_player_action_prob_data(player) for
             player in
             player_list[:-1]]
        )
    )

    # # Add the last player in to player_list
    # # This will be the default plot shown when plot is called
    data.extend(
        get_player_action_prob_data(player_list[-1], visible=True)
    )

    updatemenus = [
        dict(
            active=-1,
            showactive=True,
            buttons=[
                player_update_dict(player_list[0]),
                player_update_dict(player_list[1]),
                player_update_dict(player_list[2]),
                player_update_dict(player_list[3]),
            ]
        )
    ]

    layout = dict(
        title='Player Action Probabilities',
        showlegend=True,
        updatemenus=updatemenus,
        barmode='stack',
        xaxis=dict(tickangle=-45)
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='player-action-prob')
    return offline.offline.plot(fig)


if __name__ == '__main__':
    player_list = [
        'Draymond Green',
        'Stephen Curry',
        'Chris Bosh',
        'Dwyane Wade'
    ]

    # html is used in offline mode
    html = plot_dropdown_player_action_prob(player_list)
