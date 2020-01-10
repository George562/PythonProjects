from math import pi, sin, cos, pi, hypot
from random import randint
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, TransparencyAttrib, DirectionalLight, PointLight, VBase4, AmbientLight, TextNode, NodePath, Quat
from panda3d.physics import ActorNode, ForceNode, LinearVectorForce
from direct.showbase import DirectObject
from panda3d.ode import OdeWorld, OdeBody, OdeMass, OdeBallJoint

def getAcceleration(arr, now):
    a = [0, 0, 0]
    pos = arr[now].getPosition()
    for i in range(len(arr)):
        if i != now:
            pos1 = arr[i].getPosition()
            h = hypot(pos[0]-pos1[0], pos[1]-pos1[1])        
            a[0] += (pos[0]-pos1[0])/h
            a[1] += (pos[1]-pos1[1])/h
    return a 

def zapolnenie(world, n):
    for i in range(n):
        sphere = loader.loadModel("smiley.egg")
        sphere.reparentTo(render)
        r = randint(10, 25)
        sphere.setPos(sin(i*2*pi/n)*r, cos(i*2*pi/n)*r, 2)

        sphereBody = OdeBody(world.myWorld)
        sphereModel = OdeMass()
        sphereModel.setSphere(1, 2)
        sphereBody.setMass(sphereModel)
        sphereBody.setPosition(sin(i*2*pi/n)*r, cos(i*2*pi/n)*r, 2)
        world.spheres.append(sphereBody)
        world.objs.append(sphere)

    for i in range(n-1):
        sphereJoint = OdeBallJoint(world.myWorld)
        sphereJoint.attach(world.spheres[i], world.spheres[i+1])
        sphereJoint.setAnchor(world.spheres[i].getPosition())
        world.joints.append(sphereJoint)
    sphereJoint = OdeBallJoint(world.myWorld)
    sphereJoint.attach(world.spheres[-1], world.spheres[0])
    sphereJoint.setAnchor(world.spheres[-1].getPosition())
    world.joints.append(sphereJoint)

class KatushkaLovushkeraUWUControl(DirectObject.DirectObject):
    k = 500
    l = 10
    a = 1

    def __init__(self, world):
        self.world = world
        self.world.objs = []
        self.world.spheres = []
        self.world.joints = []

        self.world.myWorld = OdeWorld()

        zapolnenie(self.world, 10)

        self.world.deltaTimeAccumulator = 0.0
        self.world.stepSize = 1.0 / 90.0

        self.accept('g-up', self.up)
        self.accept('g', self.press)

        self.g_pressed = False
        self.world.taskMgr.doMethodLater(1.0, self.simulationTask, 'Physics Simulation')

    def simulationTask(self, task):
        self.world.deltaTimeAccumulator += globalClock.getDt()
        while self.world.deltaTimeAccumulator > self.world.stepSize:
            self.world.deltaTimeAccumulator -= self.world.stepSize
            self.world.myWorld.quickStep(self.world.stepSize)
        for i in range(len(self.world.spheres)):
            self.world.spheres[i].setForce(*getAcceleration(self.world.spheres, i))
            self.world.objs[i].setPosQuat(render, self.world.spheres[i].getPosition(), Quat(self.world.spheres[i].getQuaternion()))
        return task.cont

    def press(self):
        self.g_pressed = True

    def up(self):
        self.g_pressed = False

class CameraControls(DirectObject.DirectObject):
    delta_x = 0
    delta_y = 0
    delta_z = 0
    velocity = 0.75
    dangle = 75
    angleDegreesH = 0
    angleDegreesP = 0
    angleDegreesR = 0


    def __init__(self, a_world):
        self.world = a_world
        self.world.taskMgr.add(self.cameraStay, "CameraStay")

        ### vv Register keyboard event handlers
        # W
        self.accept('w-up', self.w_up_key)
        self.accept('w', self.press_w_key)
        # S
        self.accept('s-up', self.s_up_key)
        self.accept('s', self.press_s_key)
        # A
        self.accept('a-up', self.a_up_key)
        self.accept('a', self.press_a_key)
        # D
        self.accept('d-up', self.d_up_key)
        self.accept('d', self.press_d_key)
        # Left
        self.accept('arrow_left-up', self.left_up_key)
        self.accept('arrow_left', self.press_arrow_left)
        # Right
        self.accept('arrow_right-up', self.right_up_key)
        self.accept('arrow_right', self.press_arrow_right)
        # Up
        self.accept('arrow_up-up', self.up_up_key)
        self.accept('arrow_up', self.press_arrow_up)
        # Down
        self.accept('arrow_down-up', self.down_up_key)
        self.accept('arrow_down', self.press_arrow_down)
        # Q
        self.accept('q-up', self.q_up_key)
        self.accept('q', self.press_q_key)
        # E
        self.accept('e-up', self.e_up_key)
        self.accept('e', self.press_e_key)
        # R
        self.accept('r-up', self.r_up_key)
        self.accept('r', self.press_r_key)
        # F
        self.accept('f-up', self.f_up_key)
        self.accept('f', self.press_f_key)

    def press_arrow_left(self):
        self.world.taskMgr.add(self.cameraTurnLeft, 'CameraTurnLeft')

    def press_arrow_right(self):
        self.world.taskMgr.add(self.cameraTurnRight, 'CameraTurnRight')

    def press_arrow_up(self):
        self.world.taskMgr.add(self.cameraTurnUp, 'CameraTurnUp')

    def press_arrow_down(self):
        self.world.taskMgr.add(self.cameraTurnDown, 'CameraTurnDown')

    def press_w_key(self):
        self.world.taskMgr.add(self.cameraMoveUp, "CameraMoveUp")

    def press_s_key(self):
        self.world.taskMgr.add(self.cameraMoveDown, "CameraMoveDown")

    def press_a_key(self):
        self.world.taskMgr.add(self.cameraMoveLeft, "CameraMoveLeft")

    def press_d_key(self):
        self.world.taskMgr.add(self.cameraMoveRight, "CameraMoveRight")

    def press_r_key(self):
        self.world.taskMgr.add(self.cameraMoveTop, "CameraMoveTop")

    def press_f_key(self):
        self.world.taskMgr.add(self.cameraMoveBottom, "CameraMoveBottom")

    def press_q_key(self):
        self.world.taskMgr.add(self.cameraTurnQ, "CameraTurnQ")

    def press_e_key(self):
        self.world.taskMgr.add(self.cameraTurnE, "CameraTurnE")

    def w_up_key(self):
        self.world.taskMgr.remove("CameraMoveUp")

    def s_up_key(self):
        self.world.taskMgr.remove("CameraMoveDown")

    def a_up_key(self):
        self.world.taskMgr.remove("CameraMoveLeft")

    def d_up_key(self):
        self.world.taskMgr.remove("CameraMoveRight")

    def r_up_key(self):
        self.world.taskMgr.remove("CameraMoveTop")

    def f_up_key(self):
        self.world.taskMgr.remove("CameraMoveBottom")

    def left_up_key(self):
        self.world.taskMgr.remove("CameraTurnLeft")

    def right_up_key(self):
        self.world.taskMgr.remove("CameraTurnRight")

    def up_up_key(self):
        self.world.taskMgr.remove("CameraTurnUp")

    def down_up_key(self):
        self.world.taskMgr.remove("CameraTurnDown")

    def q_up_key(self):
        self.world.taskMgr.remove("CameraTurnQ")

    def e_up_key(self):
        self.world.taskMgr.remove("CameraTurnE")

    def cameraStay(self, task):
        self.world.camera.setX(self.world.camera.getX() - self.delta_x)
        self.world.camera.setY(self.world.camera.getY() - self.delta_y)
        self.world.camera.setZ(self.world.camera.getZ() - self.delta_z)
        self.world.camera.setH(self.angleDegreesH)
        self.world.camera.setP(self.angleDegreesP)
        self.world.camera.setR(self.angleDegreesR)
        return Task.cont

    def cameraTurnLeft(self, task):
        self.angleDegreesH += self.dangle * (pi / 180.0)
        return Task.cont

    def cameraTurnRight(self, task):
        self.angleDegreesH -= self.dangle * (pi / 180.0)
        return Task.cont

    def cameraTurnUp(self, task):
        self.angleDegreesP += self.dangle * (pi / 180.0)
        return Task.cont

    def cameraTurnDown(self, task):
        self.angleDegreesP -= self.dangle * (pi / 180.0)
        return Task.cont

    def cameraTurnQ(self, task):
        self.angleDegreesR += self.dangle * (pi / 180.0)
        return Task.cont

    def cameraTurnE(self, task):
        self.angleDegreesR -= self.dangle * (pi / 180.0)
        return Task.cont

    def cameraMoveUp(self, task):
        self.delta_y += -cos(self.angleDegreesH * (pi / 180.0))*self.velocity*cos(self.angleDegreesR * (pi / 180.0))
        self.delta_x += sin(self.angleDegreesH * (pi / 180.0))*self.velocity*cos(self.angleDegreesR * (pi / 180.0))
        self.delta_z += -sin(self.angleDegreesP * (pi / 180.0))*self.velocity
        return Task.cont

    def cameraMoveDown(self, task):
        self.delta_y += cos(self.angleDegreesH * (pi / 180.0))*self.velocity*cos(self.angleDegreesR * (pi / 180.0))
        self.delta_x += -sin(self.angleDegreesH * (pi / 180.0))*self.velocity*cos(self.angleDegreesR * (pi / 180.0))
        self.delta_z += sin(self.angleDegreesP * (pi / 180.0))
        return Task.cont

    def cameraMoveLeft(self, task):
        self.delta_y += sin(self.angleDegreesH * (pi / 180.0))*self.velocity*cos(self.angleDegreesR * (pi / 180.0))
        self.delta_x += cos(self.angleDegreesH * (pi / 180.0))*self.velocity*cos(self.angleDegreesR * (pi / 180.0))
        return Task.cont

    def cameraMoveRight(self, task):
        self.delta_y += -sin(self.angleDegreesH * (pi / 180.0))*self.velocity*cos(self.angleDegreesR * (pi / 180.0))
        self.delta_x += -cos(self.angleDegreesH * (pi / 180.0))*self.velocity*cos(self.angleDegreesR * (pi / 180.0))
        return Task.cont

    def cameraMoveTop(self, task):
        self.delta_z -= self.velocity
        return Task.cont

    def cameraMoveBottom(self, task):
        self.delta_z += self.velocity
        return Task.cont

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        ### vv Disable the camera trackball controls.
        
        ### vv Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        ### vv Reparent the model to render.
        self.scene.reparentTo(self.render)
        ### vv Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, -5)

        self.katushka = KatushkaLovushkeraUWUControl(self)

        self.alight = AmbientLight('alight')
        self.alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        self.alnp = self.render.attachNewNode(self.alight)
        self.render.setLight(self.alnp)

        ### vv Create an object responsible for all camera moves
        camera_controls = CameraControls(self)
        
        self.a_text = TextNode('my node')
        self.a_text.setText("Every day I'm honestly trying to get better in some way.")
        self.a_text_node_path = self.render.attachNewNode(self.a_text)        

    ### vv Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

app = MyApp()
app.run()