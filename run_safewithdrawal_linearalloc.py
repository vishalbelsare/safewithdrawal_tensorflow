#!/home/ubuntu/anaconda2/bin/python

# MIT License

# Copyright (c) 2016 Druce Vertes drucev@gmail.com

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function

import argparse
import pickle
from time import strftime
import sys
import os

import numpy as np
import pandas as pd

fileprefix = "best08"
bestfile = "%s.pickle" % (fileprefix)

max_unimproved_steps = 200

gamma = 8.0

#Objective: 8315.064674

# const_spend = 2.321413
# var_spend_pcts = pd.Series([0.021015604501457775, 0.021761051829444631, 0.022312098346990435, 0.022785170076322969, 0.023285983064484993, 0.023897465220170052, 0.024584673876801872, 0.02556106756991109, 0.026657864441448173, 0.028031748201320435, 0.029551066581589736, 0.031201618742953394, 0.032978432086452118, 0.034516254916809298, 0.036027857701909138, 0.037763940480250287, 0.03992129323858909, 0.042635694985269881, 0.045638329119485004, 0.049069352739346678, 0.052383268763417638, 0.056951126091794861, 0.063470193195596478, 0.070974811737827201, 0.082180160879307573, 0.098169174319082841, 0.1205906552280696, 0.15769373320000857, 0.23376809386762137, 0.51005368542831198])
# stock_allocations = pd.Series([0.82085705309182722, 0.8208564375532369, 0.80809230790394848, 0.80474242187125467, 0.80321803760810162, 0.80214299804721623, 0.80178790048600157, 0.7839705620587375, 0.77739050153152156, 0.77699016168709201, 0.77517208520407443, 0.76706047015389667, 0.76676220145412832, 0.76576837231963391, 0.76098570290996814, 0.74113354059879621, 0.73793102049167558, 0.73650905089885166, 0.72707794679494286, 0.72393066589418387, 0.7210099158662584, 0.71370848573117784, 0.7038219623712294, 0.68848317679023907, 0.61956979054659567, 0.61331107236876559, 0.59738860596743892, 0.59391944015033249, 0.59164222259062249, 0.53441829378265526])

# startval = 100
# years_retired = 30
# const_spend_pct = .02
# const_spend = startval * const_spend_pct

# var_spend_pcts = pd.Series(np.ones(years_retired) * 0.02)
# var_spend_pcts[-1]=1.0
# stock_allocations = pd.Series(np.ones(years_retired) * 0.65)

startval = 100
years_retired = 30
# 1.5% constant spending
const_spend_pct = 0.015
const_spend = startval * const_spend_pct

# var spending a function of years left
var_spend_pcts = pd.Series([ 1.0 / (years_retired - ix) - 0.01 for ix in range(years_retired)])

#Objective: 4.390120

const_spend = 1.494627
var_spend_pcts = pd.Series([0.026510001745962072, 0.027818217278890313, 0.028605532721252741, 0.028943515850045034, 0.029650425909075188, 0.030749598116744672, 0.031600262214435557, 0.032732508555050478, 0.034385383513833988, 0.036029103781616605, 0.03767831801390633, 0.039574695022857952, 0.04181956456859641, 0.043933810727326675, 0.046368133990928623, 0.049770890997431427, 0.053761145655487272, 0.058701327619542831, 0.064816641182696089, 0.072273502883599586, 0.081202909789127517, 0.0923868781223499, 0.10647268828242094, 0.1245451336773581, 0.14860396109790044, 0.18220604185509723, 0.23242068590691847, 0.31581923728426176, 0.48186646557743196, 0.98999999999999999])

start_alloc = 0.8
end_alloc = 0.5

# save starting scenario
pickle_list = [const_spend, var_spend_pcts, start_alloc, end_alloc]
pickle.dump( pickle_list, open( bestfile, "wb" ) )


# start with a learning rate that learns quickly, gradually reduce it
# run once with 50 or 100 steps to see which learning rates are effective
# then plug in that solution and run each til no improvement for a large number of steps

for learning_rate in [
        #0.00001, # too coarse, may be NaN
        0.00003, # too coarse, may be NaN
        0.000001, # coarse
        0.000003, # coarse
        0.0000001, # workhorse
        0.00000003, 
        0.00000001, # diminishing returns
        #0.000000003,
        #0.000000001, #superfine
        #0.0000000003, 
        #0.0000000001, 
        #0.00000000001, 
]:
    cmdstr = './safewithdrawal_linearalloc.py %.12f %d %f %s' % (learning_rate, max_unimproved_steps, gamma, fileprefix)
    print(cmdstr)
    os.system(cmdstr)

