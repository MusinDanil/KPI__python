"""
Зроблено три діаграми які показують:
Кругова - суму витрат чоловіків та жінок
Графік - кількість покупок в залежності від віку
Стовпчикова - кількість чоловіків та жінок у різних вікових категоріях


who_buys_more = {
                 gender: purchase
                }
age_buy_link = {
                age: purchase
               }
age_gender_spread = {
                    age: {'F':count,'M':count}
                    }

"""
import re
import plotly as py
import plotly.graph_objs as go


def get_dataset(path):
    linenumber = 1
    who_buys_more = {'F': 0, 'M': 0}
    age_buy_link = {}
    age_gender_spread = {}
    try:
        with open(path) as inp:
            inp.readline()
            for line in inp:
                linenumber += 1
                line = line.strip().rstrip()
                if not line:
                    continue
                UID, nex = get_element(line)
                PID, nex = get_product_id(nex)
                gender, nex = get_gender(nex)
                age, nex = get_age(nex)
                purchase, nex = get_purchase(line)
                who_buys_more[gender[0]] += purchase
                age = age[0]
                if age in age_buy_link:
                    age_buy_link[age] += purchase
                else:
                    age_buy_link[age] = purchase
                if age in age_gender_spread:
                    age_gender_spread[age][gender[0]] += 1
                else:
                    age_gender_spread[age] = {'F': 0, 'M': 0}
                    age_gender_spread[age][gender[0]] += 1



    except IOError as err:
        print('File ERROR', err.errno, '   ', err.strerror)
    except ValueError as v_err:
        print(line)
        print('Value ERROR', v_err, '   ', linenumber)
    return who_buys_more, age_buy_link, age_gender_spread


def get_element(line):
    result = re.split(r',', line, maxsplit=1)
    element = result[0].strip()
    return element, result[1]


def get_product_id(line):
    element, tail = get_element(line)
    product_id = re.findall(r'P\d{8}', element)
    return product_id, tail


def get_gender(line):
    element, tail = get_element(line)
    result = re.findall(r'[F|M]', element, re.IGNORECASE)
    return result, tail


def get_age(line):
    element, tail = get_element(line)
    result = re.findall(r'\d+\-\d+|55\+', element)
    return result, tail


def get_purchase(line):
    result = re.split(r',', line)[-1]
    element = result.strip()
    return int(element), result[-1::-1]


if __name__ == "__main__":
    labels = ['Women spent', 'Men spent']
    values = list(get_dataset('BlackFriday.csv')[0].values())
    colors = ['#FEBFB3', '#E1396C']
    trace = go.Pie(labels=labels, values=values,
                   hoverinfo='label+percent', textinfo='value',
                   textfont=dict(size=30),
                   marker=dict(colors=colors,
                               line=dict(color='#000000', width=2)))
    dictf = get_dataset('BlackFriday.csv')[1]
    newd = sorted(list(dictf.keys()))
    trace2 = go.Scatter(
        x=newd,
        y=[dictf[a] for a in newd]
    )
    layout = dict(title='Link between age and money spent.',
                  xaxis=dict(title='Age'),
                  yaxis=dict(title='Spent'),
                  )
    dictf2 = get_dataset('BlackFriday.csv')[2]
    newd2 = sorted(list(dictf2.keys()))
    trace11 = go.Bar(
        x=tuple(newd2),
        y=[dictf2[a]['M'] for a in newd2],
        name='Men'
    )
    trace22 = go.Bar(
        x=tuple(newd2),
        y=[dictf2[a]['F'] for a in newd2],
        name='Women'
    )
    data = [trace11, trace22]
    layout = go.Layout(
        barmode='group'
    )

    fig = dict(data=data, layout=layout)
    py.offline.plot([trace], filename='MenOrWomenSpendMoar.html')
    py.offline.plot([trace2], filename='AgeBuyLink.html')
    py.offline.plot(fig, filename='MenWomenInAge.html')