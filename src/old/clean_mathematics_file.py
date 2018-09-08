import sys
import os
import shlex
import copy
import csv

NODES = {}
EDGES = {}
NODES_MODEL = {'id':0, 'name':'', 'year':0}
EDGES_MODEL = {'source':0, 'target':0}
ID_KEY, NAME_KEY, YEAR_KEY, SOURCE_KEY, TARGET_KEY = 0,1,7,0,1

#------------------------------------------------------------------------------#

def get_gdf_line_sizes(graph_file):
    nodes = 0
    edges = 0
    with open (graph_file+'.gdf', 'r') as nodes_input:
        for line in nodes_input:
            if 'nodedef' in line:
                nodes = len(line.split(','))
                #print('node line is:\n\t{}'.format(line))
            elif 'edgedef' in line:
                edges = len(line.split(','))
                #print('edge line is:\n\t{}'.format(line))
    nodes_input.close()
    print ('nodes: {}\nedges: {}'.format(nodes,edges))
    return nodes, edges

#------------------------------------------------------------------------------#

def get_fields (graph_file):
    nodes_line_size, edges_line_size = get_gdf_line_sizes(graph_file)
    if not os.path.isdir('./results_'+graph_file):
        os.mkdir('./results_'+graph_file)
    #original file splitted
    nodes_aux = open('./results_'+graph_file+'/aux_nodes_'+graph_file+'.csv','w')
    edges_aux = open('./results_'+graph_file+'/aux_edges_'+graph_file+'.csv','w')
    #output files, will be analyzed with generate-paradox-values.py
    nodes_output = open('./results_'+graph_file+'/nodes_'+graph_file+'.csv','w')
    edges_output = open('./results_'+graph_file+'/edges_'+graph_file+'.csv','w')
    #csv reader, reads the original file splitted
    nodes_csv_input = csv.DictReader(open('./results_'+graph_file+'/aux_nodes_'+graph_file+'.csv'))
    edges_csv_input = csv.DictReader(open('./results_'+graph_file+'/aux_edges_'+graph_file+'.csv'))

    nodes_dictionary = {}
    edges_dictionary = {}
    artifficial_key = 0

    with open (graph_file+'.gdf', 'r') as graph_input:
            for line in graph_input:
                line = line.replace('\'','"')
                line = line.replace(' VARCHAR','')
                line = line.replace(' DOUBLE','')
                line = line.replace('nodedef> ','')
                line = line.replace('edgedef> ','')
                if line.count(',')+1 >= nodes_line_size:
                    nodes_aux.write(line)
                elif line.count(',')+1 == edges_line_size:
                    edges_aux.write(line)
                else:
                    print(line.count(','))
                    print(line)

    for line in nodes_csv_input:
        nodes_dictionary[line['name']]=line

    for line in edges_csv_input:
        edges_dictionary[artifficial_key]=line
        artifficial_key+=1

    nodes_output.write('id,name,year\n')
    for node in nodes_dictionary.values():
        nodes_output.write('{},{},{}\n'.format(
            node['name'],node['nome'],node['ano']))
    '''
    for index in range(0,len(nodes_dictionary.keys())):
        nodes_aux.write('{},{},{}\n'.format(
        nodes_dictionary[index]['name'],nodes_dictionary[index]['nome'],
        nodes_dictionary[index]['ano']))
        '''

    edges_output.write('source,target\n')
    for edge in edges_dictionary.values():
        if edge['node1'] in nodes_dictionary.keys() and edge['node2'] in nodes_dictionary.keys():
            edges_output.write('{},{}\n'.format(
            edge['node1'], edge['node2']))
        elif edge['node1'] not in nodes_dictionary.keys():
            print('node1')
        elif edge['node2'] not in nodes_dictionary.keys():
            print('node2')

    '''
    for index in range(0,len(edges_dictionary.keys())):
        edges_aux.write('{},{}\n'.format(
            edges_dicionary[index]['node1'], edges_dicionary[index]['node2']))
    '''
#------------------------------------------------------------------------------#

filename = "math_16_06_17"
print("tik")
get_fields(filename)
print("tok")
