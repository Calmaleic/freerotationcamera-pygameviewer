# A collection of matrix operations.
# NOTE: That no matrix shall have more than one sub-row element
#       e.g. [[[0]]] is not permitted.

import numpy as np
import math
import random
import operator
import itertools

def zeroes(shape: tuple) -> list:
  """Generate a new matrix initialized all to zeroes."""
  if shape[0] != 0 and shape[1] != 0:
    return [[0 for n in range(shape[1])] for n in range(shape[0])]

def identity(shape: tuple) -> list:
  """Generate a new identity matrix with diagonal 1's (pivots)."""
  if shape[0] == shape[1]:
    mat = zeroes(shape)
    for i in range(len(mat)):
      mat[i][i] = 1
    return mat

def randomize(mat: list) -> list:
  """Randomize the values of a matrix."""
  for i in range(len(mat)):
    for j in range(len(mat[0])):
      mat[i][j] = random.randint(0, 10)
  return mat

def allset(mat: list, num: int) -> list:
  """Set all values in the matrix to the num."""
  for i in range(len(mat)):
    for j in range(len(mat[0])):
      mat[i][j] = num
  return mat

def multiplication(mat1: list, mat2: list) -> list:
  """Perform matrix multiplication or dot products between two matrices."""
  if checkDimensions(mat1, mat2):
    m1 = np.array(mat1)
    m2 = np.array(mat2)
    m3 = np.matmul(mat1, mat2)
    return m3.tolist()
  else:
    print("Unable to perform due to dimensions."
         f"{getDimensions(mat1)} --- {getDimensions(mat2)}")

def getDimensions(mat: list) -> tuple: # Or the shape as they call it
  """Get the dimensions of a matrix."""
  return (len(mat), len(mat[0]))

def checkDimensions(mat1: list, mat2: list) -> bool:
  """Check between two matrices their dimensions.
     Remember mxn, where m is the size of the columns, and n is vice versa."""
  return True if len(mat1[0]) == len(mat2) else False

def reshape(mat: list, shape: tuple) -> list:
  """Perform a reshape on the matrix."""
  m = np.array(mat)
  m = np.reshape(m, shape)
  m = m.tolist()
  if type(m[0]) != list:
    return [m]
  else:
    return m

def grow(mat: list, shape: tuple) -> list: # TODO
  """Grow and pad to the necessary size matrix."""
  if len(mat) >= shape[0] or len(mat[0]) >= shape[1]:
    m = zeroes(shape)
    for i in range(len(mat)):
      for j in range(len(mat[0])):
        m[i][j] = mat[i][j]
    return m
  else:
    print("The shape specified is smaller than the input matrix.")

def shrink(mat: list, shape: tuple) -> list: # TODO
  """Shrink and truncate to the necessary size matrix."""
  if len(mat) <= shape[0] or len(mat[0]) <= shape[1]:
    m = zeroes(shape)
    for i in range(len(m)):
      for j in range(len(m[0])):
        m[i][j] = mat[i][j]
    return m
  else:
    print("The shape specified is larger than the input matrix.")

def powerset(iterable) -> list:
  """Retrieve the power set of the matrix."""
  m = itertools.chain.from_iterable(itertools.combinations(iterable, r) for r in range(len(iterable)+1))
  return m

def getTwoExp(comb: tuple, exp: int) -> list:
  """Get the 2^exp product of a matrix table."""
  return list(itertools.product(comb, repeat=exp))

def tupleToMatrix(tup: tuple) -> list: 
  """Convert a one-dim tuple to a matrix."""
  return [list(tup)]

def matrixToTuple(mat: list) -> tuple:
  """Convert a matrix to a one-dim tuple."""
  return tuple(mat[0])

def operation(mat1: list, mat2: list, operator) -> list:
  """Perform an operation between two equivalent matrices."""
  if len(mat1) == len(mat2):
    m = zeroes(getDimensions(mat1))
    for i in range(len(mat1)):
      for j in range(len(mat1[0])):
        m[i][j] = operator(mat1[i][j], mat2[i][j])
    return m
  else:
    print("Invalid matrices.")

def printAsRows(mat: list):
  """Print the matrix by rows."""
  if len(mat) == 0:
    print("Empty")
  else:
    for i in range(len(mat)):
      print(mat[i])

def printAsMatrix(mat: list):
  """Print the matrix with rows and columns."""
  if len(mat) == 0:
    print("Empty")
  else:
    for i in range(len(mat)):
      for j in range(len(mat[0])):
        print(mat[i][j], end=" ")
      print("")
    print("")

if __name__ == "__main__":
  pass