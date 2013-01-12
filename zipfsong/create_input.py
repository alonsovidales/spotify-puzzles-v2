import random

songs = 50000
toShow = 100

print "%s %s" % (songs, toShow)
for song in xrange(0, 50000):
    print "%s song_%s" % (random.randint(0, 10000000000000), song)
