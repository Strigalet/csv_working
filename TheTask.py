import re
import plotly
import plotly.graph_objs as go
def getTitle(line):
    result=re.split(r",",line,maxsplit=5)
    return result[0], result[5]
def getDate_and_time(line):
    result = re.split(r",", line, maxsplit=1)
    date_and_time=re.search(r"[0-9]{4}(-|:|\.)(0[1-9]|1[012])(-|:|\.)(0[1-9]|1[0-9]|2[0-9]|3[01])\s([0-1]\d|2[0-3])((-|:|\.)[0-5]\d){2}",result[0])
    return date_and_time[0],result[1]
def getTown(line):
    result = re.split(r",", line, maxsplit=1)
    return result[0],result[1]
def getAddress(line):
    result = re.split(r",", line, maxsplit=1)
    return result[0]

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
equal_addresssese=set()
towns=[]
calls=[]
for town in dataset:
    counter=0
    towns.append(town)
    cheking_address = []
    for address in dataset[town]:
        status = "yes"
        if address in equal_addresssese:
            continue
        equal_addresssese.add(address)
        for i in cheking_address:
            if i!="ST" and i!="AVE" and i!="N" and i!="MAIN" and i!="&" and i!="OLD" and i!= "END" and i!= "DR" and "RD" not in i and i in address:
                status = "no"
                break
        cheking_address += address.split()
        if status!="no":
            for date_and_time in dataset[town][address]:
                counter+=1
    calls.append(counter)

equal_addresssese=set()
empty_dict=dict()
for town in dataset:
    cheking_address = []
    for address in dataset[town]:
        status="yes"
        if address in equal_addresssese:
            continue
        equal_addresssese.add(address)
        for i in cheking_address:
            if i!="ST" and i!="AVE" and i!="N" and i!="MAIN" and i!="&" and i!="OLD" and i!= "END" and i!= "DR" and "RD" not in i and i in address:
                status = "no"
                break
        cheking_address+=address.split()
        if status!="no":
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
