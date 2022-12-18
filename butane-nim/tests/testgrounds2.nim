# me learning how pointers work

# var
#     x : int = 5
#     y : ptr int = x.addr

# echo "x:",x," y:",y[]
# x += 10
# echo "x:",x," y:",y[]

# This example shows how to draw the surface of a control.

# import nigui

# app.init()
# var window = newWindow()
# window.width = 500
# window.height = 500

# var control1 = newControl()
# window.add(control1)
# # Creates a drawable control

# control1.widthMode = WidthMode_Fill
# control1.heightMode = HeightMode_Fill
# # Let it fill out the whole window

# control1.onDraw = proc (event: DrawEvent) =
#   let canvas = event.control.canvas
#   # A shortcut

#   canvas.areaColor = rgb(30, 30, 30) # dark grey
#   canvas.fill()
#   # Fill the whole area

#   canvas.setPixel(0, 0, rgb(255, 0, 0))
#   # Modifies a single pixel

#   canvas.lineColor = rgb(255, 0, 0) # red
#   canvas.drawLine(60, 10, 110, 40)
#   # Draws a line

# control1.onMouseButtonDown = proc (event: MouseEvent) =
#   echo(event.button, " (", event.x, ", ", event.y, ")")
#   # Shows where the mouse is clicked in control-relative coordinates

# window.show()
# app.run()

import sequtils, strutils

# Define a function that multiplies two matrices together
proc matrixMultiply(matrixA, matrixB: seq[seq[float]]): seq[seq[float]] =
  # Define the resulting matrix, which will have the same number of rows as matrixA
  # and the same number of columns as matrixB
  for i in 0..<result.len:
    for j in 0..<result[i].len:
      result[i][j] = 0
      
  # Multiply each element of matrixA by the corresponding element in matrixB,
  # and add the results together to get the value for the resulting matrix
  for i in 0..<matrixA.len:
    for j in 0..<matrixB[0].len:
      for k in 0..<matrixA[0].len:
        result[i][j] += matrixA[i][k] * matrixB[k][j]
        
  # Return the resulting matrix
  return result


# Define some sample matrices
let matrixA = @[[1, 2], [3, 4]]
let matrixB = @[[5, 6], [7, 8]]

# Multiply the matrices together
let res = matrixMultiply(matrixA, matrixB)

# Print the resulting matrix
echo "Result: "
for row in res:
    echo row