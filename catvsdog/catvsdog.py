#!/usr/bin/env python

"""
This version didn't pass the tests by timeout :'( I don't know why, only takes
3.7 secs on the wrost of the cases, 100 tests, of 500 votes each one. 0.037 sec
by each one.
"""

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-01-14"

class CatVsDog:
    __debug = False
    __votesList = None

    def resolve(self):
        catLovers = []
        dogLovers = []
        totalCatLovers = 0
        totalDogLovers = 0
        votes = {}

        byCatLove = {}
        byCatHate = {}
        byDogLove = {}
        byDogHate = {}

        for vote in self.__votesList:
            if vote in votes:
                votes[vote]['votes'] += 1
                if vote[0] == 'C':
                    totalCatLovers += 1
                else:
                    totalDogLovers += 1
            else:
                voteParts = vote.split()
                if vote[0] == 'D':
                    totalDogLovers += 1
                    dogLovers.append([vote, voteParts])

                    if voteParts[0] in byDogLove:
                        byDogLove[voteParts[0]].add(vote)
                    else:
                        byDogLove[voteParts[0]] = set([vote])

                    if voteParts[1] in byDogHate:
                        byDogHate[voteParts[1]].add(vote)
                    else:
                        byDogHate[voteParts[1]] = set([vote])
                else:
                    totalCatLovers += 1
                    catLovers.append([vote, voteParts])

                    if voteParts[0] in byCatLove:
                        byCatLove[voteParts[0]].add(vote)
                    else:
                        byCatLove[voteParts[0]] = set([vote])

                    if voteParts[1] in byCatHate:
                        byCatHate[voteParts[1]].add(vote)
                    else:
                        byCatHate[voteParts[1]] = set([vote])

                votes[vote] = {
                    'votes': 1,
                    'partners': set()
                }

        setOfDogLoversVotes = set([vote[0] for vote in dogLovers])
        for catLover in catLovers:
            toRemove = byDogLove.get(catLover[1][1], set()) | byDogHate.get(catLover[1][0], set())
            votes[catLover[0]]['partners'] = setOfDogLoversVotes - toRemove

        setOfCatLoversVotes = set([vote[0] for vote in catLovers])
        maxHappyVoters = 0
        for dogLover in dogLovers:
            if self.__debug:
                print "--- Checking: %s ---" % (dogLover[0])
            totalHappyVotes = 0
            toRemove = byCatLove.get(dogLover[1][1], set()) | byCatHate.get(dogLover[1][0], set())
            #votes[dogLover[0]]['partners'] = setOfCatLoversVotes - toRemove

            dogLoversPartners = setOfDogLoversVotes
            for partner in setOfCatLoversVotes - toRemove:
                totalHappyVotes += votes[partner]['votes']
                dogLoversPartners &= votes[partner]['partners']

            if self.__debug:
                print "Parterns: %s" % (setOfCatLoversVotes - toRemove)
                print "Self parterns: %s" % (dogLoversPartners)

            for dogLoversPartner in dogLoversPartners:
                totalHappyVotes += votes[dogLoversPartner]['votes']

            if maxHappyVoters < totalHappyVotes:
                maxHappyVoters = totalHappyVotes
            #print "Votes for: %s: %s" % (dogLover[0], totalHappyVotes)

        if self.__debug:
            print "%s - %s" % (totalCatLovers, totalDogLovers)
            print "Input Votes: %s" % (self.__votesList)
            print "Votes: %s" % (votes)

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
