import dash
from dash import dcc, html
import plotly.graph_objs as go
from clib.db_ctx import SqlContext, get_credentials

with SqlContext(**get_credentials()) as sql_context:
    _, yearly_budget = sql_context.execute_query(
        query="SELECT year, total_budget, total_revenue FROM public.budget_revenue_per_year;",
        fetch=True,
    )
    _, movie_y_g = sql_context.execute_query(
        query="SELECT year, movie_count, genre FROM public.movie_genre_yearly_count;",
        fetch=True,
    )

# Process the result into the desired dictionary format
data_budget = {
    'year': [],
    'total_budget': [],
    'total_revenue': []
}

data_count = {
    'year': [],
    'movie': [],
    'genre': []
}

for row in yearly_budget:
    data_budget['year'].append(int(row[0]))
    data_budget['total_budget'].append(row[1])
    data_budget['total_revenue'].append(row[2])

for row in movie_y_g:
    data_count['year'].append(int(row[0]))
    data_count['movie'].append(row[1])
    data_count['genre'].append(row[2])

# Create a dictionary to hold traces for each genre
genre_traces = {}

# Process the data to create traces for each genre
for year, movie, genre in zip(data_count['year'], data_count['movie'], data_count['genre']):
    if genre not in genre_traces:
        genre_traces[genre] = {'year': [], 'movie': []}
    genre_traces[genre]['year'].append(year)
    genre_traces[genre]['movie'].append(movie)

# Create traces for the plot
traces = []
for genre, values in genre_traces.items():
    traces.append(go.Bar(
        x=values['year'],
        y=values['movie'],
        name=genre
    ))

# Define the layout for the plot
layout = go.Layout(
    barmode='stack',
    title='Count of Movies per Year by Genre',
    xaxis={'title': 'Year'},
    yaxis={'title': 'Movie Count'}
)

# Create the figure
fig = go.Figure(data=traces, layout=layout)

# Create Dash app
app = dash.Dash(__name__)

initial_start_date = '2018-01-01'
initial_end_date = '2021-12-31'

# Define app layout
app.layout = html.Div([
    html.H1("SoyHuCe Skander Boudawara"),
    html.H2("Macro analysis on TMDB movies"),
    dcc.Graph(
        id='budget-revenue-graph',
        figure={
            'data': [
                {'x': data_budget['year'], 'y': data_budget['total_budget'], 'type': 'bar', 'name': 'Total Budget'},
                {'x': data_budget['year'], 'y': data_budget['total_revenue'], 'type': 'bar', 'name': 'Total Revenue'}
            ],
            'layout': {
                'xaxis': {'title': 'Year'},
                'yaxis': {'title': 'Amount'},
                'title': 'Budget and Revenue per Year'
            }
        }
    ),
    dcc.Graph(
        id='movies-per-year-graph',
        figure=fig
    )
])

# Run the app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
