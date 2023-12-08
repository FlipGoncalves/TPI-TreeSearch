# Student: Filipe Gonçalves, 98083

# Discussion of the work with students:
# Pedro Lopes, 97827
# João Borges, 98155
# Gonçalo Machado, 98359
# Vicente Costa, 98515

from tree_search import *
from cidades import *

class MyNode(SearchNode):
    def __init__(self,state,parent,arg3=None,arg4=None,arg5=None):
        super().__init__(state,parent)
        self.depth = arg3
        self.cost = arg4
        self.heuristic = arg5
        self.eval = arg4 + arg5
        self.children = []

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth'): 
        self.solution_tree = None
        self.problem = problem
        root = MyNode(problem.initial, None, 0, 0, self.problem.domain.heuristic(problem.initial, self.problem.goal))
        self.all_nodes = [root]
        self.open_nodes = [0]
        self.strategy = strategy
        self.solution = None
        self.non_terminals = 0
        self.used_shortcuts = []
        self.path = None

    def astar_add_to_open(self,lnewnodes):
        #IMPLEMENT HERE
        self.open_nodes.extend(lnewnodes)
        self.open_nodes = sorted(self.open_nodes, key=lambda x: self.all_nodes[x].heuristic + self.all_nodes[x].cost)

    def propagate_eval_upwards(self,node):
        #IMPLEMENT HERE
        minimo = 10000
        for child in node.children:
            if self.all_nodes[child].eval < minimo:
                minimo = self.all_nodes[child].eval
        if minimo != 10000:
            node.eval = minimo
        if node.parent != None:
            self.propagate_eval_upwards(self.all_nodes[node.parent])

    def search2(self, atmostonce=False):
        #IMPLEMENT HERE
        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                self.path = self.get_path(self.solution)
                return self.path
            lnewnodes = []
            self.non_terminals += 1
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    dis = self.problem.domain.heuristic(newstate, self.problem.goal)
                    cost = self.problem.domain.cost(node.state, a)
                    newnode = MyNode(newstate, nodeID, node.depth + 1, node.cost + cost, dis)
                    nodes = [nd.state for nd in self.all_nodes]
                    if atmostonce and any([newstate in nodes]):
                        if newnode.cost >= self.all_nodes[nodes.index(newstate)].cost:
                            continue
                        self.all_nodes[nodes.index(newstate)] = newnode
                    else:
                        self.all_nodes.append(newnode)
                        lnewnodes.append(len(self.all_nodes)-1)
                    node.children.append(len(self.all_nodes)-1)
                    
            self.propagate_eval_upwards(node)
            self.add_to_open(lnewnodes)
        return None

    def repeated_random_depth(self,numattempts=3):
        #IMPLEMENT HERE
        maximo = 100000
        temp = self.solution_tree
        search_tm = []
        for index in range(0, numattempts):
            self.solution_tree = MyTree(self.problem, self.strategy)
            self.solution_tree.curr_pseudo_rand_number = index
            search = self.solution_tree.search2()
            if self.solution_tree.solution.cost < maximo:
                maximo = self.solution_tree.solution.cost
                temp = self.solution_tree
                search_tm = search
        self.solution_tree = temp
        return search_tm


    def make_shortcuts(self):
        #IMPLEMENT HERE
        middle = -1
        lista = []
        for index in range(len(self.path)):
            if middle == -1 or index == middle:
                middle = -1
                for action in self.problem.domain.actions(self.path[index]):
                    if action[1] in self.path:
                        index_1 = self.path.index(action[1])
                        if index > middle and index_1 > index + 1:
                            middle = index_1
                            self.used_shortcuts.append(action)
        shortcut = False
        for state in self.path:
            for st in self.used_shortcuts:
                if state == st[0]:
                    shortcut = True
                    lista.append(state)
                    break
                if state == st[1]:
                    shortcut = False
            if shortcut == False:
                lista.append(state)
        return lista


class MyCities(Cidades):

    def maximum_tree_size(self,depth):   # assuming there is no loop prevention  
        #IMPLEMENT HERE
        dic = {}
        for (e1,e2,d) in self.connections:
            if e1 not in dic.keys():
                dic[e1] = [e2]
            else:
                dic[e1].append(e2)
            if e2 not in dic.keys():
                dic[e2] = [e1]
            else:
                dic[e2].append(e1)
        avg = sum(len(x) for x in dic.values())/len(dic.keys())
        return round(sum(avg**dep for dep in range(0, depth+1)))