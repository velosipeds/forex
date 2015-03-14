
import numpy
from pylearn2.datasets.dense_design_matrix import DenseDesignMatrix
import marshal
 
def load_data(start, stop):
    
    with open('marshal.dat', 'rb') as file:
        data = marshal.load(file)

    x = []
    y = []

    offset = 10
    infill = 3

    for i in xrange(len(data)):
        if len(data[i]) > 1000:
            for j in xrange(len(data[i])):
                if j > 200 and j < len(data[i]) - offset and j % infill == 0:
                    row = data[i][j-200:j]
                    average = sum(row) / float(len(row))
                    x.append([(item - average) / average * 500. for item in row])
                    y.append([1, 0] if data[i][j+offset] > data[i][j] else [0, 1])

    X = numpy.asarray(x)
    Y = numpy.asarray(y) 

    X = X[start:stop, :]
    Y = Y[start:stop, :]
 
    return DenseDesignMatrix(X=X, y=Y)