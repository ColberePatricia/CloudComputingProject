#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import re
import sys
from operator import add

from pyspark import SparkContext

def println(x): print("%s" % x)
def printEdge(x): print("(%d,%d)" % (x[0], x[1])),
def printDegree(x): print("Degree of node %8d : %8d" % (x[0], x[1])),
def printNodeMap(x):
    print ('%8d: ' % x[0],end="")
    for nd in x[1]:
        print(' %8d ' % nd,end="");
    print(end='\n') ;
        
        
def parseEdges(nodes):
    """Parses a node pair string into nodes pair."""
    parts = re.split(r'\s+', nodes)
    return int(parts[0]), int(parts[1])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: node_degree <file>", file=sys.stderr)
        exit(-1)
    sc = SparkContext(appName="InOut")
    sc.setLogLevel("FATAL");
    lines = sc.textFile(sys.argv[1], 20).filter(lambda x : x[0] != '#')
    edges = lines.map(lambda nodes: parseEdges(nodes)).distinct()
    graph = edges.groupByKey().cache();
    degrees = graph.map(lambda nodemap: (nodemap[0],len(nodemap[1])));
    for degree in degrees.sortByKey().collect():
        printDegree(degree);
    for node in graph.collect():
        printNodeMap(node);

sc.stop()
