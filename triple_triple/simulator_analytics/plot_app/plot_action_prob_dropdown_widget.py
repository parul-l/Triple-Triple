from bokeh.models import ColumnDataSource, Select, CustomJS
from bokeh.plotting import figure, output_file, show, gridplot
from bokeh.models.layouts import VBox, HBox
from action_prob_data import action_prob_dict
import numpy as np

# Use this as a template https://stackoverflow.com/questions/33465827/bokeh-python-use-callback-on-columndatasource-to-change-stacked-bar-chart-with
# My way of doing what you want is to use 4 sources (1 per age group), and then manually change them depending on age group selected. If 15-49 age group is selected, associated source y is centered down (to height / 0), and height of all others is set to 0. I have done the 'all age' group, but not 'age standardized'. And I have not tried to resize figure to see better the Under 5 years group either. Oh, and I also swapped to numpy arrays. It is just a convenience thing, you can keep on with Python lists and Panda frames if you prefer.

# Ask me if you have any further question, Thierry

# Color Dictionary
colour_dict = {
    u'Turnover': 'LightPink',
    u'Shoot': 'LightGreen',
    u'Pass': 'DeepSkyBlue',
    u'gridline': '#b2ada6',
    u'background': '#e3e0db',
    u'axis': '#aba9a7'
}
# Data
region = [
    'paint',
    'mid_range',
    'top_key',
    'perimeter',
    'back_court',
    'out_of_bounds'
]

players = [
    'Draymond Green',
    'Stephen Curry',
    'Chris Bosh',
    'Dwyane Wade'
]


output_file('test.html')

# Row of zeros. Not sure for what
zeros = np.zeros(len(region))
# player_prob
pass_prob = action_prob_dict['Stephen Curry'].T[0]
shoot_prob = action_prob_dict['Stephen Curry'].T[1]
turnover_prob = action_prob_dict['Stephen Curry'].T[2]

# scaled_prob so that
# the bottom position of the bars is on the 0 line.
s_pass_prob = pass_prob / 2.0
s_shoot_prob = shoot_prob / 2.0
s_turnover_prob = turnover_prob / 2.0

# y values for stacked bar chart
stacked_player_pass = s_pass_prob
stacked_player_shoot = pass_prob + s_shoot_prob
stacked_player_turnover = pass_prob + shoot_prob + s_turnover_prob




# Figure for stacked bar chart
p1 = figure(
    title="Player Action Probabilities Per Region",
    x_range=region,
    y_range=[0, 1.1], # prob goes to 1
    background_fill_color=colour_dict['background'],
    plot_width=500,
    plot_height=400,
    outline_line_color=None
)

# Source for callback
# Steph Curry
player_pass = ColumnDataSource(
    data=dict(
        x=region,
        y=stacked_player_pass,
        y_full=stacked_player_pass,
        height=pass_prob,
        height_full=pass_prob,
        height_zeros=zeros,
        y_zeros=s_pass_prob,
    )
)

player_shoot = ColumnDataSource(
    data=dict(
        x=region,
        y=stacked_player_shoot,
        y_full=stacked_player_shoot,
        height=shoot_prob,
        height_full=shoot_prob,
        height_zeros=zeros,
        y_zeros=s_shoot_prob,
    )
)

player_turnover = ColumnDataSource(
    data=dict(
        x=region,
        y=stacked_player_turnover,
        y_full=stacked_player_turnover,
        height=turnover_prob,
        height_full=turnover_prob,
        height_zeros=zeros,
        y_zeros=s_turnover_prob,
    )
)

# Use rect glyphs for stacked bars
p1.rect(
    x='x', y='y',
    width=0.8, height='height',
    source=player_pass,
    color=colour_dict['Pass'], alpha=0.8,
    name='Pass',
    legend='pass'
)
p1.rect(
    x='x', y='y',
    width=0.8, height='height',
    source=player_shoot,
    color=colour_dict['Shoot'], alpha=0.8,
    name='Shoot',
    legend='shoot'
)
p1.rect(
    x='x', y='y',
    width=0.8, height='height',
    source=player_turnover,
    color=colour_dict['Turnover'], alpha=0.8,
    name='Turnover',
    legend='turnover'
)

p1.title.text_font_size = '14pt'
p1.legend.orientation = 'horizontal'
p1.legend.location = 'bottom_left'

js_code = """
    var f = cb_obj.get('value');
    var data1 = player_pass.get('data');
    var data2 = player_shoot.get('data');
    var data3 = player_turnover.get('data');
    if (f == 'Stephen Curry') {
        data1['height'] = data1['height_full'];
        data1['y'] = data1['y_full'];

        data2['height'] = data2['height_full'];
        data2['y'] = data2['y_full'];

        data3['height'] = data3['height_full'];
        data3['y'] = data3['y_full'];

        player_pass.trigger('change');
        player_shoot.trigger('change');
        player_turnover.trigger('change');
        }
    """

# Java script Callbacks for age
Callback_Age = CustomJS(
    args={
        'player_pass': player_pass,
        'player_shoot': player_shoot,
        'player_turnover': player_turnover
    },
    code=js_code
)

# Use the Select widget
dropdown_player = Select(
    title="Players:",
    value=players[1],
    options=players,
    callback=Callback_Age
)

# Display data
filters = VBox(dropdown_player)
tot = HBox(filters, gridplot([[p1]]))
show(tot)
