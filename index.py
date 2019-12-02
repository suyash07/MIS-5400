import pandas as pd
import pyodbc
import requests
from flask import Flask, render_template,request, redirect, url_for
from pandas import DataFrame

app = Flask(__name__)

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/bar')
def bar():
    connection = create_sql_connection()
    resoverall = pd.read_sql_query("SELECT Player, PTS FROM ScorePerGame", connection)

    df = DataFrame(resoverall, columns=['Player', 'PTS'])
    grouped_single = df.groupby(['Player']).agg({'PTS': 'sum'})
    grouped_single.rename(columns={'Player': 'Player', 'PTS': 'Points'}, inplace=True)
    grouped_single.reset_index(drop=False, inplace=True)
    return render_template('bar.html', title='Players Points scored per game', max=grouped_single.Points[:10].max(),
                           labels=grouped_single.Player[:10], values=grouped_single.Points[:10])


@app.route('/line')
def line():
    connection = create_sql_connection()
    resoverall = pd.read_sql_query("SELECT Pos, FG_Percent FROM ScorePerGame", connection)

    df = DataFrame(resoverall, columns=['Pos', 'FG_Percent'])
    grouped_single = df.groupby(['Pos']).agg({'FG_Percent': 'sum'})
    grouped_single.rename(columns={'Pos': 'Position', 'FG_Percent': 'FieldGoalPercentage'}, inplace=True)
    grouped_single.reset_index(drop=False, inplace=True)

    return render_template('line.html', title='Position vs Field Goal percentage',
                           max=grouped_single.FieldGoalPercentage[:10].max(),
                           labels=grouped_single.Pos[:10], values=grouped_single.FieldGoalPercentage[:10])

@app.route('/pie')
def pie():
    connection = create_sql_connection()
    resoverall = pd.read_sql_query("SELECT Player, tHREE_P FROM ScorePerGame", connection)

    df = DataFrame(resoverall, columns=['Player', 'tHREE_P'])
    grouped_single = df.groupby(['Player','tHREE_P']).agg({'tHREE_P': 'sum'})
    grouped_single.rename(columns ={'tHREE_P':'Count'}, inplace=True)
    grouped_single.reset_index(drop=False, inplace=True)
    grouped_single.rename(columns={'Player': 'Player', 'tHREE_P': 'Three_Pointer'}, inplace=True)

    return render_template('piechart.html', title='Player VS Three pointer',
                           max=grouped_single.Three_Pointer[:10].max(),
                           set=zip(grouped_single.Three_Pointer[:10], grouped_single.Player[:10], colors))

@app.route('/graph')
def graph():
    graph_list = ['Line','Bar', 'Pie']

    return render_template("graph.html",
                           title='Graph selector',
                           server_list=graph_list)


@app.route('/about')
def about():
    return render_template('about.html', title='Team Members')


@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('option')
    if select == 'Line':
        return redirect(url_for('line'))
    elif select == 'Bar':
        return redirect(url_for('bar'))
    elif select == 'Pie':
        return redirect(url_for('pie'))
    else:
        return redirect(url_for('about'))

def create_sql_connection():
    server = 'MSI'
    database = 'suyash'

    # creating connection Object which will contain SQL Server Connection
    connection = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database,
        autocommit=True)  # Creating Cursor

    connection.cursor()
    return connection


@app.route('/')
def index():
    response = requests.get("http://localhost:5000/api/v1/cpi/25")
    print(response.status_code)
    print(response.json())
    return '<h2>%s</h2>' % response.json()


@app.route('/age/<int:post_id>')
def show_post(post_id):
    connection = create_sql_connection()
    resoverall = pd.read_sql_query("SELECT * FROM ScorePerGame WHERE Age = '%s'" % post_id, connection)

    df = DataFrame(resoverall)
    return "<html><body>" + df.to_html() + "</body></html>"


if __name__ == "__main__":
    app.run()
