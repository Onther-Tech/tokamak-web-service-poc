from tinydb import TinyDB, Query
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def get_network_json():

    t_db = TinyDB(config["DATABASE"]["DATABASE"])

    o_nodes = []
    r_nodes = []
    pairs = []
    nodes = []
    links = []

    #For Links
    u_nodes = []
    pairs2 = []

    #For Target
    target = {"nodes" : [], "links" : []}

    operators = t_db.search(Query().Type == "operator")
    usernodes = t_db.search(Query().Type == "usernode")

    ### Get Rootchain, Operator nodes

    for i in operators:
        o_nodes.append(i['Name'])
        pairs.append({i['Name'] : i['RootChain']['Name']})

    for i in operators:
        r_nodes.append(i['RootChain']['Name'])

    o_nodes.extend(r_nodes)
    nodes.extend(list(set(o_nodes)))

    for i in pairs:
        key = ""
        key = list(i.keys())[0]
        links.append({"source" : nodes.index(key), "target" : nodes.index(i[key])})

    #### Expand USERNODEs
    for i in usernodes:
        u_nodes.append(i["Name"])
        pairs2.append({i["Name"] : i["Operator"]["Name"]})

    for i in pairs2:
        key = ""
        key = list(i.keys())[0]

    nodes.extend(list(set(u_nodes))) # Full Node List


    # Make network relation
    for i in pairs2:
        key = ""
        key = list(i.keys())[0]
        links.append({"source" : nodes.index(key), "target" : nodes.index(i[key])})

    # print(nodes)
    # ['kevin_root1', 'kevin_op3', 'kevin_op4', 'kevin_op2', 'kevin_root2', 'kevin_op5', 'kevin_op1', 'kevin_user2', 'kevin_user1']
    # print(links)
    # [{'source': 6, 'target': 0}, {'source': 3, 'target': 0}, {'source': 1, 'target': 0}, {'source': 2, 'target': 4}, {'source': 5, 'target': 4}, {'source': 8, 'target': 6}, {'source': 7, 'target': 6}]

    for i in nodes:
        target["nodes"].append({"name" : i})

    for i in links:
        target["links"].append(i)

    # print(target)

    return target

    # with open(filename,"w+") as f:
    #     f.write(json.dumps(target, indent=4))
