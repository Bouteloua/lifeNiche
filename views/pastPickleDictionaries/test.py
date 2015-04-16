import cPickle

g9 = cPickle.load(open('occurrenceDictionary.pickle', 'rb'))

counter = 0
for i in g9:                                                
    print i
    counter += 1

print counter

