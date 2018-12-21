# dataset = {city:
#               gender: {
#                         marital_status: {UserID: purchase_sum}
#                       }
#           }


def get_dataset(path):
    dataset = {}
    with open(path) as input_csv:
        input_csv.readline()
        for line in input_csv:
            line = line.split(',')
            if line[5] in dataset:
                if line[2] in dataset[line[5]]:
                    if line[7] in dataset[line[5]][line[2]]:
                        if line[0] in dataset[line[5]][line[2]][line[7]]:
                            dataset[line[5]][line[2]][line[7]][line[0]] += float(line[11])
                        else:
                            dataset[line[5]][line[2]][line[7]][line[0]] = float(line[11])
                    else:
                        dataset[line[5]][line[2]][line[7]] = {line[0]: float(line[11])}
                else:
                    dataset[line[5]][line[2]] = {line[7]: {line[0]: float(line[11])}}
            else:
                dataset[line[5]] = {line[2]: {line[7]: {line[0]: float(line[11])}}}
    return dataset


def male_female_buy(dataset):
    f_sum = 0
    m_sum = 0
    for city in dataset.values():
        for marital_status in city.get('F').values():
            f_sum += sum(marital_status.values())
        for marital_status in city.get('M').values():
            m_sum += sum(marital_status.values())
    return m_sum, f_sum


def city_maritage(dataset):
    cities = {}
    for city in dataset:
        cities[city] = {'married': 0, 'single': 0}
        for gender in dataset[city].values():
            cities[city]['married'] += len(gender.get('1'))
            cities[city]['single'] += len(gender.get('0'))
    return cities
