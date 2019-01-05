import pandas as pd

from bkcharts import Bar
from bokeh.embed import components

from bokeh.models.widgets import Panel, Tabs
from bokeh.io import output_file, show
from bokeh.plotting import figure


def plot_bar_sim_game(
    team0_actual,
    team1_actual,
    team0_sim_avg,
    team1_sim_avg,
    team0_sim_std,
    team1_sim_std
):

    # combine sim and actual
    combined0 = zip(team0_sim_avg, team0_actual)
    flat_combine0 = list(sum(combined0, ()))

    combined1 = zip(team1_sim_avg, team1_actual)
    flat_combine1 = list(sum(combined1, ()))

    # duplicate col_sim
    col_sim = [
        'PTS', 'FGA', 'FGM', 'FG3A', 'FG3M',
        'OREB', 'DREB', 'STL', 'BLK', 'TO', 'PASS'
    ]

    col_stats = [val for val in col_sim for _ in (0, 1)]

    df_plot0 = pd.DataFrame(
        data={
            'action': col_stats,
            'values': flat_combine0,
            'result': ['SIM', 'ACTUAL'] * 11
        }
    )

    df_plot1 = pd.DataFrame(
        data={
            'action': col_stats,
            'values': flat_combine1,
            'result': ['SIM', 'ACTUAL'] * 11
        }
    )

    title0 = 'GSW Simulated vs. Actual Results'
    title1 = 'MIA Simulated vs. Actual Results'
    hover_info = [('action', '@action'), ('value', '@height')]

    p0 = Bar(
        df_plot0,
        plot_width=600,
        plot_height=500,
        label='action',
        values='values',
        bar_width=10,
        color=['DeepSkyBlue', 'LightGreen'],
        group='result',
        tooltips=hover_info,
        title=title0,
        legend='top_left',
        toolbar_location='right')

    p1 = Bar(
        df_plot1,
        plot_width=600,
        plot_height=500,
        label='action',
        values='values',
        bar_width=10,
        color=['DeepSkyBlue', 'LightGreen'],
        group='result',
        tooltips=hover_info,
        title=title1,
        legend='top_left',
        toolbar_location='right')

    p0.title.text_font_size = '14pt'
    p1.title.text_font_size = '14pt'

    tab0 = Panel(child=p0, title="GSW")
    tab1 = Panel(child=p1, title="MIA")

    tabs = Tabs(tabs=[tab0, tab1])
    script, div = components(tabs)

    # output_file("test.html")
    # show(tabs)

    return script, div


def box_plot_sim_game(df_results_team):
    # values to represent
    # score, two_pt_shots_attempt/made, three_pt_shots_made/attempts, off/def rebounds

    rel_col = [
        'PTS', 'FGA', 'FGM', 'FG3A', 'FG3M',
        'OREB', 'DREB', 'STL', 'BLK', 'TO', 'PASS'
    ]

    # get quartile info
    # q4=min, q5=max
    q1, q2, q3, q4, q5 = {}, {}, {}, {}, {}

    for col in rel_col:
        q1[col] = df_results_team[col].quantile(q=0.25)
        q2[col] = df_results_team[col].quantile(q=0.50)
        q3[col] = df_results_team[col].quantile(q=0.75)
        q4[col] = df_results_team[col].quantile(q=0.00)
        q5[col] = df_results_team[col].quantile(q=1.00)

    df = pd.DataFrame([q1, q2, q3, q4, q5]).T
    df.columns = ['q{}'.format(i) for i, col in enumerate(df, 1)]

    iqr = df.q3 - df.q1
    upper = df.q3 + 1.5 * iqr
    lower = df.q1 - 1.5 * iqr

    new_upper = [min([x, y]) for (x, y) in zip(df.q5.values, upper.values)]
    new_lower = [max([x, y]) for (x, y) in zip(df.q4.values, lower.values)]

    p = figure(tools="save", background_fill_color="#EFE8E2", title="", x_range=rel_col)
    # stems
    p.segment(rel_col, new_upper, rel_col, df.q3.values, line_color="black")
    p.segment(rel_col, new_lower, rel_col, df.q1.values, line_color="black")

    # boxes
    p.vbar(rel_col, 0.7, df.q2.values, df.q3.values, fill_color='#FF1493', line_color="black")
    p.vbar(rel_col, 0.7, df.q1.values, df.q2.values, fill_color='#1E90FF', line_color="black")

    # whiskers (almost-0 height rects simpler than segments)
    p.rect(rel_col, new_lower, 0.2, 0.01, line_color="black")
    p.rect(rel_col, new_upper, 0.2, 0.01, line_color="black")

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = "white"
    p.grid.grid_line_width = 2
    p.xaxis.major_label_text_font_size = "12pt"

    output_file("box.html")

    show(p)
