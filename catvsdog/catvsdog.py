#!/usr/bin/env python

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-01-14"

from bipartite_match import bipartiteMatch

class CatVsDog:
    __debug = False
    __votes_list = None

    def resolve(self):
        # This graph will contain all the conflictive relations between voters
        bipartite_by_cat = {}

        cat_lovers = []
        # Dog lovers groupped by the dog who they loves
        by_dog_love = {}
        # Dog lovers groupped by the cat who they hate
        by_dog_hate = {}

        # This counter will be used to avoid problems with duplicate votes on the
        # sets and the key of the dict who conforms the graph
        count = 0
        for vote in self.__votes_list:
            vote = "%s %d" % (vote, count)
            count += 1
            if vote[0] == 'D':
                vote_parts = vote.split()

                if vote_parts[0] in by_dog_love:
                    by_dog_love[vote_parts[0]].add(vote)
                else:
                    by_dog_love[vote_parts[0]] = set([vote])

                if vote_parts[1] in by_dog_hate:
                    by_dog_hate[vote_parts[1]].add(vote)
                else:
                    by_dog_hate[vote_parts[1]] = set([vote])
            else:
                cat_lovers.append(vote)

        # Create the bipartite graph using a dictionary, the key will be the vote of the cat lover, and the
        # values a set with all the votes who have problems with the vote of the cat lover at the key
        for cat_vote in cat_lovers:
            cat_vote_parts = cat_vote.split()
            bipartite_by_cat[cat_vote] = by_dog_love.get(cat_vote_parts[1], set()) | by_dog_hate.get(cat_vote_parts[0], set())

        # Use the Hopcroft-Karp algorith in order to determinate the max cardinality, then we will know the
        # min number of conflictive votters that we have
        max_matching, pred, unlayered = bipartiteMatch(bipartite_by_cat)

        if self.__debug:
            print "Votes: %s" % (bipartite_by_cat)
            print "Max matching %s" % (max_matching)
            print "Dog love: %s" % (by_dog_love)
            print "Dog hate: %s" % (by_dog_hate)


        # The max number of happy voters are the number of total voters minus the number of conflictive pairs (we can remove
        # one of the members of each pair)
        return len(self.__votes_list) - len(max_matching)

    def __init__(self, votes):
        self.__votes_list = votes

if __name__ == "__main__":
    # I'll use raw_input to get the lines because I can't import fileinput on the test server
    problems = int(raw_input())
    results = []
    for problem in xrange(0, problems):
        problem_info = map(int, raw_input().split())
        votes = []
        for problem_line in xrange(0, problem_info[2]):
            votes.append(raw_input())

        results.append(CatVsDog(votes).resolve())

    print "\n".join(map(str, results))
