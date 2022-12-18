import arraymancer
import std/math
import boxy, windy


# ---------------------------------- colors ---------------------------------- #

const white* = rgb(255,255,255)
const black* = rgb(0,0,0)
const red* = rgb(0,0,0)

# ----------------------------------- utils ---------------------------------- #

proc `>+` *(a, b: array[3,float]): array[3,float] =  # element-wise addition of 3d vectors
    result = [a[0]+b[0],a[1]+b[1],a[2]+b[2]]

proc `>-` *(a, b: array[3,float]): array[3,float] = # element-wise subtraction of 3d vectors
    result = [a[0]-b[0],a[1]-b[1],a[2]-b[2]]

proc `>*` *(a, b: array[3,float]): array[3,float] = # element-wise multiplication of 3d vectors
    result = [a[0]*b[0],a[1]*b[1],a[2]*b[2]]

proc `>/` *(a, b: array[3,float]): array[3,float] = # element-wise division of 3d vectors
    result = [a[0]/b[0],a[1]/b[1],a[2]/b[2]]

proc `**` *(a, b: array[4,array[4,float]]): array[4,array[4,float]] = # 4x4 matrix * 4x4 matrix
    for i in 0..3:
        for j in 0..3:
            result[i][j] = (a[i][0] * b[0][j]) + (a[i][1] * b[1][j]) + (a[i][2] * b[2][j]) + (a[i][3] * b[3][j])

proc `**` *(b: array[4,float], a: array[4,array[4,float]]): array[4,float] = # 4d vector * 4x4 matrix
    for i in 0..3:
            result[i] = (a[i][0] * b[0]) + (a[i][1] * b[1]) + (a[i][2] * b[2]) + (a[i][3] * b[3])

proc translationMatrix*(trn: array[3,float]): array[4,array[4,float]] =
    result = [[1.0,0.0,0.0,trn[0]],  
              [0.0,1.0,0.0,trn[1]],
              [0.0,0.0,1.0,trn[2]],
              [0.0,0.0,0.0,1.0]]

proc rotationMatrix*(rot: array[3,float]): array[4,array[4,float]] =
    var xRotMatrix = [[1.0,0.0,0.0,0.0],
                      [0.0,cos(rot[0]), sin(rot[0]),0.0],
                      [0.0,-sin(rot[0]), cos(rot[0]),0.0],
                      [0.0,0.0,0.0,1.0]]
    var yRotMatrix = [[cos(rot[1]),0.0,-sin(rot[1]),0.0],
                      [0.0,1.0,0.0,0.0],
                      [sin(rot[1]),0.0,cos(rot[1]),0.0],
                      [0.0,0.0,0.0,1.0]]
    var zRotMatrix = [[cos(rot[2]),sin(rot[2]),0.0,0.0],
                      [-sin(rot[2]),cos(rot[2]),0.0,0.0],
                      [0.0,0.0,1.0,0.0],
                      [0.0,0.0,0.0,1.0]]
    result = xRotMatrix ** yRotMatrix ** zRotMatrix

proc scaleMatrix*(scl: array[3,float]): array[4,array[4,float]] =
    result = [[scl[0],0.0,0.0,0.0],  
              [0.0,scl[1],0.0,0.0],
              [0.0,0.0,scl[2],0.0],
              [0.0,0.0,0.0,1.0]]

proc dDown*(x: array[4,float]): array[3,float] = #truncates 4d vector, returns 3d vector
    result = [x[0],x[1],x[2]]

proc dUp*(x: array[3,float]): array[4,float] = #adds 1.0 element to 3d vector, returns 4d vector
    result = [x[0],x[1],x[2],1.0]

proc r*(oldDegrees: float): float =
    result = oldDegrees * (PI / 180.0)

proc d*(oldRadians: float): float =
    result = oldRadians * (180.0 / PI)

proc translateVector*(vector, trn: array[3, float]): array[3,float] =
    result = vector >+ trn

proc rotateVector*(vector, rot, origin: array[3, float]): array[3,float] =
    result = dDown(dUp(vector>-origin) ** rotationMatrix(rot)) >+ origin
    
proc scaleVector*(vector, scl, origin: array[3, float]): array[3,float] =
    result = ((vector >- origin) >* scl) >+ origin

proc cross*(a,b: array[3,float]): array[3,float] =
    result = [a[1]*b[2] - a[2]*b[1], a[2]*b[1] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]

proc dot*(a, b: array[3,float]): float =
  for i in a.low..a.high:
    result += a[i] * b[i]

proc magnitude*(v: array[3,float]): float =
    result = sqrt(v[0]^2 + v[1]^2 + v[2]^2)

proc triangleNormal*(v0,v1,v2: array[3,float]): array[3,float] =
    let unNormalizedNormal = cross((v0>-v1),(v1>-v2))
    let m = magnitude(unNormalizedNormal)
    result = unNormalizedNormal >/ [m,m,m]

# ------------------------------- MeshObject class ------------------------------- #
type
    MeshObject* = object
        pos*: array[3, float]
        rot*: array[3, float]
        rotDeg*: array[3, float] # not used for calculations, only for readouts
        scl*: array[3, float]
        objSpaceVertexTable*: seq[array[3, float]]
        wldSpaceVertexTable*: seq[array[3, float]]
        triTable*: seq[array[3, int]]

proc updateWldSpaceVertexTable*(this: var MeshObject) =
    for v in 0..(len(this.wldSpaceVertexTable)-1):
        this.wldSpaceVertexTable[v] = dDown(dUp(this.objSpaceVertexTable[v]) ** (translationMatrix(this.pos) ** (rotationMatrix(this.rot) ** scaleMatrix(this.scl))))

proc initMeshObject*(p = [0.0,0.0,0.0], r = [0.0,0.0,0.0], s = [1.0,1.0,1.0], osvt: seq[array[3, float]], tt: seq[array[3, int]]): MeshObject =
    result = MeshObject(pos: p, rot: r, rotDeg : r, scl: s, objSpaceVertexTable: osvt, wldSpaceVertexTable: osvt, triTable: tt) 
    for i in 0 .. 2:
        result.rotDeg[i] = d(result.rot[i])
    result.updateWldSpaceVertexTable()

proc changePosition*(this: var MeshObject, posDifference: array[3, float]) =
    this.pos = this.pos >+ posDifference
    this.updateWldSpaceVertexTable()

proc changeRotation*(this: var MeshObject, rotDifference: array[3, float]) =
    this.rot = this.rot >+ rotDifference
    for i in 0 .. 2:
        this.rotDeg[i] = d(this.rot[i])
    this.updateWldSpaceVertexTable()

proc changeScale*(this: var MeshObject, sclDifference: array[3, float]) =
    this.scl = this.scl >+ sclDifference
    this.updateWldSpaceVertexTable()

proc setPosition*(this: var MeshObject, newPos: array[3, float]) =
    this.pos = newPos
    this.updateWldSpaceVertexTable()

proc setRotation*(this: var MeshObject, newRot: array[3, float]) =
    this.rot = newRot
    for i in 0 .. 2:
        this.rotDeg[i] = d(this.rot[i])
    this.updateWldSpaceVertexTable()

proc setScale*(this: var MeshObject, newScl: array[3, float]) =
    this.scl = newScl
    this.updateWldSpaceVertexTable()

proc setGeometry*(this: var MeshObject, newObjVertexTable: seq[array[3, float]], newTriTable: seq[array[3, int]]) =
    this.objSpaceVertexTable = newObjVertexTable
    this.wldSpaceVertexTable = newObjVertexTable
    this.triTable = newTriTable
    this.updateWldSpaceVertexTable()



# -------------------------------- Empty class ------------------------------- #
type
    Empty* = object
        pos*: array[3, float]
        rot*: array[3, float]
        rotDeg*: array[3, float] # not used for calculations, only for readouts
        scl*: array[3, float]

proc initEmpty*(p = [0.0,0.0,0.0], r = [0.0,0.0,0.0], s = [1.0,1.0,1.0]): Empty =
    result = Empty(pos: p, rot: r, rotDeg : r, scl: s) 
    for i in 0 .. 2:
        result.rotDeg[i] = d(result.rot[i])

proc changePosition*(this: var Empty, posDifference: array[3, float]) =
    this.pos = this.pos >+ posDifference

proc changeRotation*(this: var Empty, rotDifference: array[3, float]) =
    this.rot = this.rot >+ rotDifference
    for i in 0 .. 2:
        this.rotDeg[i] = d(this.rot[i])

proc changeScale*(this: var Empty, sclDifference: array[3, float]) =
    this.scl = this.scl >+ sclDifference

proc setPosition*(this: var Empty, newPos: array[3, float]) =
    this.pos = newPos

proc setRotation*(this: var Empty, newRot: array[3, float]) =
    this.rot = newRot
    for i in 0 .. 2:
        this.rotDeg[i] = d(this.rot[i])

proc setScale*(this: var Empty, newScl: array[3, float]) =
    this.scl = newScl

# ------------------------------- Camera class ------------------------------- #
type
    Camera* = object
        pos*: array[3, float]
        rot*: array[3, float]
        rotDeg*: array[3, float] # not used for calculations, only for readouts
        scl*: array[3, float]
        fov*: float
        sX*: float
        sY*: float
        nearZ*: float
        farZ*: float

proc initCamera*(p = [0.0,0.0,0.0], r = [0.0,0.0,0.0], s = [1.0,1.0,1.0], f = r(90), shiftX = 0.0, shiftY=0.0, nZ = 0.1, fZ = 5.0): Camera =
    result = Camera(pos: p, rot: r, rotDeg : r, scl: s, fov: f, sX: shiftX, sY: shiftY, nearz: nZ, farZ: fZ) 
    for i in 0 .. 2:
        result.rotDeg[i] = d(result.rot[i])

proc changePosition*(this: var Camera, posDifference: array[3, float]) =
    this.pos = this.pos >+ posDifference

proc changeRotation*(this: var Camera, rotDifference: array[3, float]) =
    this.rot = this.rot >+ rotDifference
    for i in 0 .. 2:
        this.rotDeg[i] = d(this.rot[i])

proc changeScale*(this: var Camera, sclDifference: array[3, float]) =
    this.scl = this.scl >+ sclDifference

proc setPosition*(this: var Camera, newPos: array[3, float]) =
    this.pos = newPos

proc setRotation*(this: var Camera, newRot: array[3, float]) =
    this.rot = newRot
    for i in 0 .. 2:
        this.rotDeg[i] = d(this.rot[i])

proc setScale*(this: var Camera, newScl: array[3, float]) =
    this.scl = newScl

proc setFOV*(this: var Camera, newFOV: float) =
    this.fov = newFOV

proc setViewShift*(this: var Camera, newShiftX: float, newShiftY: float) =
    this.sX = newShiftX
    this.sY = newShiftY

proc setZClipping*(this: var Camera, newNearZ: float, newFarZ: float) =
    this.nearZ = newNearZ
    this.farZ = newFarZ

# ------------------------------- Screen class ------------------------------- #
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

# -------------------------------- Scene class ------------------------------- #

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

# ---------------------------- Pipeline functions ---------------------------- #
proc cameraSpace*(vertex: array[3, float], camera: Camera): array[4,float] =
    result = dUp(vertex >- camera.pos) ** rotationMatrix(camera.rot)

proc clipSpace*(camSpaceVertex: array[4,float], camera: Camera, screen: Screen): array[4,float] =
    let projectionMatrix = [
        [(tan(camera.fov/2.0)), 0.0, 0.0, 0.0],
        [0.0, (-tan(camera.fov/2.0)*screen.aspectRatio), 0.0, 0.0],
        [0.0, 0.0, ((camera.nearZ+camera.farZ)/(camera.farZ-camera.nearZ)), 1.0],
        [0.0, 0.0, ((2.0*camera.nearZ*camera.farZ)/(camera.nearZ-camera.farZ)), 0.0]]

    echo projectionMatrix

    result = camSpaceVertex ** projectionMatrix

proc imageSpace*(clipSpaceVertex: array[4,float], camera: Camera): array[2,float] =
    result = [(clipSpaceVertex[0]/clipSpaceVertex[3]+camera.sX),(clipSpaceVertex[1]/clipSpaceVertex[3]+camera.sY)]

proc screenSpace*(imageSpaceVertex: array[2,float], screen: Screen): array[2,int] = 
    result = [int((imageSpaceVertex[0]+1)*(screen.width/2)),int((imageSpaceVertex[1]+1)*(screen.height/2))]

proc isInClipSpace*(clipSpaceV: array[4,float]): bool =
    result = ((-clipSpaceV[3] <= clipSpaceV[0] and clipSpaceV[0] <= clipSpaceV[3]) and -clipSpaceV[3] <= clipSpaceV[1] and clipSpaceV[1] <= clipSpaceV[3] and -clipSpaceV[3] <= clipSpaceV[2] and clipSpaceV[2] <= clipSpaceV[3])
