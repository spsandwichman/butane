import arraymancer, std/math, boxy, windy, linearalgebra

# ------------------------------ default colors ------------------------------ #
const white* = rgb(255,255,255)
const black* = rgb(0,0,0)
const red* = rgb(255,0,0)
const green* = rgb(0,255,0)
const blue* = rgb(0,0,255)

# -------------------------------- conversion -------------------------------- #

proc rad*(oldDegrees: float): float = oldDegrees * (PI / 180.0)
proc deg*(oldDegrees: float): float = oldDegrees * (180.0 / PI)

proc dDown*(x: Vector[4]): Vector[3] = #truncates 4d vector, returns 3d vector
    result = [x[0],x[1],x[2]]

proc dUp*(x: Vector[3]): Vector[4] = #adds 1.0 element to 3d vector, returns 4d vector
    result = [x[0],x[1],x[2],1.0]

# --------------------------- basic tranformations --------------------------- #
proc makeTranslationMatrix*(v: Vector[3]): Matrix[4,4] =
    result = [
        [1.0, 0.0, 0.0, v[0]],
        [0.0, 1.0, 0.0, v[1]],
        [0.0, 0.0, 1.0, v[2]],
        [0.0, 0.0, 0.0, 1.0]
    ]

proc makeRotationMatrix*(v: Vector[3]): Matrix[4,4] =
    let xRotMatrix = [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, cos(v[0]), sin(v[0]), 0.0],
        [0.0, -sin(v[0]), cos(v[0]), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]
    let yRotMatrix = [
        [cos(v[1]), 0.0, sin(v[1]), 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [-sin(v[1]), 0.0, cos(v[1]), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]
    let zRotMatrix = [
        [cos(v[2]), -sin(v[2]), 0.0, 0.0],
        [sin(v[2]), cos(v[2]), 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]

    result = xRotMatrix ** yRotMatrix ** zRotMatrix

proc makeScaleMatrix*(v: Vector[3]): Matrix[4,4] =
    result = [
        [v[0], 0.0, 0.0, 0.0],
        [0.0, v[1], 0.0, 0.0],
        [0.0, 0.0, v[2], 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]

proc translateVector*(vector, translation: Vector[3]): Vector[3] = 
    result = dDown(makeTranslationMatrix(translation) ** dUp(vector))

proc rotateVector*(vector, rotation, origin: Vector[3]): Vector[3] = 
    result = dDown(makeTranslationMatrix(-1.0*origin) ** makeRotationMatrix(rotation) ** makeTranslationMatrix(origin) ** dUp(vector))

proc scaleVector*(vector, scale, origin: Vector[3]): Vector[3] =
    result = dDown(makeScaleMatrix(scale) ** dUp(vector))

# ------------------------------ classes an shit ----------------------------- #