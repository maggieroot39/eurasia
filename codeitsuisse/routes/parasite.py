import json
import os
import heapq
#import logging

from flask import request, jsonify

from codeitsuisse import app

#logger = logging.getLogger(__name__)

def find_healthy(grid,m,n):
  healthy = set()
  for i in range(m):
    for j in range(n):
      if grid[i][j] == 3:
        para = (i,j)
      elif grid[i][j] == 1:
        healthy.add((i,j))
  return para, tuple(healthy)

def parasite_A(grid, interest, para, healthy,m,n):
  t_time = -1
  to_visit = set(healthy)
  cur = [[0,para[0],para[1]]]
  visited = set()
  dist = [[float('inf')]*n for _ in range(m)]
  dist[para[0]][para[1]] = 0

  moves = [(0,1), (0,-1), (-1,0), (1,0)]
  # Use Dijkstra to find all-map shortest distance from para
  while cur:
    d, x, y = heapq.heappop(cur)
    if (x, y) in visited:
      continue
    for i,j in moves:
      newx,newy = x+i, y+j
      if (0<=newx<m) and (0<=newy<n) and (grid[newx][newy]==1) and ((newx,newy) not in visited) and (dist[newx][newy]>d+1):
        dist[newx][newy] = d+1
        heapq.heappush(cur, [d+1, newx, newy])
        to_visit.discard((newx,newy))
        t_time = max(t_time,d+1)
    visited.add((x,y))

  if to_visit:
    t_time = -1
  individual = dict()
  for s in interest:
    s1, s2 = [int(x) for x in s.split(",")]
    if (dist[s1][s2] == float('inf')) or (grid[s1][s2] != 1):
      individual[s] = -1
    else:
      individual[s] = dist[s1][s2]
  return individual, t_time

# Basically the same code, but with different edge weight
def parasite_B(grid, para, healthy,m,n):
  t_time = -1
  to_visit = set(healthy)
  cur = [[0,para[0],para[1]]]
  visited = set()
  dist = [[float('inf')]*n for _ in range(m)]
  dist[para[0]][para[1]] = 0

  moves = [(0,1), (0,-1), (-1,0), (1,0), (1,1), (-1,1), (1,-1), (-1,-1)]
  # Use Dijkstra to find all-map shortest distance from para
  while cur:
    d, x, y = heapq.heappop(cur)
    if (x, y) in visited:
      continue
    for i,j in moves:
      newx,newy = x+i, y+j
      if (0<=newx<m) and (0<=newy<n) and (grid[newx][newy]==1) and ((newx,newy) not in visited) and (dist[newx][newy]>d+1):
        dist[newx][newy] = d+1
        heapq.heappush(cur, [d+1, newx, newy])
        to_visit.discard((newx,newy))
        t_time = max(t_time,d+1)
    visited.add((x,y))

  if to_visit:
    t_time = -1
  return t_time


def parasite_X(grid, para, healthy,m,n):
  energy = 0
  to_visit = set(healthy)
  cur = [[0,para[0],para[1]]]
  visited = set()
  dist = [[float('inf')]*n for _ in range(m)]
  dist[para[0]][para[1]] = 0

  moves = [(0,1), (0,-1), (-1,0), (1,0)]
  # Use Dijkstra to find all-map shortest distance from para
  while to_visit:
    d, x, y = heapq.heappop(cur)
    if (x, y) in visited:
      continue
    for i,j in moves:
      newx,newy = x+i, y+j
      if (0<=newx<m) and (0<=newy<n) and ((newx,newy) not in visited) and (dist[newx][newy]>d):
        dist[newx][newy] = min(dist[newx][newy],abs(grid[newx][newy]-1)+d)
        heapq.heappush(cur, [dist[newx][newy], newx, newy])
        to_visit.discard((newx,newy))
        if grid[newx][newy] == 1:
          energy = max(energy,dist[newx][newy])
    visited.add((x,y))
  return energy


@app.route('/parasite', methods=['POST'])
def evaluateParasite():
  sol = []
  data_full = request.get_json()
#  logging.info("data sent for evaluation {}".format(data_full))

  for data in data_full:
    room, grid, interest = data["room"], data["grid"], data["interestedIndividuals"]
    m,n = len(grid), len(grid[0])
    para, healthy = find_healthy(grid,m,n)
    p1, p2 = parasite_A(grid, interest, para, healthy,m,n)
    p3 = parasite_B(grid, para, healthy,m,n)
    if p2 == -1:
      p4 = parasite_X(grid, para, healthy,m,n)
    else:
      p4 = 0
    sol.append({"room":room, "p1":p1, "p2":p2, "p3":p3, "p4":p4})
#  logging.info("My result :{}".format(sol))
  return json.dumps(sol)
