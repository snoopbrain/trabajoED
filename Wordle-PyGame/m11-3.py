from collections import deque

class Node():
  def __init__(self):
    self.visited = False

def BFS(nodes, edges):
  families = 0
  maxMembers = 0

  for id, node in nodes.items():
    if node.visited == False:
      families +=1
      members = 0
      line = deque()
      line.append(id)

      while line:
        vertex = line.popleft()
        for edge in edges[vertex]:
            if nodes[edge].visited == False:
              members += 1
              nodes[edge].visited = True
              line.append(edge)
      
      if members > maxMembers:
         maxMembers = members

  print(families, maxMembers)

cases = int(input())

for i in range(cases):
  nodes = {}
  edges = {}
  
  for i in range(int(input())):
    ids = list(map(int, input().split()))
    nodes[ids[0]] = Node()
    nodes[ids[-1]] = Node()

    if ids[0] in edges:
        edges[ids[0]].append(ids[-1])
    else:
        edges[ids[0]] = [ids[-1]]
    
    if ids[-1] in edges:
        edges[ids[-1]].append(ids[0])
    else:
        edges[ids[-1]] = [ids[0]]
  BFS(nodes, edges)