import json
import logging

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def gridMap(data):
  e1,e2 = (data["entryPoint"]["first"], data["entryPoint"]['second'])
  t1,t2 = (data["targetPoint"]["first"], data["targetPoint"]["second"])
  x,y = abs(t1-e1)+1,abs(t2-e2)+1
  grid = [[0]*x for _ in range(y)]
  depth = data["gridDepth"]
  key = data["gridKey"]
  hstep = data["horizontalStepper"]
  vstep = data["verticalStepper"]
  # Calculate Risk Level of each grid
  # with Y coord 0
  for i in range(x):
    grid[0][i] = (i*hstep+depth)%key
  # with X coord 0
  for j in range(y):
    grid[j][0] = (j*vstep+depth)%key
  for j in range(1,y):
    for i in range(1,x):
      grid[j][i] = (grid[j-1][i]*grid[j][i-1]+depth)%key
  grid[y-1][x-1] = 0
  # calculate the actual risk
  risk_dict = {0:"L", 1:"M", 2:"S"}
  for i in range(y):
    for j in range(x):
      grid[i][j] = risk_dict[grid[i][j]%3]
  print(grid)
  return grid

# Basically a dijkstra shortest path
def shortpath(grid):
  cost_dict = {"L":3, "M":2, "S":1}
  m,n = len(grid), len(grid[0])
  min_cost = [[float('inf')]*n for _ in range(m)]
  min_cost[0][0] = 0
  current = [(0,0)]
  visited = set()
  while current:
#    if (m-1,n-1) in visited:
#      break
    p1,p2 = current.pop()
    for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
      newi,newj = p1+i,p2+j
      if 0<=newi<m and 0<=newj<n and (newi,newj) not in visited:
        min_cost[newi][newj] = min(min_cost[newi][newj], min_cost[p1][p2]+cost_dict[grid[newi][newj]])
        current.append((newi,newj))
    visited.add((p1,p2))
  return min_cost[m-1][n-1]


@app.route('/stock-hunter', methods=['POST'])
def evaluateStockHunter():
  sol = []
  data_full = request.get_json()
  logging.info("data sent for evaluation {}".format(data_full))
  for data in data_full:
    grid = gridMap(data)
    min_cost = shortpath(grid)
    sol.append({"gridMap":grid,"minimumCost":min_cost})
  logging.info("My result :{}".format(sol))
  return json.dumps(sol)

#if __name__ == "__main__":
#  main()
