from MoraJai import MoraJai
from queue import Queue
import copy
import networkx as nx
from matplotlib import colormaps
import matplotlib.pyplot as plt
def solveMoraJai(Box: MoraJai) -> MoraJai:
    if Box.isSolved(): return Box
    q: Queue[MoraJai] = Queue()
    q.put(Box)
    visited = set()
    visited.add(Box)
    while not q.empty():
        curr = q.get()
        for r in range(3):
            for c in range(3):
                tmp = copy.deepcopy(curr)
                tmp.pressTile(r, c)
                if tmp.isSolved():
                    return tmp
                if tmp not in visited:
                    visited.add(tmp)
                    q.put(tmp)
    return Box

def solveMoraJaiPath(Box: MoraJai) -> list:
    if Box.isSolved(): return [Box]
    q = Queue()
    q.put([Box])
    visited = set()
    visited.add(Box)
    
    while not q.empty():
        currList = q.get()
        curr: MoraJai = currList[-1]
        for r in range(3):
            for c in range(3):
                tmp = copy.deepcopy(curr)
                tmp.pressTile(r, c)
                if tmp.isSolved():
                    currList.append(tmp)
                    return currList
                if tmp not in visited:
                    visited.add(tmp)
                    tmpList = copy.deepcopy(currList)
                    tmpList.append(tmp)
                    q.put(tmpList)
    return Box

def getMoraJaiAdjDict(Box: MoraJai) -> tuple:
    if Box.isSolved(): return ({Box: []}, [])
    q = Queue()
    q.put([Box])

    visited = set()
    visited.add(Box)
    
    adj = {Box: []}
    sol = []
    while not q.empty():
        currList = q.get()
        if len(sol) != 0 and len(currList) > len(sol[0]):
            continue
        curr: MoraJai = currList[-1]
        for r in range(3):
            for c in range(3):
                tmp = copy.deepcopy(curr)
                tmp.pressTile(r, c)
                tmpList = copy.deepcopy(currList)
                tmpList.append(tmp)
                adj[curr].append(tmp)
                if tmp.isSolved():
                    if len(sol) == 0:
                        sol = [tmpList]
                    elif len(sol[0]) >= len(tmpList):
                        sol.append(tmpList)
                if tmp not in visited:
                    visited.add(tmp)
                    adj[tmp] = []
                    q.put(tmpList)
    return (adj, sol)

def buildColorMap(adj, sol):
    q = Queue()
    tmp = Queue()
    visited = set()
    for boxes in sol:
        for box in boxes:
            if box not in visited:
                q.put(box)
                visited.add(box)

    color_val = 100
    color_delta = 100 // len(sol[0])
    cmp = {}

    while not q.empty():
        box = q.get()
        cmp[box] = color_val
        for ngbr in adj[box]:
            if ngbr not in visited:
                tmp.put(ngbr)
                visited.add(ngbr)
        if q.empty():
            q = tmp
            tmp = Queue()
            color_val -= color_delta

    return cmp



adj, sol = getMoraJaiAdjDict(MoraJai())
cmp = buildColorMap(adj, sol)
cmap = []

G = nx.DiGraph(adj)

for box in G:
    cmap.append(cmp[box])

lay = nx.forceatlas2_layout(G)
nx.draw(G, pos=lay, with_labels=True, font_size=6, font_weight='bold', alpha=0.3, arrows=True, cmap=colormaps["plasma"], node_color=cmap)
plt.show()

printMoraJaiPath(solveMoraJaiPath(MoraJai()))

# Sanctum
result = len(solveMoraJaiPath(MoraJai([[3,2,3],[2,2,2],[3,5,3]],[2,2,2,2])))
print("got:{} expect:{}".format(result, 13))
result = len(solveMoraJaiPath(MoraJai([[1,3,1],[9,8,9],[7,3,2]],[8,8,8,8]))) 
print("got:{} expect:{}".format(result, 20))
result = len(solveMoraJaiPath(MoraJai([[2,5,1],[5,3,5],[1,5,2]],[5,5,5,5])))
print("got:{} expect:{}".format(result, 13))
result = len(solveMoraJaiPath(MoraJai([[5,6,5],[3,8,2],[6,6,6]],[6,6,6,6])))
print("got:{} expect:{}".format(result, 22))
result = len(solveMoraJaiPath(MoraJai([[9,2,9],[9,9,9],[6,3,6]],[9,9,9,9])))
print("got:{} expect:{}".format(result, 17))
t = (solveMoraJaiPath(MoraJai([[5,5,5],[7,4,7],[1,1,1]],[7,7,7,7])))
printMoraJaiPath(t)
result = len(t)
print("got:{} expect:{}".format(result, 9))
result = len(solveMoraJaiPath(MoraJai([[4,4,1],[1,1,1],[9,9,9]],[4,4,4,4])))
print("got:{} expect:{}".format(result, 14))
result = len(solveMoraJaiPath(MoraJai([[3,1,3],[1,9,9],[1,2,6]],[3,3,3,3])))
print("got:{} expect:{}".format(result, 23))