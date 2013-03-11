#!/usr/bin/env python

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-01-14"

from bipartite_match import bipartiteMatch

class CatVsDog:
    __debug = False
    __votesList = None

    def resolve(self):
        # This graph will contain all the conflictive relations between voters
        bipartiteByCat = {}

        catLovers = []
        # Dog lovers groupped by the dog who they loves
        byDogLove = {}
        # Dog lovers groupped by the cat who they hate
        byDogHate = {}

        # This counter will be used to avoid problems with duplicate votes on the
        # sets and the key of the dict who conforms the graph
        count = 0
        for vote in self.__votesList:
            vote = "%s %d" % (vote, count)
            count += 1
            if vote[0] == 'D':
                voteParts = vote.split()

                if voteParts[0] in byDogLove:
                    byDogLove[voteParts[0]].add(vote)
                else:
                    byDogLove[voteParts[0]] = set([vote])

                if voteParts[1] in byDogHate:
                    byDogHate[voteParts[1]].add(vote)
                else:
                    byDogHate[voteParts[1]] = set([vote])
            else:
                catLovers.append(vote)

        # Create the bipartite graph using a dictionary, the key will be the vote of the cat lover, and the
        # values a set with all the votes who have problems with the vote of the cat lover at the key
        for catVote in catLovers:
            catVoteParts = catVote.split()
            bipartiteByCat[catVote] = byDogLove.get(catVoteParts[1], set()) | byDogHate.get(catVoteParts[0], set())

        # Use the Hopcroft-Karp algorith in order to determinate the max cardinality, then we will know the
        # min number of conflictive votters that we have
        maxMatching, pred, unlayered = bipartiteMatch(bipartiteByCat)

        if self.__debug:
            print "Votes: %s" % (bipartiteByCat)
            print "Max matching %s" % (maxMatching)
            print "Dog love: %s" % (byDogLove)
            print "Dog hate: %s" % (byDogHate)


        # The max number of happy voters are the number of total voters minus the number of conflictive pairs (we can remove
        # one of the members of each pair)
        return len(self.__votesList) - len(maxMatching)

    def __init__(self, inVotes):
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

        results.append(CatVsDog(votes).resolve())

    print "\n".join(map(str, results))
