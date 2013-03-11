#!/usr/bin/env python

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-01-14"

class CatVsDog:
    __debug = False

    def __checkCompatibility(self, inGroupPos, inVote):
        votesList = inVote.split()
        for vote in self.__groups[inGroupPos]['votes']:
            groupVotesList = vote.split()
            if groupVotesList[0] == votesList[1] or groupVotesList[1] == votesList[0]:
                return False

        return True

    def resolve(self):
        for catLoverVote in self.__catLovers:
            catLoverVoteList = catLoverVote.split()
            for dogLoverVote in self.__dogLovers:
                dogLoverVoteList = dogLoverVote.split()
                if catLoverVoteList[0] <> dogLoverVoteList[1] and catLoverVoteList[1] <> dogLoverVoteList[0]:
                    self.__votes[catLoverVote]['partners'].add(dogLoverVote)
                    self.__votes[dogLoverVote]['partners'].add(catLoverVote)

        maxHappyVoters = 0
        finalGraph = {}
        # Create the list of partners in the other side
        partnersToVisit = []
        for votes, voteInfo in self.__votes.items():
            votesList = votes.split()
            try:
                partnersToVisit += voteInfo['partners']
                finalGraph[votes]['votes'] += voteInfo['votes']
            except:
                finalGraph[votes] = {
                    'notAllowedPartners': {
                        'left': set(),
                        'right': set(),
                    },
                    'partners': voteInfo['partners'],
                    'votes': voteInfo['votes']
                }
                partnersToVisit += voteInfo['partners']

            for votePartner in voteInfo['partners']:
                votePartnerList = votePartner.split()
                finalGraph[votes]['notAllowedPartners']['left'].add(votePartnerList[1])
                finalGraph[votes]['notAllowedPartners']['right'].add(votePartnerList[0])
                

        for vote, toDo in finalGraph.items():
            if self.__debug:
                print "---- Current Node: %s ----" % (vote)
            visitedPartners = set([vote])
            currentVotes = toDo['votes']
            for partnerToVisit in toDo['partners']:
                if self.__debug:
                    print "Direct Partner: %s" % (partnerToVisit)
                currentVotes += self.__votes[partnerToVisit]['votes']
                for partner in self.__votes[partnerToVisit]['partners']:
                    if partner not in visitedPartners:
                        visitedPartners.add(partner)
                        partnerList = partner.split()
                        if self.__debug:
                            print "Checking Partner: %s - Not: %s" % (partner, toDo['notAllowedPartners'])
                        if partnerList[0] not in toDo['notAllowedPartners']['left'] and partnerList[1] not in toDo['notAllowedPartners']['right']:
                            currentVotes += self.__votes[partner]['votes']

            if self.__debug:
                print "CurrentVotes: %s" % (currentVotes)
            if currentVotes > maxHappyVoters:
                maxHappyVoters = currentVotes

        if self.__debug:
            print "VotesGraph: %s" % (self.__votes)
            print "Max happy votters: %s" % (maxHappyVoters)

        if maxHappyVoters < self.__totalCatLovers:
            maxHappyVoters = self.__totalCatLovers

        if maxHappyVoters < self.__totalDogLovers:
            maxHappyVoters = self.__totalDogLovers

        return maxHappyVoters

    def __init__(self, inNumCats, inNumDogs, inVotes):
        self.__catLovers = set()
        self.__dogLovers = set()
        self.__totalCatLovers = 0
        self.__totalDogLovers = 0
        self.__votes = {}

        for vote in inVotes:
            if vote[0] == 'C':
                self.__totalCatLovers += 1
                self.__catLovers.add(vote)
            else:
                self.__totalDogLovers += 1
                self.__dogLovers.add(vote)

            try:
                self.__votes[vote]['votes'] += 1
            except:
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
