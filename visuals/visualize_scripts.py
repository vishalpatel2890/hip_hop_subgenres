import plotly as plt
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot, plot
from plotly import tools
from plotly.tools import FigureFactory as ff
init_notebook_mode(connected = True)


def create_topic_plot(df):
    data=[]
    for topic in [0,1,2,3,4]:
        years = [1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
        year_data = []
        years_appended =[]
        for x in years:
            try:
                n = (df.groupby(df.release_date.dt.year).topic.value_counts()[x].sort_index()[topic])/df.groupby(df.release_date.dt.year)['count'].sum()[x]
                year_data.append(n)
                years_appended.append(x)
            except:
                pass

        trace0 = go.Scatter(
                x = years_appended,
                y= year_data,
                line=dict(
                shape='spline',
            ),
            marker=dict(
            ),
            name=f'Topic {topic + 1}'
        )
        data.append(trace0)

    layout = dict(
        title = 'Topic Prevalance by Year',
        xaxis=dict(
            title='Year',
            titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#000000'
            )
        ),
        yaxis=dict(
            title='Percentage of All Topics',
            titlefont=dict(
                family='Courier New, monospace',
                size=20
            )
        )
    )
#

    fig = dict(data=data, layout=layout)
    plot(fig, filename='topic_prevalance.html')

def create_spotify_plot(df, spotify_key):
    data=[]
    metric = df.groupby(df.release_date.dt.year).mean()[spotify_key]

    trace0 = go.Scatter(
            x = list(metric.index),
            y= metric,
            line=dict(
            shape='spline',
        ),
        marker=dict(
        ),
        name=f'{spotify_key}'
    )
    data.append(trace0)

    layout = dict(
        title = f'{spotify_key} by Year',
        xaxis=dict(
            title='Year',
            titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#000000'
            )
        ),
        yaxis=dict(
            title=f'{spotify_key}',
            titlefont=dict(
                family='Courier New, monospace',
                size=20
            )
        )
    )
#

    fig = dict(data=data, layout=layout)
    plot(fig, filename=f'visuals/{spotify_key}.html')
