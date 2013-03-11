#!/usr/bin/env python

"""
This version didn't pass the tests by timeout :'( I don't know why, only takes
3.7 secs on the wrost of the cases, 100 tests, of 500 votes each one. 0.037 sec
by each one.
"""

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-01-14"

import bipartite_match

class CatVsDog:
    __debug = False
    __votesList = None

    def resolve(self):
        catLoversParts = []
        dogLoversParts = []
        totalCatLovers = 0
        totalDogLovers = 0
        votes = {}

        byDogLove = {}
        byDogHate = {}
        byCatLove = {}
        byCatHate = {}

        dogLovers = set()
        catLovers = set()

        # Create the bipartite graph and the byXXXLove and by byXXXHate dictionaries,
        # that will contain the direct access to the sets of voters that likes a determinate
        # cat/dog and hates a determiante cat/dog
        vertexWeight = {}
        sufix = 0
        for vote in self.__votesList:
            voteSufix = "%s %d" % (vote, sufix)
            voteParts = vote.split()
            if vote[0] == 'D':
                totalDogLovers += 1
                if voteParts[0] in byDogLove:
                    byDogLove[voteParts[0]].add(voteSufix)
                else:
                    byDogLove[voteParts[0]] = set([voteSufix])

                if voteParts[1] in byDogHate:
                    byDogHate[voteParts[1]].add(voteSufix)
                else:
                    byDogHate[voteParts[1]] = set([voteSufix])
                dogLoversParts.append([voteSufix, voteParts])
                dogLovers.add(voteSufix)
            else:
                totalCatLovers += 1
                if voteParts[0] in byCatLove:
                    byCatLove[voteParts[0]].add(voteSufix)
                else:
                    byCatLove[voteParts[0]] = set([voteSufix])

                if voteParts[1] in byCatHate:
                    byCatHate[voteParts[1]].add(voteSufix)
                else:
                    byCatHate[voteParts[1]] = set([voteSufix])
                catLoversParts.append([voteSufix, voteParts])
                catLovers.add(voteSufix)

            sufix += 1

        # If we don't have opposite votters, return the whole list of votters
        if totalDogLovers == 0 or totalCatLovers == 0:
            return len(self.__votesList)

        # Create the graph edges from uncompatible cat lovers to dog lovers
        for catLover in catLoversParts:
            # Get the uncompatible list of friends by each vertex
            votes[catLover[0]] = byDogLove.get(catLover[1][1], set()) | byDogHate.get(catLover[1][0], set())

        minUnfriends = len(self.__votesList)
        # Create the graph edges from uncompatible dog lovers to cat lovers
        for dogLover in dogLoversParts:
            # Get the uncompatible list of friends by each vertex
            votes[dogLover[0]] = byCatLove.get(dogLover[1][1], set()) | byCatHate.get(dogLover[1][0], set())

            # The unfriends of my friends are my unfriends :)
            for unfriendOtherSide in (catLovers - votes[dogLover[0]]):
                unfriendOtherSideParts = unfriendOtherSide.split()
                votes[dogLover[0]] |= byDogLove.get(unfriendOtherSideParts[1], set()) | byDogHate.get(unfriendOtherSideParts[0], set())

            if len(votes[dogLover[0]]) < minUnfriends:
                minUnfriends = len(votes[dogLover[0]])

        # Now get the uncompatibles on the same side for cat lovers
        for catLover in catLoversParts:
            # The unfriends of my friends are my unfriends :)
            for unfriendOtherSide in (dogLovers - votes[catLover[0]]):
                unfriendOtherSideParts = unfriendOtherSide.split()
                votes[catLover[0]] |= byCatLove.get(unfriendOtherSideParts[1], set()) | byCatHate.get(unfriendOtherSideParts[0], set())

            if len(votes[catLover[0]]) < minUnfriends:
                minUnfriends = len(votes[catLover[0]])

        if self.__debug:
            print "Min unfriends - %s" % (minUnfriends)
            print "%s - %s" % (totalCatLovers, totalDogLovers)
            print "Input Votes: %s" % (self.__votesList)
            print "Votes: %s" % (votes)

        maxHappyVoters = len(self.__votesList) - minUnfriends

        if maxHappyVoters < totalCatLovers:
            maxHappyVoters = totalCatLovers

        if maxHappyVoters < totalDogLovers:
            maxHappyVoters = totalDogLovers

        return maxHappyVoters

    def __init__(self, inNumCats, inNumDogs, inVotes):
        self.__votesList = inVotes

if __name__ == "__main__":
    # I'll use raw_input to get the lines because I can't import fileinput on the test server
    problems = int(raw_input())
    results = []
    for problem in xrange(0, problems):
        problemInfo = map(int, raw_input().split())
        votes = []
        for problemLine in xrange(0, problemInfo[2]):
            votes.append(raw_input())

        results.append(CatVsDog(problemInfo[0], problemInfo[1], votes).resolve())

    print "\n".join(map(str, results))
    #print " ".join(map(str, results))
