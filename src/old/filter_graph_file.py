import os
import sys
import copy
import argparse

#------------------------------------------------------------------------------#

NODES = {}
EDGES = {}
NODES_MODEL = {'id':0, 'name':'', 'year':0, 'area':''}
EDGES_MODEL = {'source':0, 'target':0, 'finished_in':0}
ID_KEY, NAME_KEY, AREA_KEY, SOURCE_KEY, TARGET_KEY, YEAR_KEY = 0,0,0,0,0,0

#------------------------------------------------------------------------------#

def  manage_args_and_get_filename(args):
    global ID_KEY,NAME_KEY,AREA_KEY,SOURCE_KEY,TARGET_KEY,YEAR_KEY

    if not os.path.isfile(args.file):
        print("Sorry! The file {} does not exists. Try again!".format(
            args.file))
        sys.exit()

    extension = args.file.rsplit('.',1)[1]
    if not extension == args.format:
        print("Sorry! The indicated file format ({}) does not correspond to "
            "the extension of the file ({}).".format(args.format,extension)
        )
        sys.exit()
    if not extension=='gdf':
        print('nope.')
        sys.exit()

    ID_KEY = args.id
    NAME_KEY = args.name
    AREA_KEY = args.area
    SOURCE_KEY = args.source
    TARGET_KEY = args.target
    YEAR_KEY = args.year

    filename_split = args.file.rsplit('/',1)

    return (filename_split[len(filename_split)-1]).rsplit('.',1)[0]

#------------------------------------------------------------------------------#

def get_gdf_line_sizes(graph_file):

    with open (graph_file, 'r') as input:
        for line in input:
            if 'nodedef>' in line:
                #parsed_line = line.split(',')
                #nodes = len(parsed_line)
                nodes = len(line.split(','))
                '''
                print("vertices:\n")
                for i in parsed_line:
                    print(i)
                '''
            elif 'edgedef>' in line:
                #parsed_line = line.split(',')
                #edges = len(parsed_line)
                edges = len(line.split(','))
                '''
                print("arestas:\n")
                for i in parsed_line:
                    print(i)
                '''
                break
        return nodes, edges

#------------------------------------------------------------------------------#

def create_structures_from_gdf(file_path):
    global ID_KEY, NAME_KEY, AREA_KEY, SOURCE_KEY, TARGET_KEY, YEAR_KEY
    edges_dict = {}
    nodes_dict = {}
    nodes_line_size, edges_line_size = get__gdf_line_sizes(file_path)
    artifficial_key=0

    with open (file_path, 'r') as graph_file:
        for line in graph_file:
            parsed_line = line.split(',')
            if len(parsed_line) == nodes_line_size and 'nodedef>' not in line:
                nodes_dict = copy.deepcopy(NODES_MODEL)
                nodes_dict['id'] = int( parsed_line[ID_KEY])
                nodes_dict['name'] = parsed_line[NAME_KEY]
                nodes_dict['area'] = parsed_line[AREA_KEY]
                NODES[nodes_dict['id']] = nodes_dict
            elif len(parsed_line) == edges_line_size and 'edgedef>' not in line:
                edges_dict = copy.deepcopy(EDGES_MODEL)
                edges_dict['source'] = int(parsed_line[SOURCE_KEY])
                edges_dict['target'] = int(parsed_line[TARGET_KEY])
                edges_dict['finished_in'] = int(parsed_line[YEAR_KEY])
                NODES[edges_dict['target']]['year'] = edges_dict['finished_in']
                EDGES[artifficial_key] = edges_dict
                artifficial_key+=1

#------------------------------------------------------------------------------#

def print_to_file(filename):
    if not os.path.isdir('./results_'+filename):
        os.mkdir('./results_'+filename)
    file_path_nodes = './results_'+filename+'/nodes_'+filename+'.csv'
    file_path_edges = './results_'+filename+'/edges_'+filename+'.csv'
    set_of_nodes_that_are_in_the_graph=set([])
    with open (file_path_nodes, 'w') as nodes_output:
        nodes_output.write('id,name,area,year\n')
        for node in NODES.values():
            set_of_nodes_that_are_in_the_graph.add(node['id'])
            nodes_output.write('{},{},{},{}\n'.format(
                node['id'],node['name'],
                node['area'],node['year']))
    with open (file_path_edges, 'w') as edges_output:
        edges_output.write('source,target,year\n')
        for edge in EDGES.values():
            if edge['source'] in set_of_nodes_that_are_in_the_graph and \
                edge['target'] in set_of_nodes_that_are_in_the_graph:
                edges_output.write('{},{},{}\n'.format(
                    edge['source'], edge['target'],edge['finished_in']))


#------------------------------------------------------------------------------#

def main():
    parser = argparse.ArgumentParser(
        description = ("This program processes graph files in the formats  "
        ".gdf and .graphml and generates csv files with info about the "
        )
    )
    parser.add_argument(
        "format", action = "store",
        help = "format of the graph file."
    )
    parser.add_argument(
        "file", action = "store",
        help = "absolute file path of the graph file with the extension indicated with '"'--format'"' flag."
    )
    parser.add_argument(
        "-id", action = "store", dest="id", default=0, type=int,
        help = "position of the '"'id'"' key in the gdf file."
    )
    parser.add_argument(
        "-name", action = "store", dest="name", default=1, type=int,
        help = "position of the '"'name'"' key in the gdf file."
    )
    parser.add_argument(
        "-area", action = "store", dest="area", default=3, type=int,
        help = "position of the '"'area'"' key in the gdf file."
    )
    parser.add_argument(
        "-source", action = "store", dest="source", default=0, type=int,
        help = "position of the '"'source'"' key in the gdf file."
    )
    parser.add_argument(
        "-target", action = "store", dest="target", default=0, type=int,
        help = "position of the '"'target'"' key in the gdf file."
    )
    parser.add_argument(
        "-year", action = "store", dest="year", default=0, type=int,
        help = "position of the '"'year'"' key in the gdf file."
    )

    args = parser.parse_args()
    filename = manage_args_and_get_filename(args)
    create_structures_from_gdf(filename+'.'+args.format)
    print_to_file(filename)
    print("Done! =)")

#------------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        main()
    except:
        raise
