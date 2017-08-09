from flask import Flask, render_template, redirect
from action_prob_data import get_prob_df
from plot_action_prob_comp import get_plot_comp


player_prob_app = Flask(__name__)


@player_prob_app.route('/')
def main():
    return redirect('/plot_template')


@player_prob_app.route('/plot_template', methods=['GET', 'POST'])
def index():
    player_name = 'Stephen Curry'
    df = get_prob_df(player_name=player_name)
    script, div, _ = get_plot_comp(df=df, player_name=player_name)

    return render_template('plot_template.html', script=script, div=div)
    # return render_template('test_bar.html')

if __name__ == '__main__':
    player_prob_app.run(port=33507)
