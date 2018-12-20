import re
import plotly
import plotly.graph_objs as go
def getTitle(line):
    result=re.split(r",",line,maxsplit=5)
    title=re.search(r"[A-Z]+[a-z]*\:\s[A-Z]+[A-Z,\s]*\-?",result[4])
    return title[0], result[5]
def getDate_and_time(line):
    result = re.split(r",", line, maxsplit=1)
    date_and_time=re.search(r"[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])\s([0-1]\d|2[0-3])(:[0-5]\d){2}",result[0])
    return date_and_time[0],result[1]
def getTown(line):
    result = re.split(r",", line, maxsplit=1)
    town=re.search(r"[A-Z]+\s?([A-Z]+\s?)*",result[0])
    if not town:
        return "NO TOWN",result[1]
    return town[0],result[1]
def getAddress(line):
    result = re.split(r",", line, maxsplit=1)
    address=re.search(r"(\w*\s?)+(\&\s)*(\w*\s?)*",result[0])
    if not address:
        return "NO ADDRESS"
    return address[0]

dataset = dict()

try:
    current_line=0
    with open('data/911.csv',mode="r",encoding="utf-8") as file:
        header=file.readline().rstrip()
        good_header=[column.strip().upper() for column in header.split(",")]
        for line in file:
            if not line.rstrip():
                continue
            title,new_line= getTitle(line)
            date_and_time,new_line=getDate_and_time(new_line)
            town,new_line=getTown(new_line)
            address=getAddress(new_line)
            if town in dataset:
                if address in dataset[town]:
                    dataset[town][address][date_and_time] = {
                        "title": title
                    }
                else:
                    dataset[town][address] = {
                        date_and_time: {
                            "title": title
                        }

                    }
            else:
                dataset[town] = {
                    address: {
                        date_and_time: {
                            "title": title
                        }

                    }

                }
            current_line += 1

except IOError as io_error:
    print("Error with file", io_error.errno, io_error.strerror)

except ValueError as v_error:
    print("Error in line",current_line,v_error)

towns=[]
calls=[]
for town in dataset:
    counter=0
    towns.append(town)
    for address in dataset[town]:
        for date_and_time in dataset[town][address]:
            counter+=1
    calls.append(counter)


empty_dict=dict()
for town in dataset:
    for address in dataset[town]:
        for date_and_time in dataset[town][address]:
            if date_and_time in empty_dict:
                empty_dict[date_and_time]+=1
            else:
                empty_dict[date_and_time]=1

figure = { "data" : [
        {
            "x": list(empty_dict.keys()),
            "y": list(empty_dict.values()),
            "type": "scatter",
            "name": "Calls_by_date_and_time",
        },
        {
            "x": towns,
            "y": calls,
            "type": "bar",
            "name": "Calls_by_town_on_Bar",
            "xaxis": "x2",
            "yaxis": "y2"
        },
        {
            "labels": towns,
            "values": calls,
            "type": "pie",
            "name": "Calls_by_town_on_Pie",
            "textinfo": "none",
            'domain': {'x': [0, 0.45], 'y': [0.55, 1]},
        }
    ], "layout" : go.Layout(
            xaxis=dict(domain=[0, 0.45]), yaxis=dict(domain=[0, 0.45]),
            xaxis2=dict(domain=[0.55, 1]), yaxis2=dict(domain=[0, 0.45], anchor='x2'))}


plotly.offline.plot(figure, filename='plololotly.html')
