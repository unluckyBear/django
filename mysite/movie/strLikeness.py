#!/bin/python
#coding:utf-8
#http://www.cnblogs.com/ymind/archive/2012/03/27/fast-memory-efficient-Levenshtein-algorithm.html
def strcmp(s, t):
    if len(s) > len(t):
        s, t = t, s
    #第一步
    n = len(s)
    m = len(t)
 
    if not m : return n
    if not n : return m
     
    #第二步
    v0 = [ i for i in range(0, m+1) ]
    v1 = [ 0 ] * (m+1) 
 
    #第三步
    cost = 0
    for i in range(1, n+1):
        v1[0] = i
        for j in range(1, m+1):
            #第四步,五步
            if s[i-1] == t[j-1]:
                cost = 0
            else:
                cost = 1
 
            #第六步
            a = v0[j] + 1
            b = v1[j-1] + 1
            c = v0[j-1] + cost
            v1[j] = min(a, b, c)
        v0 = v1[:]
    #第七步
    return v1[m]