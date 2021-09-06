from django.http import HttpResponse
from django.template import loader
from django.db import connection


def index(request):
    template = loader.get_template('public/index.html')
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT DATE_FORMAT(create_time, '%Y-%m-%d %H:%i') as date, product_name, pl_rate FROM History ORDER BY create_time DESC")
        rows = cursor.fetchall()

    # 日付
    x_print = []
    for row in rows:
        if row[0] not in x_print:
            x_print.append(row[0])
    # print(x_print)

    data = {}
    for row in rows:
        if row[1] not in data:
            data[row[1]] = []
        data[row[1]].append(row)
    # print(data)
    data_print = {}
    for key, values in data.items():
        # 初期化
        if key not in data_print:
            data_print[key] = []
            for i in range(len(x_print)):
                data_print[key].append("null")

        for item in values:
            index = x_print.index(item[0])
            data_print[key][index] = item[2]

    displayString = ""
    displayString += "['x'," + ','.join("'" + str(x) + "'" for x in x_print) + "],\n"

    for key, value in data_print.items():
        displayString += '["%s", %s],\n' % (key, ','.join(value))

    # それぞれの商品履歴
    eachProduct = {}
    for row in rows:
        if row[1] not in eachProduct:
            eachProduct[row[1]] = {}
        if row[0] not in eachProduct[row[1]]:
            eachProduct[row[1]][row[0]] = row[2]


    #print(eachProduct)
    #print(displayString)

    #context = {'data': "[" + ','.join(data_print) + "]"}
    context = {
        'data': "[" + displayString.rstrip(',') + "]",
        'eachProduct': eachProduct
    }
    return HttpResponse(template.render(context, request))
