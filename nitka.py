from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, TransparencyAttrib, DirectionalLight, PointLight, VBase4, AmbientLight, TextNode
from direct.showbase import DirectObject

class BoxControl(DirectObject.DirectObject):
    def __init__(self, a_world):
        self.worl = a_world

        self.accept('space-up', self.turnoff)
        self.accept('space', self.turnon)

    def turnon(self):
        self.world.taskMgr.add(self.boxturnon, 'BoxTurnOn')

    def turnoff(self):
        self.world.taskMgr.add(self.boxturnoff, 'BoxTurnOff')

    def boxturnon(self, task):
        self.world.boxmodel.setH(self.worl.)

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

        ### vv Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk" : "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        ### vv Loop its animation.
        self.pandaActor.loop("walk")
        self.pandaActor.setTransparency(TransparencyAttrib.MAlpha)
        self.pandaActor.setColor(1, 0, 0, 0.5)

        ### Load and transform the box actor.
        self.boxModel = self.loader.loadModel("models/box")
        self.boxModel.reparentTo(self.render)
        self.boxModel.setPos(0, 0, 0)

        ### Load and transform the sphere actor.
        # self.sphereModel = self.loader.loadModel("models/misc/sphere")
        # self.sphereModel.reparentTo(self.render)
        # self.sphereModel.setPos(0, 0, 0)

        # self.plight = PointLight('plight')
        # self.plight.setColor(VBase4(1, 1, 1, 1))
        # self.plnp = self.render.attachNewNode(self.plight)
        # self.plnp.setPos(0, 0, 0)
        # self.render.setLight(self.plnp)
        # self.plight.setAttenuation((1, 0, 0.1))

        self.alight = AmbientLight('alight')
        self.alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        self.alnp = self.render.attachNewNode(self.alight)
        self.render.setLight(self.alnp)

        ### vv Create an object responsible for all camera moves
        camera_controls = CameraControls(self)
        
        self.a_text = TextNode('my node')
        self.a_text.setText("Every day I'm honestly trying to get better in some way.")
        self.a_text_node_path = self.render.attachNewNode(self.a_text)
        
        # Create the four lerp intervals needed for the panda to
        # walk back and forth
        pandaPosInterval1 = self.pandaActor.posInterval(13,
                                                        Point3(0, -10, 0),
                                                        startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13,
                                                        Point3(0, 10, 0),
                                                        startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(180, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(pandaPosInterval1,
                                  pandaHprInterval1,
                                  pandaPosInterval2,
                                  pandaHprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()
        

    ### vv Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


    
app = MyApp()
app.run()