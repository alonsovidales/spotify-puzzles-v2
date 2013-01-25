#!/usr/bin/env python

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-01-14"

class CatVsDog:
    __debug = True
    __numCats = None
    __numDogs = None
    __votes = None
    __groups = []

    def resolve(self):
        catLovers = []
        bipartGraph = {}

        for votePos in xrange(0, len(self.__votes)):
            if self.__votes[votePos][0] == 'C':
                catLovers.append("%s %s" % (self.__votes[votePos], votePos))
                bipartGraph["%s %s" % (self.__votes[votePos], votePos)] = []
            else:
                bipartGraph["%s %s" % (self.__votes[votePos], votePos)] = []

        for voteDog in bipartGraph.keys():
            for voteCat in catLovers:
                voteCatList = voteCat.split()
                voteDogList = voteDog.split()
                if voteCatList[0] <> voteDogList[1] and voteCatList[1] <> voteDogList[0]:
                    bipartGraph[voteDog].append(voteCat)
                    bipartGraph[voteCat].append(voteDog)

        if self.__debug:
            print "Bipartite graph: %s" % (bipartGraph)

        if self.__debug:
            print maxMatching

        return len(maxMatching)

    def __init__(self, inNumCats, inNumDogs, inVotes):
        self.__numCats = inNumCats
        self.__numDogs = inNumDogs
        self.__votes = inVotes

        if self.__debug:
            print "Input Votes: %s" % (inVotes)
            print "Votes: %s" % (self.__votes)

if __name__ == "__main__":
    # I'll use raw_input to get the lines because I can't import fileinput on the test server
    lines = []
    while True:
        try:
            lines.append(raw_input())
        except (EOFError):
            break #end of file reached

    currentLine = 1
    while currentLine < len(lines):
        info = map(int, lines[currentLine].split())
        print CatVsDog(info[0], info[1], lines[currentLine + 1:info[2] + currentLine + 1]).resolve()
        currentLine += info[2] + 1
