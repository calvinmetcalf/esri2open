from struct import pack

def linearRing(coordinates):
    values =[0]
    outnum = "I"
    for coord in coordinates:
        outnum=outnum+"dd"
        values[0]=values[0]+1
        values.append(coord[0])
        values.append(coord[1])
    return [outnum,values]
def multiRing(coordinates):
    values =[0]
    outnum = "I"
    for lineString in coordinates:
        [ptrn,coords]=linearRing(lineString)
        outnum=outnum+ptrn
        values[0]=values[0]+1
        values.extend(coords)
    return [outnum,values]
def metaMultiRing(coordinates):
    values =[0]
    outnum = "I"
    for lineStrings in coordinates:
        [ptrn,coords]=multiRing(lineStrings)
        outnum=outnum+ptrn
        values[0]=values[0]+1
        values.extend(coords)
    return [outnum,values]
def makePoint(c):
    return ["Idd",[1,c[0],c[1]]]
def makeMultiPoing(c):
    values = ["I",[4]]
    [ptrn,coords]=linearRing(c)
    values[0]=values[0]+ptrn
    values[1].extend(coords)
    return values
def makeLineString(c):
    values = ["I",[2]]
    [ptrn,coords]=linearRing(c)
    values[0]=values[0]+ptrn
    values[1].extend(coords)
    return values
def makeMultiLineString(c):
    values = ["I",[5]]
    [ptrn,coords]=multiRing(c)
    values[0]=values[0]+ptrn
    values[1].extend(coords)
    return values
def makePolygon(c):
    values = ["I",[3]]
    [ptrn,coords]=multiRing(c)
    values[0]=values[0]+ptrn
    values[1].extend(coords)
    return values
def makeMultiPolygon(c):
    values = ["I",[6]]
    [ptrn,coords]=metaMultiRing(c)
    values[0]=values[0]+ptrn
    values[1].extend(coords)
    return values
def makeCollection(geometries):
    values = ["II",[7,0]]
    for geom in geometries:
        [ptrn,coords]=parseGeo(geom)
        values[0]=values[0]+ptrn
        values[1].extend(coords)
        values[1][1]=values[1][1]+1
    return values
def parseGeo(geometry):
    if geometry["type"]=="Point":
        return makePoint(geometry["coordinates"])
    elif geometry["type"]=="MultiPoint":
        return makeMultiPoing(geometry["coordinates"])
    elif geometry["type"]=="LineString":
        return makeLineString(geometry["coordinates"])
    elif geometry["type"]=="MultiLineString":
        return makeMultiLineString(geometry["coordinates"])
    elif geometry["type"]=="Polygon":
        return makePolygon(geometry["coordinates"])
    elif geometry["type"]=="MultiPolygon":
        return makeMultiPolygon(geometry["coordinates"])
    elif geometry["type"]=="GeometryCollection":
        return makeCollection(geometry["geometries"])

def makeWKB(geometry):
    values = ["<B",1]
    [ptrn,coords]=parseGeo(geometry)
    values[0]=values[0]+ptrn
    values.extend(coords)
    return pack(*values)
