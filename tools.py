def immutabledict2dict(imdict):
    d = {}
    for i in imdict: 
        d[i] = imdict[i]
    return d