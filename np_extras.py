# A collection of functions created for general purposes.

import traceback

def checkForNone(*args):
  """Check that the recieving arguments are not empty."""
  try:
    for n in args:
      assert n != None
  except Exception as err:
    print("TEST FAILED: "+traceback.format_exc())

def worldToUnitCoordinates(pos: tuple, worldLimit: tuple) -> tuple:
  """Convert world coordinates to unit coordinates.
     World coordinates are between -inf to inf.
     Unit coordinates are between -1.0 and 1.0."""
  if len(pos) <= 3:
    newPos = []
    for i in range(len(pos)):
      newPos.append(pos[i] / worldLimit[i])
    return tuple(newPos)
  else:
    print(f"Position has a dimension of {len(pos)}")

def unitToWorldCoordinates(pos: tuple, worldLimit: tuple) -> tuple:
  """Convert unit coordinates to world coordinates.
     Unit coordinates are between -1.0 and 1.0.
     World coordinates are between -inf to inf."""
  if len(pos) <= 3:
    newPos = []
    for i in range(len(pos)):
      newPos.append(pos[i] * worldLimit[i])
    return tuple(newPos)
  else:
    print(f"Position has a dimension of {len(pos)}")

def worldToPixelCoordinates(screenSize: tuple, pos: tuple, worldLimit: float) -> tuple:
  """Convert world coordinates to pixel coordinates.
     World coordinates are between -inf to inf.
     Pixel coordinates are between 0 to screen size max.
     NOTE: One time pass, should not be used since this is only for display."""
  if len(pos) <= 3:
    return (pos[0]*(round(screenSize[0]/2)/worldLimit[0]),
            pos[1]*(round(screenSize[1]/2)/worldLimit[1]),
            pos[2]*(round((screenSize[0]+screenSize[1])/2)/worldLimit[2])) # The Z-coordinate is mostly negligible.
  else:
    print(f"Position has a dimension of {len(pos)}")

def cartesianToCom(screenSize: tuple, pos: tuple) -> tuple:
  """Convert a cartesian coordinate into a computer screen coordinate.
     NOTE: that this only applies to pixel coordinate offsets."""
  center = (round(screenSize[0]/2), round(screenSize[1]/2), 0)
  return (round(center[0]+pos[0]), round(center[1]+(-1*pos[1])))

def comToCartesian(screenSize: tuple, pos: tuple) -> tuple:
  """Convert a computer screen coordinate into a cartesian coordinate.
     NOTE: that this only applies to pixel coordinate offsets."""
  center = (int(screenSize[0]/2), int(screenSize[1]/2), 0)
  return (round(pos[0]-center[0]), round(center[1]-pos[1]))

if __name__ == "__main__":
  #screenSize = (1000, 1000) # In pixel coordinates
  #pos = (1.0, -1.0, 0)     # In unit coordinates
  #worldLimit = (10, 10, 10) # In world coordinates
  #
  #pos = (-4, 4, 2)
  #print(pos)
  #pos = worldToPixelCoordinates(screenSize, pos, worldLimit)
  #print(pos)
  #pos = cartesianToCom(screenSize, pos)
  #print(pos)
  pass
  
  