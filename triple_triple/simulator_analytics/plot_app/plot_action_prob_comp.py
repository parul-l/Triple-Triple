from bkcharts import Bar, defaults
from bokeh.embed import components
from bkcharts.attributes import cat, color
from bkcharts.operations import blend

from bkcharts import output_file, show


def get_plot_comp(df, player_name):
    values = blend(
        'pass', 'shoot', 'turnover',
        name='action probability',
        labels_name='play_action'
    )
    labels = cat(columns='region', sort=False)
    stacks = cat(columns='play_action', sort=False)
    colors = color(
        columns='play_action',
        palette=['DeepSkyBlue', 'LightGreen', 'LightPink'],
        sort=False
    )
    title = player_name + ' Action Probability per Region'
    hover_info = [('action', '@play_action'), ('prob', '@height')]

    defaults.width = 450
    defaults.height = 450
    bar = Bar(
        df,
        values=values,
        label=labels,
        stack=stacks,
        color=colors,
        legend='bottom_left',
        title=title,
        tooltips=hover_info
    )

    bar.title.text_font_size = '14pt'
    bar.legend.orientation = 'horizontal'
    script, div = components(bar)
    output_file("test_bar.html")
    return script, div, bar
