import os
import sys
import csv
import copy
import argparse

#------------------------------------------------------------------------------#

NODES = {}
EDGES = {}
NODES_MODEL = { 'id': 0,
                'name': '',
                'year': 0,
                'list_of_sons': set([]),
                'list_of_grandsons': set([]),
                'list_of_fathers': set([]),
                'list_of_brothers': set([]),
                'list_of_nephews': set([]),
                'paradox_sons': None,
                'paradox_fathers': None,
                'paradox_brothers': None}
EDGES_MODEL = { 'source': 0,
                'target': 0,
                'finished_in': 0}
NUMBER_OF_NODES = len(NODES)
PARADOX_SONS_COUNTING = { None: 0, True: 0, False : 0 }
PARADOX_FATHERS_COUNTING = { None : 0, True: 0, False : 0 }
PARADOX_BROTHERS_COUNTING = { None: 0, True: 0, False : 0 }
PARADOX_VALUE_OVER_YEARS_FATHERS = {}
PARADOX_VALUE_OVER_YEARS_BROTHERS = {}
PARADOX_VALUE_OVER_YEARS_SONS = {}

#------------------------------------------------------------------------------#

def  manage_args(args):
    if not os.path.isdir("./results_"+args.directory):
        print("Sorry! The directory '"'{}'"' does not exists. "
            "Try again!".format(args.directory))
        sys.exit()
    path = args.directory.split('/')
    return path[len(path)-1]


#------------------------------------------------------------------------------#

def fill_the_dictionaries(filename):
    global NUMBER_OF_NODES
    file_path_nodes = './results_'+filename+'/nodes_'+filename+'.csv'
    file_path_edges = './results_'+filename+'/edges_'+filename+'.csv'

    nodes_csv_input = csv.DictReader(open('./results_'+filename+'/nodes_'+filename+'.csv'))
    edges_csv_input = csv.DictReader(open('./results_'+filename+'/edges_'+filename+'.csv'))

    nodes_dictionary = {}
    edges_dictionary = {}
    artifficial_key = 0

    for line in nodes_csv_input:
        nodes_dictionary = copy.deepcopy(NODES_MODEL)
        #print('linha é "{}"'.format(line))
        nodes_dictionary['id'] = int(line['id'])
        nodes_dictionary['name'] = line['name']
        try:
            nodes_dictionary['year'] = int(line['year'])
        except:
            pass
        NODES[nodes_dictionary['id']] = nodes_dictionary

    for line in edges_csv_input:
        edges_dictionary = copy.deepcopy(EDGES_MODEL)
        edges_dictionary['source'] = int(line['source'])
        edges_dictionary['target'] = int(line['target'])
        EDGES[artifficial_key] = edges_dictionary
        artifficial_key+=1
    NUMBER_OF_NODES = len(NODES)

#------------------------------------------------------------------------------#

def fill_the_lists():
    for edge in EDGES.values():
        NODES[edge['source']]['list_of_sons'].add(edge['target'])
        NODES[edge['target']]['list_of_fathers'].add(edge['source'])
    for node in NODES.values():
        #print(node['list_of_fathers'])
        for father in node['list_of_fathers']:
            #print(NODES[father]['list_of_sons'])
            for brother in NODES[father]['list_of_sons']:
                if brother != node['id']:
                    node['list_of_brothers'].add(brother)
        for son in node['list_of_sons']:
            for grandson in NODES[son]['list_of_sons']:
                node['list_of_grandsons'].add(grandson)
                #print(grandson)
        for brother in node['list_of_brothers']:
            for nephew in NODES[brother]['list_of_sons']:
                node['list_of_nephews'].add(nephew)

#------------------------------------------------------------------------------#

def calculate_the_paradox():
    value=0
    for node in NODES.values():
        # fathers
        if len(node['list_of_fathers'])==0:
            node['paradox_fathers'] = None
        elif len(node['list_of_sons'])==0:
            node['paradox_fathers'] = True
        elif ((len(node['list_of_brothers'])+1)/len(node['list_of_fathers'])) \
            > len(node['list_of_sons']):
            node['paradox_fathers'] = True
        else:
            node['paradox_fathers'] = False
        PARADOX_FATHERS_COUNTING[node['paradox_fathers']]+=1
        # sons
        if len(node['list_of_sons'])==0:
            node['paradox_sons'] = None
        elif len(node['list_of_grandsons'])==0:
            node['paradox_sons'] = False
        elif (len(node['list_of_grandsons'])/len(node['list_of_sons'])) \
            > len(node['list_of_sons']):
            node['paradox_sons'] = True
        else:
            node['paradox_sons'] = False
        PARADOX_SONS_COUNTING[node['paradox_sons']]+=1
        # brothers
        if len(node['list_of_brothers'])==0:
            node['paradox_brothers'] = None
        elif len(node['list_of_nephews'])==0:
            node['paradox_brothers'] = False
        elif len(node['list_of_sons'])==0:
            node['paradox_brothers'] = True
        elif (len(node['list_of_nephews'])/len(node['list_of_brothers'])) \
            > len(node['list_of_sons']):
            node['paradox_brothers'] = True
        else:
            node['paradox_brothers'] = False
        PARADOX_BROTHERS_COUNTING[node['paradox_brothers']]+=1

#------------------------------------------------------------------------------#

def paradox_over_time():
    global TOTAL_VALID_SONS,TOTAL_VALID_BROTHERS,TOTAL_VALID_FATHERS
    for node in NODES.values():
        if node['year'] not in PARADOX_VALUE_OVER_YEARS_SONS.keys():
            PARADOX_VALUE_OVER_YEARS_SONS[node['year']] = {True:0, False:0, None:0}
            PARADOX_VALUE_OVER_YEARS_FATHERS[node['year']] = {True:0, False:0, None:0}
            PARADOX_VALUE_OVER_YEARS_BROTHERS[node['year']] = {True:0, False:0, None:0}
        PARADOX_VALUE_OVER_YEARS_SONS[node['year']][node['paradox_sons']]+=1
        PARADOX_VALUE_OVER_YEARS_FATHERS[node['year']][node['paradox_fathers']]+=1
        PARADOX_VALUE_OVER_YEARS_BROTHERS[node['year']][node['paradox_brothers']]+=1

#------------------------------------------------------------------------------#

def print_to_file_paradox_over_years(filename):
    file_path_fathers = './results_'+filename+'/fathers_'+filename+'.csv'
    file_path_brothers = './results_'+filename+'/brothers_'+filename+'.csv'
    file_path_sons = './results_'+filename+'/sons_'+filename+'.csv'
    with open (file_path_fathers, 'w') as fathers_output:
        fathers_output.write('year;absolute none;absolute false;absolute true;'
            'percentual none;percentual false;percentual true;total;total valid\n')
        for year, paradox_value in PARADOX_VALUE_OVER_YEARS_FATHERS.items():
            total_per_year = paradox_value[None]+paradox_value[False]+\
                paradox_value[True]
            fathers_output.write('{};{};{};{};{:.4f};{:.4f};{:.4f};{};{}\n'.format(
                year,paradox_value[None],paradox_value[False],
                paradox_value[True],paradox_value[None]/total_per_year,
                paradox_value[False]/total_per_year,
                paradox_value[True]/total_per_year,total_per_year,
                paradox_value[False]+paradox_value[True]).replace('.',','))
    with open (file_path_brothers, 'w') as brothers_output:
        brothers_output.write('year;absolute none;absolute false;absolute true;'
            'percentual none;percentual false;percentual true;total;total valid\n')
        for year, paradox_value in PARADOX_VALUE_OVER_YEARS_BROTHERS.items():
            total_per_year = paradox_value[None]+paradox_value[False]+\
                paradox_value[True]
            brothers_output.write('{};{};{};{};{:.4f};{:.4f};{:.4f};{};{}\n'.format(year,
                paradox_value[None],paradox_value[False],paradox_value[True],
                paradox_value[None]/total_per_year,
                paradox_value[False]/total_per_year,
                paradox_value[True]/total_per_year,total_per_year,
                paradox_value[False]+paradox_value[True]).replace('.',','))
    with open (file_path_sons, 'w') as sons_output:
        sons_output.write('year;absolute none;absolute false;absolute true;'
            'percentual none;percentual false;percentual true;total;total valid\n')
        for year, paradox_value in PARADOX_VALUE_OVER_YEARS_SONS.items():
            total_per_year = paradox_value[None]+paradox_value[False]+\
                paradox_value[True]
            sons_output.write('{};{};{};{};{:.4f};{:.4f};{:.4f};{};{}\n'.format(year,
                paradox_value[None],paradox_value[False],paradox_value[True],
                paradox_value[None]/total_per_year,
                paradox_value[False]/total_per_year,
                paradox_value[True]/total_per_year, total_per_year,
                paradox_value[False]+paradox_value[True]).replace('.',','))


#------------------------------------------------------------------------------#

def terminal_output():
    print('TOTAL = {}\n'.format(NUMBER_OF_NODES))
    print('SONS\nNone;False;True\n{};{};{}\n{:.4f};{:.4f};{:.4f}\n'.format(
        PARADOX_SONS_COUNTING[None],PARADOX_SONS_COUNTING[False],
        PARADOX_SONS_COUNTING[True],
        PARADOX_SONS_COUNTING[None]/NUMBER_OF_NODES,
        PARADOX_SONS_COUNTING[False]/NUMBER_OF_NODES,
        PARADOX_SONS_COUNTING[True]/NUMBER_OF_NODES).replace('.',','))
    print('FATHERS\nNone;False;True\n{};{};{}\n{:.4f};{:.4f};{:.4f}\n'.format(
        PARADOX_FATHERS_COUNTING[None],PARADOX_FATHERS_COUNTING[False],
        PARADOX_FATHERS_COUNTING[True],
        PARADOX_FATHERS_COUNTING[None]/NUMBER_OF_NODES,
        PARADOX_FATHERS_COUNTING[False]/NUMBER_OF_NODES,
        PARADOX_FATHERS_COUNTING[True]/NUMBER_OF_NODES).replace('.',','))
    print('BROTHERS\nNone;False;True\n{};{};{}\n{:.4f};{:.4f};{:.4f}\n'.format(
        PARADOX_BROTHERS_COUNTING[None],PARADOX_BROTHERS_COUNTING[False],
        PARADOX_BROTHERS_COUNTING[True],
        PARADOX_BROTHERS_COUNTING[None]/NUMBER_OF_NODES,
        PARADOX_BROTHERS_COUNTING[False]/NUMBER_OF_NODES,
        PARADOX_BROTHERS_COUNTING[True]/NUMBER_OF_NODES).replace('.',','))

#------------------------------------------------------------------------------#

def main():
    parser = argparse.ArgumentParser(
        description = ("This program processes the data filtered by "
        "'"'filter-graph-file.py'"'. The objective is to generate csv files"
        "with information about genealogy graphs, in particular, about the "
        "friendship paradox.")
    )
    parser.add_argument(
        "directory", action = "store",
        help = "absolute file path of the directory where the csv files "
            "generated from '"'filter-graph-file.py'"' are stored."
    )

    args = parser.parse_args()
    filename = manage_args(args)
    fill_the_dictionaries(filename)
    fill_the_lists()
    calculate_the_paradox()
    #paradox_over_time()
    #print_to_file_paradox_over_years(filename)
    terminal_output()
    lev = {'f':0,'s':0,'b':0,'fs':0,'sb':0,'bf':0,'fsb':0}

    for node in NODES.values():
        f,s,b=node['paradox_fathers'],node['paradox_sons'],node['paradox_brothers']
        if f and not s and not b:
            lev['f']+=1
        if s and not b and not f:
            lev['s']+=1
        if b and not f and not s:
            lev['b']+=1
        if f and s and not b:
            lev['fs']+=1
        if s and b and not f:
            lev['sb']+=1
        if b and f and not s:
            lev['bf']+=1
        if b and s and b:
            lev['fsb']+=1
    print('fathers: {}\nsons: {}\nbrothers: {}\nfathers and sons: {}\n'
        'sons and brothers: {}\nbrothers and fathers: {}\n'
        'fathers and sons and brothers {}\neveryone: {}'.format(lev['f'],
        lev['s'],lev['b'],lev['fs'],lev['sb'],lev['bf'],lev['fsb'],
        lev['f']+lev['s']+lev['b']+lev['fs']+lev['sb']+lev['bf']+lev['fsb']))


#------------------------------------------------------------------------------#

if __name__ == '__main__':
    try:
        main()
    except:
        print("whoops!")
        raise
    print("Done! =)")
