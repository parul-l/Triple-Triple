from bokeh.plotting import figure, output_file, show
from bokeh.models.ranges import Range1d
import numpy as np


output_file("line_bar.html")

p = figure(plot_width=400, plot_height=400)

# add a line renderer
#p.line([1, 2, 3, 4, 5], [6, 7, 6, 4, 5], line_width=2)

# setting bar values
h1 = np.array([2, 8, 5, 10, 7, 9])
h2 = np.array([1, 4, 3, 2, 5, 2])
h3 = np.array([12, 3, 7, 3, 3, 4])
# Correcting the bottom position of the bars to be on the 0 line.
adj_h1 = h1/2.
adj_h2 = h1 + 0.5 * h2
adj_h3 = h1 + h2  + 0.5 * h3

# add bar renderer
p.rect(x=[1, 2, 3, 4, 5, 6], y=adj_h1, width=0.4, height=h1, color="#CAB2D6")
p.rect(x=[1, 2, 3, 4, 5, 6], y=adj_h2, width=0.4, height=h2, color='Red')
p.rect(x=[1, 2, 3, 4, 5, 6], y=adj_h3, width=0.4, height=h3, color='Blue')


# Setting the y  axis range   
p.y_range = Range1d(0, 20)


show(p)


adj1 = pass_prob /2.
adj2 = pass_prob + shoot_prob/2.
adj3 = pass_prob + shoot_prob + turnover_prob/2.

p1 = Plot(
    x_range=region,
    y_range=[0, 1.1], # prob goes to 1
    background_fill_color=colour_dict['background'],
    plot_width=500,
    plot_height=400,
    outline_line_color=None
)

p1.Rect(
    x=region, y=adj1,
    width=0.8, height=pass_prob,
    color=colour_dict['Pass'], alpha=0.8,
    name='Pass',
    legend='pass'
)
p1.Rect(
    x=region, y=adj2,
    width=0.8, height=shoot_prob,
    color=colour_dict['Shoot'], alpha=0.8,
    name='Shoot',
    legend='shoot'
)
p1.Rect(
    x=region, y=adj3,
    width=0.8, height=turnover_prob,
    color='Red', alpha=0.8,
    name='Turnover',
    legend='turnover'
)
p1.title.text_font_size = '14pt'
p1.legend.orientation = 'horizontal'
p1.legend.location = 'bottom_left'


from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis, Grid
from bokeh.models.glyphs import Rect
from bokeh.io import curdoc, show

N = 9
x = np.linspace(-2, 2, N)
y = x**2
w = x/15.0 + 0.3
h = y/20.0 + 0.3

source = ColumnDataSource(dict(
    x=[1, 2, 3, 4, 5, 6], y=stacked_player_turnover, w=0.8, h=turnover_prob))

#xdr = DataRange1d()
#ydr = DataRange1d()

plot = Plot(
    title=None, plot_width=300, plot_height=300,
    h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location=None)

glyph = Rect(x="x", y="y", width="w", height="h", angle=-0.7, fill_color="#CAB2D6")
plot.add_glyph(source, glyph)

xaxis = LinearAxis()
plot.add_layout(xaxis, 'below')

yaxis = LinearAxis()
plot.add_layout(yaxis, 'left')

plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

curdoc().add_root(plot)

show(plot)

















import numpy as np
import matplotlib.pyplot as plt

ind = np.arange(3)
d1 = [0.364, 0.643, 0.333]
d2 = [0.636, 0.286, 0.667]
d3 = [0, 0.071, 0]

p1 = plt.bar(ind, d3, color='green')
p2 = plt.bar(ind, d2, color='blue', bottom=d3)
p3 = plt.bar(ind, d1, color='red', bottom=d2)

plt.show()


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

players = ['Stephen Curry', 'Chris Bosh']


output_file('player_prob2.html')

# Row of zeros. Not sure for what
zeros = np.zeros(len(region))
#####################################
#####################################
# player_prob
pass_prob0 = action_prob_dict['Stephen Curry'].T[0]
shoot_prob0 = action_prob_dict['Stephen Curry'].T[1]
turnover_prob0 = action_prob_dict['Stephen Curry'].T[2]

# scaled_prob so that
# the bottom position of the bars is on the 0 line.
s_pass_prob0 = pass_prob0 / 2.0
s_shoot_prob0 = shoot_prob0 / 2.0
s_turnover_prob0 = turnover_prob0 / 2.0

# y values for stacked bar chart
stacked_player_pass0 = s_pass_prob0
stacked_player_shoot0 = pass_prob0 + s_shoot_prob0
stacked_player_turnover0 = pass_prob0 + shoot_prob0 + s_turnover_prob0
#######################################
# player_prob
pass_prob1 = action_prob_dict['Chris Bosh'].T[0]
shoot_prob1 = action_prob_dict['Chris Bosh'].T[1]
turnover_prob1 = action_prob_dict['Chris Bosh'].T[2]

# scaled_prob so that
# the bottom position of the bars is on the 0 line.
s_pass_prob1 = pass_prob1 / 2.0
s_shoot_prob1 = shoot_prob1 / 2.0
s_turnover_prob1 = turnover_prob1 / 2.0

# y values for stacked bar chart
stacked_player_pass1 = s_pass_prob1
stacked_player_shoot1 = pass_prob1 + s_shoot_prob1
stacked_player_turnover1 = pass_prob1 + shoot_prob1 + s_turnover_prob1

#####################################
#####################################

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
player_pass0 = ColumnDataSource(
    data=dict(
        x=region,
        y=stacked_player_pass0,
        y_full=stacked_player_pass0,
        height=pass_prob0,
        height_full=pass_prob0,
        height_zeros=zeros,
        y_zeros=s_pass_prob0,
    )
)

player_shoot0 = ColumnDataSource(
    data=dict(
        x=region,
        y=stacked_player_shoot0,
        y_full=stacked_player_shoot0,
        height=shoot_prob0,
        height_full=shoot_prob0,
        height_zeros=zeros,
        y_zeros=s_shoot_prob0,
    )
)

player_turnover0 = ColumnDataSource(
    data=dict(
        x=region,
        y=stacked_player_turnover0,
        y_full=stacked_player_turnover0,
        height=turnover_prob0,
        height_full=turnover_prob0,
        height_zeros=zeros,
        y_zeros=s_turnover_prob0,
    )
)
#####################################
# Chris Bosh
player_pass1 = ColumnDataSource(
    data=dict(
        x=region,
        y=stacked_player_pass1,
        y_full=stacked_player_pass1,
        height=pass_prob1,
        height_full=pass_prob1,
        height_zeros=zeros,
        y_zeros=s_pass_prob1,
    )
)

player_shoot1 = ColumnDataSource(
    data=dict(
        x=region,
        y=stacked_player_shoot1,
        y_full=stacked_player_shoot1,
        height=shoot_prob1,
        height_full=shoot_prob1,
        height_zeros=zeros,
        y_zeros=s_shoot_prob1,
    )
)

player_turnover1 = ColumnDataSource(
    data=dict(
        x=region,
        y=stacked_player_turnover1,
        y_full=stacked_player_turnover1,
        height=turnover_prob1,
        height_full=turnover_prob1,
        height_zeros=zeros,
        y_zeros=s_turnover_prob1,
    )
)

#####################################
#####################################

# Use rect glyphs for stacked bars
p1.rect(
    x='x', y='y',
    width=0.8, height='height',
    source=player_pass0,
    color=colour_dict['Pass'], alpha=0.8,
    name='Pass',
    legend='pass'
)
p1.rect(
    x='x', y='y',
    width=0.8, height='height',
    source=player_shoot0,
    color=colour_dict['Shoot'], alpha=0.8,
    name='Shoot',
    legend='shoot'
)
p1.rect(
    x='x', y='y',
    width=0.8, height='height',
    source=player_turnover0,
    color=colour_dict['Turnover'], alpha=0.8,
    name='Turnover',
    legend='turnover'
)
########################################
p1.rect(
    x='x', y='y',
    width=0.8, height='height',
    source=player_pass1,
    color=colour_dict['Pass'], alpha=0.8,
    name='Pass',
    legend='pass'
)
p1.rect(
    x='x', y='y',
    width=0.8, height='height',
    source=player_shoot1,
    color=colour_dict['Shoot'], alpha=0.8,
    name='Shoot',
    legend='shoot'
)
p1.rect(
    x='x', y='y',
    width=0.8, height='height',
    source=player_turnover1,
    color=colour_dict['Turnover'], alpha=0.8,
    name='Turnover',
    legend='turnover'
)
##########################################

p1.title.text_font_size = '14pt'
p1.legend.orientation = 'horizontal'
p1.legend.location = 'bottom_left'

js_code = """
    var f = cb_obj.get('value');
    var data_1 = player_pass0.get('data');
    var data_2 = player_shoot0.get('data');
    var data_3 = player_turnover0.get('data');
    var data_4 = player_pass1.get('data');
    var data_5 = player_shoot1.get('data');
    var data_6 = player_turnover1.get('data');
    
    if (f == 'Stephen Curry') {
        data_1['height'] = data_1['height_full'];
        //data_1['y'] = data_1['y_full'];

        data_2['height'] = data_2['height_full'];
        //data_2['y'] = data_2['y_full'];

        data_3['height'] = data_3['height_full'];
        //data_3['y'] = data_3['y_full'];
        
        data_4['height'] = data_4['height_zeros'];
        data_5['height'] = data_5['height_zeros'];
        data_6['height'] = data_6['height_zeros'];
        
        player_pass0.trigger('change');
        player_shoot0.trigger('change');
        player_turnover0.trigger('change');
        player_pass1.trigger('change');
        player_shoot1.trigger('change');
        player_turnover1.trigger('change');
        
        }
    
    if (f == 'Chris Bosh') {
        data_4['height'] = data_4['height_full'];
        data_4['y'] = data_4['y_full'];

        data_5['height'] = data_5['height_full'];
        data_5['y'] = data_5['y_full'];

        data_6['height'] = data_6['height_full'];
        data_6['y'] = data_6['y_full'];

        data_1['height'] = data_1['height_zeros'];
        data_2['height'] = data_2['height_zeros'];
        data_3['height'] = data_3['height_zeros'];

        player_pass0.trigger('change');
        player_shoot0.trigger('change');
        player_turnover0.trigger('change');
        player_pass1.trigger('change');
        player_shoot1.trigger('change');
        player_turnover1.trigger('change');
        }
        
    """

# Java script Callbacks for age
Callback_Prob = CustomJS(
    args={
        'player_pass0': player_pass0,
        'player_shoot0': player_shoot0,
        'player_turnover0': player_turnover0,
        'player_pass1': player_pass1,
        'player_shoot1': player_shoot1,
        'player_turnover1': player_turnover1
        
    },
    code=js_code
)

# Use the Select widget
dropdown_player = Select(
    title="Players:",
    #value=players[1],
    options=players,
    callback=Callback_Prob
)

# Display data
filters = VBox(dropdown_player)
tot = HBox(filters, gridplot([[p1]]))
show(tot)
