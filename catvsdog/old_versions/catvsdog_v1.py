#!/usr/bin/env python

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-01-14"

class CatVsDog:
    __debug = False
    __numCats = None
    __numDogs = None
    __votes = None
    __groups = []

    def resolve(self):
        possibleGroups = []

        for votes, voters in self.__votes.items():
            votesList = votes.split()
            for groupPos in xrange(0, len(possibleGroups)):
                compatible = True
                compatibleVotes = set([votes])
                compatibleVoters = self.__votes[votes]

                for votesGroup in possibleGroups[groupPos]['votes']:
                    votesGroupList = votesGroup.split()
                    if votesGroupList[0] <> votesList[1] and votesGroupList[1] <> votesList[0]:
                        compatibleVotes.add(votesGroup)
                        compatibleVoters += self.__votes[votesGroup]
                    else:
                        compatible = False

                if self.__debug:
                    print "Checking: %s - %s" % (votesList, possibleGroups[groupPos])
                if compatible:
                    possibleGroups[groupPos]['votes'].add(votes)
                    possibleGroups[groupPos]['voters'] += voters
                else:
                    # Check if duplicated, and in this case, don't add the group
                    duplicated = False
                    for groupPos in xrange(0, len(possibleGroups)):
                        if compatibleVoters == possibleGroups[groupPos]['voters'] and len(compatibleVotes - possibleGroups[groupPos]['votes']) == 0:
                            duplicated = True
                            break

                    #if not duplicated:
                    if True:
                        possibleGroups.append({
                            'votes': compatibleVotes,
                            'voters': compatibleVoters
                        })

            if len(possibleGroups) == 0:
                possibleGroups.append({
                    'votes': set([votes]),
                    'voters': voters
                })

            #print len(possibleGroups)
            if self.__debug:
                print possibleGroups

        maxVoters = 0
        for possibleGroup in possibleGroups:
            if maxVoters < possibleGroup['voters']:
                maxVoters = possibleGroup['voters']

        return maxVoters

    def __init__(self, inNumCats, inNumDogs, inVotes):
        self.__numCats = inNumCats
        self.__numDogs = inNumDogs
        self.__votes = {}
        self.__groups = []

        for vote in inVotes:
            self.__votes[vote] = self.__votes.get(vote, 0) + 1

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
