from bokeh.models import ColumnDataSource, Select, CustomJS
from bokeh.plotting import figure, output_file, show, gridplot
from bokeh.models.layouts import VBox, HBox
from action_prob_data import action_prob_dict
import numpy as np

# Use this as a template https://stackoverflow.com/questions/33465827/bokeh-python-use-callback-on-columndatasource-to-change-stacked-bar-chart-with
# My way of doing what you want is to use 4 sources (1 per age group), and then manually change them depending on age group selected. If 15-49 age group is selected, associated source y is centered down (to height / 0), and height of all others is set to 0. I have done the 'all age' group, but not 'age standardized'. And I have not tried to resize figure to see better the Under 5 years group either. Oh, and I also swapped to numpy arrays. It is just a convenience thing, you can keep on with Python lists and Panda frames if you prefer.

# Ask me if you have any further question, Thierry
######################################################
# I think I have to do p1.rect for every player and make the other ones zero if they are not being called.
######################################################
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

player_list = [
    'Draymond Green',
    'Stephen Curry',
    'Chris Bosh',
    'Dwyane Wade'
]

action_list = ['_pass', '_shoot', '_turnover']


#player_name = 'Stephen Curry'
output_file('player_prob2.html')

# Row of zeros. Not sure for what
zeros = np.zeros(len(region))


# get probabilities we need
def get_probs_for_player(player_name):
    # player_prob
    pass_prob = action_prob_dict[player_name].T[0]
    shoot_prob = action_prob_dict[player_name].T[1]
    turnover_prob = action_prob_dict[player_name].T[2]

    # scaled_prob so that
    # the bottom position of the bars is on the 0 line.
    s_pass_prob = pass_prob / 2.0
    s_shoot_prob = shoot_prob / 2.0
    s_turnover_prob = turnover_prob / 2.0

    # y values for stacked bar chart
    stacked_player_pass = s_pass_prob
    stacked_player_shoot = pass_prob + s_shoot_prob
    stacked_player_turnover = pass_prob + shoot_prob + s_turnover_prob

    return (
        pass_prob,
        shoot_prob,
        turnover_prob,
        stacked_player_pass,
        stacked_player_shoot,
        stacked_player_turnover,
        s_pass_prob,
        s_shoot_prob,
        s_turnover_prob
    )


# get info in dictionary form
def get_source_for_callback(player_name):
    (pass_prob,
     shoot_prob,
     turnover_prob,
     stacked_player_pass,
     stacked_player_shoot,
     stacked_player_turnover,
     s_pass_prob,
     s_shoot_prob,
     s_turnover_prob) \
        = get_probs_for_player(player_name)

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

    return player_pass, player_shoot, player_turnover


# def plot_one_player(player_name, dict_of_player_info, p1):
#     # player_pass, player_shoot, player_turnover = get_source_for_callback(player_name)
#     dict_of_player_info[player_name]
#     # Use rect glyphs for stacked bars
#     p1.rect(
#         x='x', y='y',
#         width=0.8, height='height',
#         source=player_pass,
#         color=colour_dict['Pass'], alpha=0.8,
#         name='Pass',
#         legend='pass'
#     )
#     p1.rect(
#         x='x', y='y',
#         width=0.8, height='height',
#         source=player_shoot,
#         color=colour_dict['Shoot'], alpha=0.8,
#         name='Shoot',
#         legend='shoot'
#     )
#     p1.rect(
#         x='x', y='y',
#         width=0.8, height='height',
#         source=player_turnover,
#         color=colour_dict['Turnover'], alpha=0.8,
#         name='Turnover',
#         legend='turnover'
#     )
# 
#     p1.title.text_font_size = '14pt'
#     p1.legend.orientation = 'horizontal'
#     p1.legend.location = 'bottom_left'
# 
#     return p1


def plot_all_players(all_dicts):
    p1 = figure(
        title='Action Probabilities Per Region',
        x_range=region,
        y_range=[0, 1.1], # prob goes to 1
        background_fill_color=colour_dict['background'],
        plot_width=500,
        plot_height=400,
        outline_line_color=None
    )
    for key, value in all_dicts.items():
        if key.split('_')[1] == 'pass':
            p1.rect(
                x='x', y='y',
                width=0.8, height='height',
                source=value,
                color=colour_dict['Pass'], alpha=0.8,
                name='Pass',
                legend='pass'
            )

        elif key.split('_')[1] == 'shoot':
            p1.rect(
                x='x', y='y',
                width=0.8, height='height',
                source=value,
                color=colour_dict['Shoot'], alpha=0.8,
                name='Shoot',
                legend='shoot'
            )

        elif key.split('_')[1] == 'turnover':
            p1.rect(
                x='x', y='y',
                width=0.8, height='height',
                source=value,
                color=colour_dict['Turnover'], alpha=0.8,
                name='Turnover',
                legend='turnover'
            )
    # 
    # 
    # for player in player_list:
    #     p1 = plot_one_player(player, p1)

    p1.title.text_font_size = '14pt'
    p1.legend.orientation = 'horizontal'
    p1.legend.location = 'bottom_left'

    return p1


def create_dict_of_player_info(players):
    dict_of_player_info = {}
    i = 0
    for player in players:
        player_pass, player_shoot, player_turnover = get_source_for_callback(player)
        player_info = {}
        player_info['player' + str(i) + '_pass'] = player_pass
        player_info['player' + str(i) + '_shoot'] = player_shoot
        player_info['player' + str(i) + '_turnover'] = player_turnover
        dict_of_player_info[player] = player_info
        i += 1
    return dict_of_player_info


def combine_all_dicts(dict_of_player_info):
    all_dicts = [values for values in dict_of_player_info.values()]
    return {k: v for d in all_dicts for k, v in d.items()}


def js_string_variables(player_list, action_list):
    var_string = """
        var f = cb_obj.get('value');
    """
    new_var_end = ".get('data');"
    # add player info
    i = 0
    for player in player_list:
        for action in action_list:
            new_var_beg = 'var data' + str(i) + action + ' = ' + 'player' + str(i)
            var_string += '\n' + new_var_beg + action + new_var_end
        i += 1

    return var_string


def js_plot_chosen_player(player_list, action_list, chosen_player):
    idx_player = player_list.index(chosen_player)
    data_source = 'data' + str(idx_player)

    data_str = """ """
    for action in action_list:
        data_str += data_source + action + "['height'] = " + data_source + "['height_full'];" + '\n'
        data_str += data_source + action + "['y'] = " + data_source + "['y_full'];" + '\n'

    return data_str


def js_plot_other_players(player_list, action_list, chosen_player):
    idx_player = player_list.index(chosen_player)
    all_players = [x for x in range(len(player_list)) if x != idx_player]

    data_str = """ """
    for player in all_players:
        for action in action_list:
            data_source = 'data' + str(player)
            data_str += data_source + action + "['height'] = " + data_source + action + "['height_zeros'];" + '\n'

    return data_str


def js_trigger_string(player_list, action_list):
    trigger_str = """ """

    for player in player_list:
        idx_player = player_list.index(player)
        for action in action_list:
            trigger_str += 'player' + str(idx_player) + action + ".trigger('change');"'\n'

    return trigger_str


def js_one_if_statement(player_name, player_list, action_list):
    if_string = "if (f == '" + player_name + "')"
    chosen_player = js_plot_chosen_player(
        player_list=player_list,
        action_list=action_list,
        chosen_player=player_name
    )
    other_players = js_plot_other_players(
        player_list=player_list,
        action_list=action_list,
        chosen_player=player_name
    )
    trigger_string = js_trigger_string(
        player_list=player_list,
        action_list=action_list
    )
    combined_string = (
        if_string + '{'
        + '\n' + chosen_player
        + '\n' + other_players
        + '\n' + trigger_string + '}'
    )
    return combined_string


def js_all_if_statement(player_list, action_list):
    combined_string = """ """
    # initiate variables
    combined_string += js_string_variables(
        player_list=player_list,
        action_list=action_list
    ) + '\n'

    for player in player_list:
        combined_string += js_one_if_statement(
            player_name=player,
            player_list=player_list,
            action_list=action_list
        ) + '\n'
    return combined_string


dict_of_player_info = create_dict_of_player_info(player_list)
all_dicts = combine_all_dicts(dict_of_player_info)
p1 = plot_all_players(all_dicts)
js_code = js_all_if_statement(player_list, action_list)

Callback_Age = CustomJS(
    args=all_dicts,
    code=js_code
)

# Use the Select widget
dropdown_player = Select(
    title="Players:",
    value=player_list[1],
    options=player_list,
    callback=Callback_Age
)

# Display data
filters = VBox(dropdown_player)
tot = HBox(filters, gridplot([[p1]]))
show(tot)



















##############################################    
##############################################
##############################################    
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
    value=players[1],
    options=players,
    callback=Callback_Prob
)

# Display data
filters = VBox(dropdown_player)
tot = HBox(filters, gridplot([[p1]]))
show(tot)

###############################################
from bokeh.models import  Callback, ColumnDataSource, Rect, Select,CustomJS
from bokeh.plotting import figure, output_file, show,  gridplot
from bokeh.models.layouts import VBox,HBox
import numpy as np

#Color Dictionary
redcolor5 = {u'All ages': "#720017", u'70+ years': "#bd0026", u'50-69 years':  "#f03b20", u'15-49 years': "#fd8d3c", u'Under 5 years': "#f4cc63", u'gridline': '#b2ada6', u'background': '#e3e0db', u'axis' : '#aba9a7'}

#Just a sample of my data
country_both = ['China', 'India', 'United States', 'Russia', 'Japan', 'Indonesia', 'Germany', 'United Kingdom', 'Italy', 'Brazil']
ages_gen = ['Under 5 years', '15-49 years', '50-69 years', '70+ years', 'All ages', 'Age-standardized']

height70yr = np.array([919470, 421922, 321125, 193960, 148946, 107822, 97529, 90198, 81107, 76782])
height50to69 = np.array([640496, 626995, 182338, 195472, 40422, 109242, 44161, 33333, 24964, 64429])
height15to49 = np.array([126094, 139420, 26159, 43239, 5480, 39040, 6829, 4163, 3571, 16152])
heightUnder5 = np.array([10210, 43338, 82, 714, 41, 5255, 0, 26, 0, 1201])
zeros = np.zeros(len(country_both))


#Y Values for Stacked bar chart
yUnder5 = heightUnder5 / 2.0
y15to49 = yUnder5 + height15to49/2.0
y50to69 = y15to49 + height50to69/2.0
y70yr = y50to69 + height70yr/2.0


output_file('UW_TobaccoDeath.html')

#Figure for Stacked bar chart
p1 = figure(title="Top Countries with Death Due to Tobacco by Age", 
            x_range=country_both, y_range=[0, np.amax([y70yr+height70yr])],
            background_fill_color=redcolor5['background'], 
            plot_width=700, plot_height = 600,
            outline_line_color= None)


#source for callback
source1 = ColumnDataSource(data=dict(x=country_both, y = yUnder5, y_full = yUnder5, height = heightUnder5, height_full = heightUnder5 ,height_zeros = zeros, y_zeros = heightUnder5 / 2.0))

source2 = ColumnDataSource(data=dict(x=country_both, y = y15to49, y_full = y15to49, height = height15to49, height_full = height15to49,height_zeros = zeros, y_zeros = height15to49 / 2.0))

source3 = ColumnDataSource(data=dict(x=country_both, y = y50to69, y_full = y50to69, height = height50to69, height_full = height50to69,height_zeros = zeros , y_zeros = height50to69 / 2.0))

source4 = ColumnDataSource(data=dict(x=country_both, y = y70yr, y_full = y70yr, height = height70yr, height_full = height70yr,height_zeros = zeros, y_zeros =  height70yr / 2.0))

#Use rect glyphs for stached bars
p1.rect(x ='x', y ='y', width =.8, height = 'height', source = source1, color=redcolor5['Under 5 years'], alpha=0.8, name = "Under 5")
p1.rect(x = 'x', y ='y', width = .8, height ='height', source = source2, color=redcolor5['15-49 years'], alpha=0.8, name = "15 to 49")
p1.rect(x = 'x', y ='y', width = .8, height ='height', source = source3, color=redcolor5['50-69 years'], alpha = .8, name = "50 to 69")
p1.rect(x = 'x', y ='y', width = .8, height ='height', source = source4, color=redcolor5['70+ years'], alpha = .8, name = "70+ yrs")

#Java script Callbacks for age  
#I want this to recognize the 70+ year old drop down selection 
#and change the plot so that the height of the glyph is the same as the y value and the 70 year old glyph is the only one that displays
Callback_Age = CustomJS(args={'source1': source1,'source2': source2,'source3': source3,'source4': source4}, code="""
        var f = cb_obj.get('value');
        var data1 = source1.get('data');
        var data2 = source2.get('data');
        var data3 = source3.get('data');
        var data4 = source4.get('data');
        if (f == 'Under 5 years') {
            data3['height'] = data3['height_zeros'];
            data2['height'] = data2['height_zeros'];
            data4['height'] = data4['height_zeros'];
            data1['y'] = data1['y_zeros'];
            data1['height'] = data1['height_full'];
            source1.trigger('change');
            source2.trigger('change');
            source3.trigger('change');
            source4.trigger('change');
            }
        if (f == '15-49 years') {
            data1['height'] = data1['height_zeros'];
            data3['height'] = data3['height_zeros'];
            data4['height'] = data4['height_zeros'];
            data2['y'] = data2['y_zeros'];
            data2['height'] = data2['height_full'];
            source1.trigger('change');
            source2.trigger('change');
            source3.trigger('change');
            source4.trigger('change');
            }

        if (f == '50-69 years') {
            data1['height'] = data1['height_zeros'];
            data2['height'] = data2['height_zeros'];
            data4['height'] = data4['height_zeros'];
            data3['y'] = data3['y_zeros'];
            data3['height'] = data3['height_full'];
            console.log('data3',data3)
            source1.trigger('change');
            source2.trigger('change');
            source3.trigger('change');
            source4.trigger('change');
            }
        if (f == '70+ years') {
            data1['height'] = data1['height_zeros'];
            data2['height'] = data2['height_zeros'];
            data3['height'] = data3['height_zeros'];
            data4['y'] = data4['y_zeros'];
            data4['height'] = data4['height_full'];
            source1.trigger('change');
            source2.trigger('change');
            source3.trigger('change');
            source4.trigger('change');
            }
        if (f == 'All ages') {
            data1['height'] = data1['height_full'];
            data1['y'] = data1['y_full'];
            data2['height'] = data2['height_full'];
            data2['y'] = data2['y_full'];
            data3['height'] = data3['height_full'];
            data3['y'] = data3['y_full'];
            data4['height'] = data4['height_full'];
            data4['y'] = data4['y_full'];
            source1.trigger('change');
            source2.trigger('change');
            source3.trigger('change');
            source4.trigger('change');
            }



    """)
#Use the Select widget
dropdown_age = Select(title="Ages:", value=ages_gen[4], options= ages_gen,  callback = Callback_Age)

#Display data
filters = VBox(dropdown_age)
tot =  HBox(filters, gridplot([[p1]]))
show(tot)

#######################################################
#######################################################
