import lib, objects  # butane stuff
import boxy, opengl, windy # boxy stuff

proc main() =

    echo """
 ____        _                   _   _ _              ___  __ 
|  _ \      | |                 | \ | (_)            / _ \/_ |
| |_) |_   _| |_ __ _ _ __   ___|  \| |_ _ __ ___   | | | || |
|  _ <| | | | __/ _` | '_ \ / _ \ . ` | | '_ ` _ \  | | | || |
| |_) | |_| | || (_| | | | |  __/ |\  | | | | | | | | |_| || |
|____/ \__,_|\__\__,_|_| |_|\___|_| \_|_|_| |_| |_|  \___(_)_|"""

    # initialize Boxy stuff
    let windowSize = ivec2(250, 255)
    let window = newWindow("ButaneNim", windowSize)
    makeContextCurrent(window)
    loadExtensions()
    let bxy = newBoxy()
    var frame: int = 0

    # initialize Butane stuff
    var scene = initScene()
    echo "initalized scene"
    var screen = initScreen(windowSize[0],windowSize[1])
    echo "initalized screen with dimensions ", windowSize[0], " x ", windowSize[1]
    var cam = initCamera()
    echo "initalized camera at ", cam.pos, " with rotation ", cam.rot, " and FOV ", d(cam.fov), "d"

    scene.addMeshObject(Cube.unsafeaddr)


    cam.setPosition([3.5, 9.5, 5.0])
    cam.setRotation([r(-114.0),0.0,r(160.0)])
    cam.setFOV(d(90.0))
    cam.setZClipping(0.1,20.0)




    proc draw() =

        # fun little color demo (keeps screen occupied temporarily)
        for row in 0..255:
            for column in 0..255:
                screen.drawPixel([column,row], rgb(uint8(row),uint8(column),uint8(frame)))
        
        for obj in scene.objectCollection:
            for tri in obj.triTable:
                let v0 = obj.wldSpaceVertexTable[tri[0]]
                let v1 = obj.wldSpaceVertexTable[tri[1]]
                let v2 = obj.wldSpaceVertexTable[tri[2]]











    # Called when it is time to draw a new frame.
    proc display() =
        bxy.addImage("screenpixels", screen.pixels)
        bxy.beginFrame(windowSize)
        bxy.drawImage("screenpixels", vec2(0,0))
        bxy.endFrame()
        window.swapBuffers()
        inc frame
        # screen.clear()

    while not window.closeRequested:
        draw()
        display()
        pollEvents()


main()