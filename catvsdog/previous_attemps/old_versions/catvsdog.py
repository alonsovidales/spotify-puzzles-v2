#!/usr/bin/env python

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-01-14"

class CatVsDog:
    __debug = False

    def resolve(self):
        maxHappyVoters = 0
        finalGraph = {}
        # Create the list of partners on the other side
        partnersToVisit = []
        if self.__totalCatLovers < self.__totalDogLovers:
            toCompare = 'C'
        else:
            toCompare = 'D'

        maxHappyVoters = 0
        for votes, voteInfo in self.__votes.items():
            if votes[0] == toCompare:
                if self.__debug:
                    print "---- Current Node: %s ----" % (votes)
                    print "Opposite Partners set: %s" % (voteInfo['partners'])

                finalPartners = None
                voters = 0
                for oppositPartner in voteInfo['partners']:
                    voters += self.__votes[oppositPartner]['votes']
                    if finalPartners == None:
                        finalPartners = self.__votes[oppositPartner]['partners']
                    else:
                        finalPartners &= self.__votes[oppositPartner]['partners']

                if self.__debug:
                    print "Final Partners set: %s" % (finalPartners)
                if finalPartners != None:
                    for finalPartner in finalPartners:
                        voters += self.__votes[finalPartner]['votes']

                if self.__debug:
                    print "Votes for %s: %s" % (votes, voters)
                if maxHappyVoters < voters:
                    maxHappyVoters = voters

        if self.__debug:
            print "VotesGraph: %s" % (self.__votes)
            print "Max happy voters: %s" % (maxHappyVoters)

        if maxHappyVoters < self.__totalCatLovers:
            maxHappyVoters = self.__totalCatLovers

        if maxHappyVoters < self.__totalDogLovers:
            maxHappyVoters = self.__totalDogLovers

        return maxHappyVoters

    def __init__(self, inNumCats, inNumDogs, inVotes):
        self.__catLovers = []
        self.__dogLovers = []
        self.__totalCatLovers = 0
        self.__totalDogLovers = 0
        self.__votes = {}

        grouppedPref = {}

        for vote in inVotes:
            if vote in self.__votes:
                self.__votes[vote]['votes'] += 1
                if vote[0] == 'C':
                    self.__totalCatLovers += 1
                else:
                    self.__totalDogLovers += 1
            else:
                voteParts = vote.split()
                if vote[0] == 'C':
                    self.__totalCatLovers += 1
                    self.__catLovers.append([vote, voteParts])
                    oppositeLovers = self.__dogLovers
                else:
                    self.__totalDogLovers += 1
                    self.__dogLovers.append([vote, voteParts])
                    oppositeLovers = self.__catLovers

                partners = set()
                for opposite in oppositeLovers:
                    if voteParts[0] <> opposite[1][1] and voteParts[1] <> opposite[1][0]:
                        partners.add(opposite[0])
                        self.__votes[opposite[0]]['partners'].add(vote)

                self.__votes[vote] = {
                    'votes': 1,
                    'partners': partners
                }

        if self.__debug:
            print "%s - %s" % (self.__totalCatLovers, self.__totalDogLovers)
            print "Input Votes: %s" % (inVotes)
            print "Votes: %s" % (self.__votes)

if __name__ == "__main__":
    # I'll use raw_input to get the lines because I can't import fileinput on the test server
    problems = int(raw_input())
    for problem in xrange(0, problems):
        problemInfo = map(int, raw_input().split())
        votes = []
        for problemLine in xrange(0, problemInfo[2]):
            votes.append(raw_input())

        print CatVsDog(problemInfo[0], problemInfo[1], votes).resolve()
