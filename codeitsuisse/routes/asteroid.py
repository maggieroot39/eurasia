import json
import datetime
from collections import defaultdict
from itertools import groupby
import logging

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def mancher(s, top=1):
    s = "#" + '#'.join([e for e in s]) + "#"
    record = [1 for e in range(len(s))]
    l, r, c = -1, -1, -1

    for i in range(len(s)):
        if i >= r:
            l, r, c = i, i, i
            while  r + 1 < len(s) and l - 1 > -1  and s[r + 1] ==  s[l - 1]:
                l -=1
                r +=1
            record[i] = r - c

        if i < r:
            if r - i > record[2*c-i]:
                record[i] = record[2*c-i]
            else:
                l = 2*i - r
                c = i
                while  r + 1 < len(s) and l - 1 > -1  and s[r + 1] ==  s[l - 1]:
                    l -=1
                    r +=1
                record[i] = r - c

    top_ids = [i for i, j in enumerate(record) if j == sorted(record)[-1]]
    result = []
    if top == 1:
        idx_list = top_ids
    elif top == 2:
        second_top_ids = [i for i, j in enumerate(record) if j == sorted(record)[-1-len(top_ids)]]
        idx_list = second_top_ids
    elif top == 3:
        second_top_ids = [i for i, j in enumerate(record) if j == sorted(record)[-1-len(top_ids)]]
        third_top_ids = [i for i, j in enumerate(record) if j == sorted(record)[-1-len(top_ids)-len(second_top_ids)]]
        idx_list = third_top_ids
    for idx in idx_list:
        r =  s[idx - record[idx]: idx + record[idx] + 1].replace('#', '')
        out = int((idx+1)/2-1), len(r), r
        result.append(out)

    return result


def multiplier(num):
    if num <= 6:
        return 1*num
    elif 7 <= num < 10:
        return 1.5*num
    elif num >= 10:
        return 2*num


def main(test_case):
    statistics = [[k,len(list(v))] for k,v in groupby(test_case)]

    abbv_string = [item[0] for item in statistics]
    abbv_count = [item[1] for item in statistics]
    longest_list = mancher(abbv_string, top=1)

    pos_best, score_best = 0, 0
    for longest in longest_list:
        char_idx, char_len, char = longest
        if not abbv_count[char_idx] % 2 == 1:
            continue
        pos = sum(abbv_count[:char_idx]) + int(abbv_count[char_idx]/2)
        score = multiplier(abbv_count[char_idx])
        for i in range(int((char_len-1)/2)):
            count = i+1
            score += multiplier( abbv_count[char_idx-count]+abbv_count[char_idx+count] )
        if score > score_best:
            pos_best, score_best = pos, score

    try:
        second_longest_list = mancher(abbv_string, top=2)
        for longest in second_longest_list:
            char_idx, char_len, char = longest
            if not abbv_count[char_idx] % 2 == 1:
                continue
            pos = sum(abbv_count[:char_idx]) + int(abbv_count[char_idx]/2)
            score = multiplier(abbv_count[char_idx])
            for i in range(int((char_len-1)/2)):
                count = i+1
                score += multiplier( abbv_count[char_idx-count]+abbv_count[char_idx+count] )
            if score > score_best:
                pos_best, score_best = pos, score
    except:
        pass

    try:
        third_longest_list = mancher(abbv_string, top=3)
        for longest in third_longest_list:
            char_idx, char_len, char = longest
            if not abbv_count[char_idx] % 2 == 1:
                continue
            pos = sum(abbv_count[:char_idx]) + int(abbv_count[char_idx]/2)
            score = multiplier(abbv_count[char_idx])
            for i in range(int((char_len-1)/2)):
                count = i+1
                score += multiplier( abbv_count[char_idx-count]+abbv_count[char_idx+count] )
            if score > score_best:
                pos_best, score_best = pos, score
    except:
        pass

    return pos_best, score_best




@app.route('/asteroid', methods=['POST'])
def evaluateAsteroid():
  sol = []
  data = request.get_json()
  logging.info("data sent for evaluation {}".format(data))
  for test_case in data['test_cases']:
    pos, score = main(test_case)
    sol.append({"input":test_case,"score":score,"origin":pos})
  logging.info("My result :{}".format(sol))
  return json.dumps(sol)
