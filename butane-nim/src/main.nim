import lib, objects  # butane stuff
import boxy, opengl, windy # boxy stuff

proc main() =

    # initialize Boxy stuff
    let windowSize = ivec2(1000, 500)
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
    scene.setBackfaceCulling(true)

    cam.setPosition([3.5,  9.5, 5.0])
    cam.setRotation([r(-114.0),0.0,r(160.0)])
    cam.setFOV(r(90.0))
    cam.setZClipping(0.1,20.0)

    echo clipSpace([1.1,1.1,1.1,1.1], cam, screen)


    proc draw() =

        # for i in 0..255:
        #     for j in 0..225:
        #         screen.drawPixel([i+400,j], rgb(uint8(i),uint8(j),uint8(frame)))


        for obj in scene.objectCollection:
            for tri in obj.triTable:

                let v0 = obj.wldSpaceVertexTable[tri[0]]
                let v1 = obj.wldSpaceVertexTable[tri[1]]
                let v2 = obj.wldSpaceVertexTable[tri[2]]

                let normalVector = triangleNormal(v0,v1,v2)
                let averagePosition = [(v0[0]+v1[0]+v2[0])/3,(v0[1]+v1[1]+v2[1])/3,(v0[2]+v1[2]+v2[2])/3]
                let cameraToTriangleVector = averagePosition >- cam.pos

                if scene.backfaceCulling and (dot(normalVector, cameraToTriangleVector) >= 0):
                    continue
                
                let cameraSpaceV0 = cameraSpace(v0, cam)
                let cameraSpaceV1 = cameraSpace(v1, cam)
                let cameraSpaceV2 = cameraSpace(v2, cam)

                let clipSpaceV0 = clipSpace(cameraSpaceV0, cam, screen)
                let clipSpaceV1 = clipSpace(cameraSpaceV1, cam, screen)
                let clipSpaceV2 = clipSpace(cameraSpaceV2, cam, screen)

                #echo clipSpaceV0

                # if not (isInClipSpace(clipSpaceV0) and isInClipSpace(clipSpaceV1) and isInClipSpace(clipSpaceV2)):
                #     continue
                
                let imageSpaceV0 = imageSpace(clipSpaceV0, cam)
                let imageSpaceV1 = imageSpace(clipSpaceV1, cam)
                let imageSpaceV2 = imageSpace(clipSpaceV2, cam)

                let screenSpaceV0 = screenSpace(imageSpaceV0, screen)
                let screenSpaceV1 = screenSpace(imageSpaceV1, screen)
                let screenSpaceV2 = screenSpace(imageSpaceV2, screen)

                screen.drawLine(screenSpaceV0,screenSpaceV1,white)
                screen.drawLine(screenSpaceV1,screenSpaceV2,white)
                screen.drawLine(screenSpaceV2,screenSpaceV0,white)
    
        #Cube.changeRotation([0.0,0.0,0.01])
        #echo "cam pos: ", cam.pos,  " cam rot: ", cam.rotDeg

    # Called when it is time to draw a new frame.
    proc display() =
        bxy.addImage("screenpixels", screen.pixels)
        bxy.beginFrame(windowSize)
        bxy.drawImage("screenpixels", vec2(0,0))
        bxy.endFrame()
        window.swapBuffers()
        inc frame
        screen.clear()
        bxy.removeImage("screenpixels")

    while not window.closeRequested:
        draw()
        display()
        pollEvents()


main()