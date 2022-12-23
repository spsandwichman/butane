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
type
    MeshObject* = object
        pos*: Vector[3]
        rot*: Vector[3]
        scl*: Vector[3]
        objSpaceVertexTable*: seq[Vector[3]]
        wldSpaceVertexTable*: seq[Vector[3]]
        triTable*: seq[array[3,int]]

proc updateWldSpaceVertexTable*(this: var MeshObject) =
    for v in 0..(len(this.wldSpaceVertexTable)-1):
        this.wldSpaceVertexTable[v] = dDown(makeTranslationMatrix(this.pos) ** makeRotationMatrix(this.rot) ** makeScaleMatrix(this.scl) ** dUp(this.objSpaceVertexTable[v]))

proc initMeshObject*(p = [0.0,0.0,0.0], r = [0.0,0.0,0.0], s = [1.0,1.0,1.0], osvt: seq[Vector[3]], tt: seq[array[3, int]]): MeshObject =
     result = MeshObject(pos: p, rot: r, scl: s, objSpaceVertexTable: osvt, wldSpaceVertexTable: osvt, triTable: tt)
     result.updateWldSpaceVertexTable()

proc changePosition*(this: var MeshObject, posDifference: Vector[3]) =
    this.pos = this.pos + posDifference
    this.updateWldSpaceVertexTable()

proc changeRotation*(this: var MeshObject, rotDifference: Vector[3]) =
    this.rot = this.pos + rotDifference
    this.updateWldSpaceVertexTable()

proc changeScale*(this: var MeshObject, sclDifference: Vector[3]) =
    this.scl = this.pos + sclDifference
    this.updateWldSpaceVertexTable()

proc setPosition*(this: var MeshObject, newPos: Vector[3]) =
    this.pos = newPos
    this.updateWldSpaceVertexTable()

proc setRotation*(this: var MeshObject, newRot: Vector[3]) =
    this.rot = newRot
    this.updateWldSpaceVertexTable()

proc setScale*(this: var MeshObject, newScl: Vector[3]) =
    this.scl = newScl
    this.updateWldSpaceVertexTable()

proc setGeometry*(this: var MeshObject, newObjSpaceVertexTable: seq[Vector[3]], newTriTable: seq[array[3,int]]) =
    this.objSpaceVertexTable = newObjSpaceVertexTable
    this.wldSpaceVertexTable = newObjSpaceVertexTable
    this.triTable = newTriTable
    this.updateWldSpaceVertexTable()


# ADD EMPTY CLASS HERE LATER - i cant be fucked rn

type
    Camera* = object
        pos*: Vector[3]
        rot*: Vector[3]
        scl*: Vector[3]
        fov*: float
        shiftX: float
        shiftY: float
        nearZ: float
        farZ: float

proc initCamera*(p = [0.0,0.0,0.0], r = [0.0,0.0,0.0], s = [1.0,1.0,1.0], f = rad(90.0), sX = 0.0, sY=0.0, nZ = 0.1, fZ = 5.0): Camera =
    result = Camera(pos: p, rot: r, scl: s, fov: f, shiftX: sX, shiftY: sY, nearZ: nZ, farZ: fZ) 

proc changePosition*(this: var Camera, posDifference: Vector[3]) =
    this.pos = this.pos + posDifference

proc changeRotation*(this: var Camera, rotDifference: Vector[3]) =
    this.rot = this.pos + rotDifference

proc changeScale*(this: var Camera, sclDifference: Vector[3]) =
    this.scl = this.pos + sclDifference

proc setPosition*(this: var Camera, newPos: Vector[3]) =
    this.pos = newPos

proc setRotation*(this: var Camera, newRot: Vector[3]) =
    this.rot = newRot

proc setScale*(this: var Camera, newScl: Vector[3]) =
    this.scl = newScl

proc setFOV*(this: var Camera, newFOV: float) = 
    this.fov = newFOV

proc setViewShift*(this: var Camera, newShiftX, newShiftY: float) =
    this.shiftX = newShiftX
    this.shiftY = newShiftY

proc setZClipping*(this: var Camera, newNearZ, newFarZ: float) =
    this.nearZ = newNearZ
    this.farZ = newFarZ




type
    Screen* = object
        width*: int
        height*: int
        aspectRatio*: float
        pixels*: Image

proc initScreen*(w,h: int): Screen =
    result = Screen(width: w, height: h, aspectRatio: w/h)
    result.pixels = newImage(w, h)

proc drawPixel*(this: var Screen, point2d: array[2, int], color: ColorRGB) =
    let x = point2D[0]
    let y = point2D[1]
    if x < this.width and y < this.height and x >= 0 and y >= 0:
        this.pixels[x,y] = color

proc drawLine*(this: var Screen, point0, point1: array[2,int], color: ColorRGB) =
    var x0 = point0[0]
    var y0 = point0[1]
    let x1 = point1[0]
    let y1 = point1[1]
    let dx = abs(x1-x0)
    let sx = (if (x0 < x1): 1 else: -1)
    let dy = -abs(y1-y0)
    let sy = (if (y0 < y1): 1 else: -1)
    var error = dx + dy

    while true:
        this.drawPixel([x0,y0], color)
        if (x0 == x1) and (y0 == y1):
            break
        var e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break
            error = error + dy
            x0 = x0 + sx
        if e2 <= dx:
            if y0 == y1:
                break
            error = error + dx
            y0 = y0 + sy

proc clear*(this: var Screen) = 
    this.pixels = newImage(this.width, this.height)



type
    Scene* = object
        objectCollection*: seq[ptr MeshObject]
        backgroundColor*: ColorRGB
        backfaceCulling*: bool

proc initScene*(bgColor = rgb(0, 0, 0), bfCulling = true): Scene =
    result = Scene(backgroundColor: bgColor, backfaceCulling: bfCulling)

proc addMeshObject*(this: var Scene, objReference: ptr MeshObject) = 
    this.objectCollection.add(objReference)

proc setBackground*(this: var Scene, newColor: ColorRGB) =
    this.backgroundColor = newColor

proc setBackfaceCulling*(this: var Scene, isOn: bool) =
    this.backfaceCulling = isOn


# ---------------------------- pipeline functions ---------------------------- #
proc toCameraSpace*(vertex: Vector[3], camera: Camera): Vector[4] = makeRotationMatrix(camera.rot) ** dUp(vertex-camera.pos)
