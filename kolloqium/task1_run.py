import task1 as ds_proc
import plotly as py
import plotly.graph_objs as go

dataset = ds_proc.get_dataset('BlackFriday.csv')
labels = ['Men spent', 'Women spent']
values = ds_proc.male_female_buy(dataset)
colors = ['#FEBFB3', '#E1396C']
trace = go.Pie(labels=labels, values=values,
               hoverinfo='label+percent', textinfo='value',
               textfont=dict(size=20),
               marker=dict(colors=colors,
                           line=dict(color='#000000', width=2)))
cities = ds_proc.city_maritage(dataset)
bars = go.Bar(
            x=tuple(cities.keys()),
            y=tuple(cities.values())
    )

trace1 = go.Bar(
    x=tuple(cities.keys()),
    y=tuple([val['married'] for val in cities.values()]),
    name='Married'
)
trace2 = go.Bar(
    x=tuple(cities.keys()),
    y=tuple([val['single'] for val in cities.values()]),
    name='Single'
)

data = [trace1, trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig, filename='grouped_bar.html')


py.offline.plot([trace], filename='styled_pie_chart.html')
trace = go.Pie(labels=labels, values=values)

