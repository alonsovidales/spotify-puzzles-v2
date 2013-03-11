import random

samples = 100
catsDogs = 100
voters = 500

print samples
for sample in xrange(0, samples):
    print "%s %s %s" % (catsDogs, catsDogs, voters)
    for voter in xrange(0, voters):
        if random.randint(0, 1) == 1:
            print "C%s D%s" % (random.randint(0, catsDogs), random.randint(0, catsDogs))
        else:
            print "D%s C%s" % (random.randint(0, catsDogs), random.randint(0, catsDogs))
