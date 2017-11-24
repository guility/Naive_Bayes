from __future__ import division
from collections import defaultdict
from math import log

import random
random.seed()


dataset_files = ['weather_nom.txt', 'soybean.txt']

def checkCond(set_a, set_b):
    check = 1
    for i in range(len(a)):
        if a[i]!=b[i]: check = 0
    if check == 1: return True
    else: return False

def getCondProb(train_set, feature, feat_num, klass):
    incl = int(0)
    incl_c = int(0)
    klass_num=len(train_set[0])-1
    for i in range(len(train_set)):
        if train_set[i][feat_num].strip() == feature:
            incl = incl + 1
            if train_set[i][klass_num].strip() == klass:
                incl_c = incl_c + 1
    return abs(log(float(incl_c)/incl))
    
def classify(instance, options, train_set):
    classes = options[len(options)-1]
    class_prob = []
    res_class = None
    for klass in classes:
        feat_num = int(0)
        curr_prob = float(1)
        for feat in instance:
            curr_prob = curr_prob*getCondProb(train_set, feat, feat_num, klass)
            feat_num = feat_num + 1
        class_prob.append(curr_prob)
    curr_prob = class_prob[0]
    for prob in class_prob:
        if curr_prob > class_prob[prob]:
            curr_prob = class_prob[prob]
            res_class = classes[prob]
    
def trainModel(features, train_set):
    NF = len(features)-1
    prob_dct = {}
    for instance in train_set:
        if instance in prob_dct.keys():
            prob_dct[instance] = prob_dct[instance] + 1
        else:
            prob_dct[instance] = int(1)
    return prob_dct
        
    
def scanInfo(filepath):
    file = open(filepath)
    features = []
    feat_opt = []
    data = []
    datamet = 0
    for line in file:
        line = line.rstrip()
        line = line.lower()
        line = line.replace('\t\t',' ')
        line = line.replace('\t',' ')
        if datamet==1:
            data.append(line.split(','))
        else:
            if line.startswith('@attribute'):
                options = line[line.find('{')+1:line.find('}')]
                feat_opt.append(options.split(','))
                features.append(line[len('@attribute '):line.find('{')-1])
        if '@data' in line: datamet = 1
    if data[-3]==['%']:
        data=data[0:-3]
    return data, features, feat_opt

def genNumRand(number, ch_range):
    lst = []
    for i in range(number):
        lst.append(random.randint(0, ch_range))
    return lst

def selRand(dataset):
    train_set = []
    test_set = []
    sel_set = genNumRand(len(dataset)//10, len(dataset))
    for i in range(len(dataset)):
        if i in sel_set:
            test_set.append(dataset[i])
        else:
            train_set.append(dataset[i])
    
    return train_set, test_set

def splitData(data):
    missing_data = []
    train_set = []
    test_set = []
    for instance in data:
        if ('?' in instance) or (' ?' in instance) or ('' in instance):
            missing_data.append(instance)
        else:
            train_set.append(instance)
    train_set, test_set = selRand(train_set)
    return train_set, test_set, missing_data



def soybean(source_file):
    data, features, options = scanInfo(source_file)
    train_set, test_set = splitData(data)
    return 0


