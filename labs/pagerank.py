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

"""
This is an example implementation of PageRank. For more conventional use,
Please refer to PageRank implementation provided by graphx
"""
from __future__ import print_function

import re
import sys
from operator import add

from pyspark import SparkContext


def computeContribs(nodes, rank):
    """Calculates NODE contributions to the rank of other NODEs."""
    num_nodes = len(nodes)
    for node in nodes:
        yield (node, rank / num_nodes)


def parseNeighbors(node):
    """Parses a node pair string into node pair."""
    parts = re.split(r'\s+', node)
    return parts[0], parts[1]

def printNeighbours(node):
    """Parses a node pair string into node pair."""
    print("%s: %s." % (node[0], node[1]))
def printNodeMap(x):
    print ('%8s: ' % x[0],end="")
    for nd in x[1]:
        print(' %8s ' % nd,end="");
    print(end='\n') ;



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pagerank <file> <iterations>", file=sys.stderr)
        exit(-1)

    print("""WARN: This is a naive implementation of PageRank and is
          given as an example! Please refer to PageRank implementation provided by graphx""",
          file=sys.stderr)

    sc=SparkContext(appName="PageRank")
    sc.setLogLevel("FATAL");
    # Loads in input file. It should be in format of:
    #     NODE         neighbor NODE
    #     NODE         neighbor NODE
    #     NODE         neighbor NODE
    #     ...
    lines = sc.textFile(sys.argv[1]).filter(lambda x : x[0] != '#')
    # Loads all NODEs from input file and initialize their neighbors.
    links = lines.map(lambda node: parseNeighbors(node)).distinct().groupByKey().cache()
    nrk   = links.count();
    #for node in links.collect():
    #    printNodeMap(node);
    
    
    # Loads all NODEs with other NODE(s) link to from input file
    # and initialize ranks of them to one.
    ranks = links.map(lambda node_neighbors: (node_neighbors[0], 1.0))
    #for (node, rank) in ranks.sortBy(lambda x: x[0]).collect():
    #    print("%s has rank: %s." % (node, rank))


    
    # Calculates and updates NODE ranks continuously using PageRank algorithm.
    for iteration in range(int(sys.argv[2])):
        print("Iteration: %s"%(iteration));

        # Calculates NODE contributions to the rank of other NODEs.
        contribs = links.join(ranks,numPartitions=8).flatMap(
            lambda node_nodes_rank: computeContribs(node_nodes_rank[1][0], node_nodes_rank[1][1]))

        # Re-calculates NODE ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)

    # Collects all NODE
    # ranks and dump them to console.
    for (node, rank) in ranks.sortBy(lambda x: x[0]).collect():
        print("%s has rank: %s." % (node, rank))

sc.stop()
