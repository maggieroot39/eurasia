import json
import os
import heapq

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
  return grid

# Basically a dijkstra shortest path
def shortpath(grid):
  cost_dict = {"L":3, "M":2, "S":1}
  m,n = len(grid), len(grid[0])
  min_cost = [[float('inf')]*n for _ in range(m)]
  min_cost[0][0] = 0
  current = [(0,0,0)] #use heap to find current lowest distance node
  visited = set()
  while current:
    d,p1,p2 = heapq.heappop(current)
    if (p1,p2) in visited:
      continue
    for i, j in [(-1,0),(1,0),(0,-1),(0,1)]:
      newi,newj = p1+i,p2+j
      if (0<=newi<m) and (0<=newj<n) and ((newi,newj) not in visited):
        min_cost[newi][newj] = min(min_cost[newi][newj], min_cost[p1][p2]+cost_dict[grid[newi][newj]])
        heapq.heappush(current,(min_cost[newi][newj],newi,newj))
    visited.add((p1,p2))
  return min_cost[m-1][n-1]

files = [f for f in os.listdir() if f.endswith(".json")]
def main():
  
  # Process and write
  for f in files:
    sol = []
    # Read and process documents
    with open(f) as json_file:
      data_full = json.load(json_file)
      for data in data_full:
        grid = gridMap(data)
        min_cost = shortpath(grid)
        sol.append({"gridMap":grid,"minimumCost":min_cost})
    # Write this in our output text
    # g.write(""))
    print(sol)
  return 




#print(shortpath(grid))
if __name__ == "__main__":
  main()