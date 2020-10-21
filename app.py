from flask import Flask, render_template, jsonify, request
from dubl import get_dubl
from graph import get_result
import json


app = Flask(__name__)


@app.route('/clear-potential-spy', methods=['GET'])
def clear_spy():
    CONF = json.loads(open('conf.json', 'r').read())
    FLIGHTS_NUMBER = CONF['FLIGHTS_NUMBER']
    SPY_LIST = CONF['SPY_LIST']
    CONF['POTENTIAL_SPY_LIST'] = []
    json.dump(CONF, open('conf.json', 'w'), indent=4)
    info={}
    cur_spy_name = ''
    if SPY_LIST:
        info = get_result(SPY_LIST[0])
        cur_spy_name = SPY_LIST[0]
    else:
        info = {'nodes_info': [], 'edges_info': []}
        cur_spy_name = 'None'
    return render_template('out.html', multidigraph=CONF['MULTIDIGRAPH'], time_in_city=CONF['TIME_IN_CITY'], potential_spy_list=[], current_spy_name=cur_spy_name, flights_number=FLIGHTS_NUMBER, spy_list=SPY_LIST, nodes_info=info['nodes_info'], edges_info=info['edges_info'])


@app.route('/add-potential-spy', methods=['GET'])
def add_spy():
    potential_spy_name = request.args.get('potential_spy_name')
    CONF = json.loads(open('conf.json', 'r').read())
    FLIGHTS_NUMBER = CONF['FLIGHTS_NUMBER']
    SPY_LIST = CONF['SPY_LIST']
    POTENTIAL_SPY_LIST = CONF['POTENTIAL_SPY_LIST']
    POTENTIAL_SPY_LIST.append(potential_spy_name)
    CONF['POTENTIAL_SPY_LIST'] = POTENTIAL_SPY_LIST
    json.dump(CONF, open('conf.json', 'w'), indent=4)
    for ps in POTENTIAL_SPY_LIST:
        if ps in SPY_LIST:
            SPY_LIST.remove(ps)
    info={}
    cur_spy_name = ''
    if SPY_LIST:
        info = get_result(SPY_LIST[0])
        cur_spy_name = SPY_LIST[0]
    elif POTENTIAL_SPY_LIST:
        info = get_result(POTENTIAL_SPY_LIST[0])
        cur_spy_name = POTENTIAL_SPY_LIST[0]
    else:
        info = {'nodes_info': [], 'edges_info': []}
        cur_spy_name = 'None'
    return render_template('out.html', multidigraph=CONF['MULTIDIGRAPH'], time_in_city=CONF['TIME_IN_CITY'], potential_spy_list=POTENTIAL_SPY_LIST, current_spy_name=cur_spy_name, flights_number=FLIGHTS_NUMBER, spy_list=SPY_LIST, nodes_info=info['nodes_info'], edges_info=info['edges_info'])


@app.route('/create', methods=['GET'])
def create():
    CONF = json.loads(open('conf.json', 'r').read())
    FLIGHTS_NUMBER = CONF['FLIGHTS_NUMBER']
    SPY_LIST = CONF['SPY_LIST']
    POTENTIAL_SPY_LIST = CONF['POTENTIAL_SPY_LIST']
    for ps in POTENTIAL_SPY_LIST:
        if ps in SPY_LIST:
            SPY_LIST.remove(ps)
    spy_name = request.args.get('spy_name')
    info = get_result(spy_name)
    return render_template('out.html', multidigraph=CONF['MULTIDIGRAPH'], time_in_city=CONF['TIME_IN_CITY'], potential_spy_list=POTENTIAL_SPY_LIST, current_spy_name=spy_name, flights_number=FLIGHTS_NUMBER, spy_list=SPY_LIST, nodes_info=info['nodes_info'], edges_info=info['edges_info'])


@app.route('/update-list', methods=['GET'])
def update_list():
    if request.args.get('flights_number'):
        flights_number = int(request.args.get('flights_number'))
        CONF = json.loads(open('conf.json', 'r').read())
        CONF['FLIGHTS_NUMBER'] = flights_number
        TIME_IN_CITY = CONF['TIME_IN_CITY']
        SPY_LIST = get_dubl(flights_number, TIME_IN_CITY, CONF['MULTIDIGRAPH'])
        CONF['SPY_LIST'] = SPY_LIST
        json.dump(CONF, open('conf.json', 'w'), indent=4)
        POTENTIAL_SPY_LIST = CONF['POTENTIAL_SPY_LIST']
        for ps in POTENTIAL_SPY_LIST:
            if ps in SPY_LIST:
                SPY_LIST.remove(ps)
        info={}
        cur_spy_name = ''
        if SPY_LIST:
            info = get_result(SPY_LIST[0])
            cur_spy_name = SPY_LIST[0]
        elif POTENTIAL_SPY_LIST:
            info = get_result(POTENTIAL_SPY_LIST[0])
            cur_spy_name = POTENTIAL_SPY_LIST[0]
        else:
            info = {'nodes_info': [], 'edges_info': []}
            cur_spy_name = 'None'
        return render_template('out.html', multidigraph=CONF['MULTIDIGRAPH'], time_in_city=TIME_IN_CITY, potential_spy_list=POTENTIAL_SPY_LIST, current_spy_name=cur_spy_name, flights_number=flights_number, spy_list=SPY_LIST, nodes_info=info['nodes_info'], edges_info=info['edges_info'])
    if request.args.get('time_in_city'):
        time_in_city = int(request.args.get('time_in_city'))
        CONF = json.loads(open('conf.json', 'r').read())
        CONF['TIME_IN_CITY'] = time_in_city
        SPY_LIST = get_dubl(CONF['FLIGHTS_NUMBER'], time_in_city, CONF['MULTIDIGRAPH'])
        CONF['SPY_LIST'] = SPY_LIST
        json.dump(CONF, open('conf.json', 'w'), indent=4)
        POTENTIAL_SPY_LIST = CONF['POTENTIAL_SPY_LIST']
        for ps in POTENTIAL_SPY_LIST:
            if ps in SPY_LIST:
                SPY_LIST.remove(ps)
        info={}
        cur_spy_name = ''
        if SPY_LIST:
            info = get_result(SPY_LIST[0])
            cur_spy_name = SPY_LIST[0]
        elif POTENTIAL_SPY_LIST:
            info = get_result(POTENTIAL_SPY_LIST[0])
            cur_spy_name = POTENTIAL_SPY_LIST[0]
        else:
            info = {'nodes_info': [], 'edges_info': []}
            cur_spy_name = 'None'
        return render_template('out.html', multidigraph=CONF['MULTIDIGRAPH'], time_in_city=time_in_city, potential_spy_list=POTENTIAL_SPY_LIST, current_spy_name=cur_spy_name, flights_number=CONF['FLIGHTS_NUMBER'], spy_list=SPY_LIST, nodes_info=info['nodes_info'], edges_info=info['edges_info'])
    if request.args.get('multidigraph'):
        multidigraph = bool(int(request.args.get('multidigraph')))
        CONF = json.loads(open('conf.json', 'r').read())
        CONF['MULTIDIGRAPH'] = multidigraph
        SPY_LIST = get_dubl(CONF['FLIGHTS_NUMBER'], CONF['TIME_IN_CITY'], multidigraph)
        CONF['SPY_LIST'] = SPY_LIST
        json.dump(CONF, open('conf.json', 'w'), indent=4)
        POTENTIAL_SPY_LIST = CONF['POTENTIAL_SPY_LIST']
        for ps in POTENTIAL_SPY_LIST:
            if ps in SPY_LIST:
                SPY_LIST.remove(ps)
        info={}
        cur_spy_name = ''
        if SPY_LIST:
            info = get_result(SPY_LIST[0])
            cur_spy_name = SPY_LIST[0]
        elif POTENTIAL_SPY_LIST:
            info = get_result(POTENTIAL_SPY_LIST[0])
            cur_spy_name = POTENTIAL_SPY_LIST[0]
        else:
            info = {'nodes_info': [], 'edges_info': []}
            cur_spy_name = 'None'
        return render_template('out.html', multidigraph=multidigraph, time_in_city=CONF['TIME_IN_CITY'], potential_spy_list=POTENTIAL_SPY_LIST, current_spy_name=cur_spy_name, flights_number=CONF['FLIGHTS_NUMBER'], spy_list=SPY_LIST, nodes_info=info['nodes_info'], edges_info=info['edges_info'])


@app.route('/', methods=['GET'])
def main():
    CONF = json.loads(open('conf.json', 'r').read())
    FLIGHTS_NUMBER = CONF['FLIGHTS_NUMBER']
    TIME_IN_CITY = CONF['TIME_IN_CITY']
    SPY_LIST = CONF['SPY_LIST']
    POTENTIAL_SPY_LIST = CONF['POTENTIAL_SPY_LIST']
    for ps in POTENTIAL_SPY_LIST:
        if ps in SPY_LIST:
            SPY_LIST.remove(ps)
    info={}
    cur_spy_name = ''
    if SPY_LIST:
        info = get_result(SPY_LIST[0])
        cur_spy_name = SPY_LIST[0]
    elif POTENTIAL_SPY_LIST:
        info = get_result(POTENTIAL_SPY_LIST[0])
        cur_spy_name = POTENTIAL_SPY_LIST[0]
    else:
        info = {'nodes_info': [], 'edges_info': []}
        cur_spy_name = 'None'
    return render_template('out.html', multidigraph=CONF['MULTIDIGRAPH'], time_in_city=TIME_IN_CITY, potential_spy_list=POTENTIAL_SPY_LIST, current_spy_name=cur_spy_name, flights_number=FLIGHTS_NUMBER, spy_list=SPY_LIST, nodes_info=info['nodes_info'], edges_info=info['edges_info'])


if __name__ == '__main__':
    CONF = json.loads(open('conf.json', 'r').read())
    FLIGHTS_NUMBER = CONF['FLIGHTS_NUMBER']
    TIME_IN_CITY = CONF['TIME_IN_CITY']
    MULTIDIGRAPH = CONF['MULTIDIGRAPH']
    SPY_LIST = get_dubl(FLIGHTS_NUMBER, TIME_IN_CITY, MULTIDIGRAPH)
    CONF['SPY_LIST'] = SPY_LIST
    json.dump(CONF, open('conf.json', 'w'), indent=4)
    app.run(port=5000, debug=True)