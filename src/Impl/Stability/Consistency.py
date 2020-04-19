def consistency(cl1, cl2):
    centerSet1 = set([c.id for c in cl1])   # centers at t-1
    centerSet2 = set([c.id for c in cl2])   # centers at t
    return len(centerSet2.difference(centerSet1))
