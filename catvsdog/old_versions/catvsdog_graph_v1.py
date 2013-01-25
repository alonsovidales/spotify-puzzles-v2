#!/usr/bin/env python

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-01-14"

class CatVsDog:
    __debug = False

    def resolve(self):
        for catLoverVote in self.__catLovers:
            catLoverVoteList = catLoverVote.split()
            for dogLoverVote in self.__dogLovers:
                # 5s
                if catLoverVoteList[0] <> dogLoverVote[1][1] and catLoverVoteList[1] <> dogLoverVote[1][0]:
                    # 3s
                    self.__votes[catLoverVote]['partners'].add(dogLoverVote[0])
                    # 3s
                    self.__votes[dogLoverVote[0]]['partners'].add(catLoverVote)

        if self.__debug:
            print "Bipartite Graph %s" % (self.__votes)

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

        for vote in inVotes:
            if vote[0] == 'C':
                self.__totalCatLovers += 1
                self.__catLovers.append(vote)
            else:
                self.__totalDogLovers += 1
                self.__dogLovers.append([vote, vote.split()])

            if vote in self.__votes:
                self.__votes[vote]['votes'] += 1
            else:
                self.__votes[vote] = {
                    'votes': 1,
                    'partners': set()
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
