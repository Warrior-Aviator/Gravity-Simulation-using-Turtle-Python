from turtle import *
fps = 0 ; fps_skip = 2
G = 20
w = Screen() ; w.tracer(0) ; w.bgcolor("black")
defining = True

def make_star_shape(STAR_NAME , BRIGHT_COLOR , DARK_COLOR) :
    t = Turtle() ; t.reset() ; t.ht() ; t.pu()
    t.fd(6)
    t.lt(90)
    
    t.begin_poly() ; t.circle(6 , 180) ; t.end_poly()
    BRIGHT_SIDE = t.get_poly()
    
    t.begin_poly() ; t.circle(6 , 180) ; t.end_poly()
    DARK_SIDE   = t.get_poly()

    STAR_SHAPE = Shape("compound")
    STAR_SHAPE.addcomponent( BRIGHT_SIDE , BRIGHT_COLOR )
    STAR_SHAPE.addcomponent( DARK_SIDE   , DARK_COLOR   )
    
    w.register_shape(STAR_NAME, STAR_SHAPE)


make_star_shape("planet","lightblue","darkblue")



















class GravSys(object):
    def __init__(self):
        self.planets = []
        self.t = 0
        self.dt = 0.01
    def init(self):
        for p in self.planets:
            p.init()
    def start(self):
        global fps
        while True :
            fps += 1
            self.t += self.dt
            for p in self.planets:
                p.step()
                if fps%fps_skip == 0 : w.update()

class Star(Turtle):
    def __init__(self, m, x, v, gravSys, shape):
        Turtle.__init__(self, shape=shape)
        self.pu()
        self.m = m
        self.setpos(x)
        self.v = v
        gravSys.planets.append(self)
        self.gravSys = gravSys
        self.resizemode("user")
        self.pd()
    def init(self):
        dt = self.gravSys.dt
        self.a = self.acc()
        self.v = self.v + 0.5*dt*self.a
    def acc(self):
        a = Vec2D(0,0)
        for planet in self.gravSys.planets:
            if planet != self:
                v = planet.pos()-self.pos()
                a += (G*planet.m/abs(v)**3)*v
        return a
    def step(self):
        dt = self.gravSys.dt
        self.setpos(self.pos() + dt*self.v)
        if self.gravSys.planets.index(self) != 0:
            self.setheading(self.towards(self.gravSys.planets[0]))
        self.a = self.acc()
        self.v = self.v + dt*self.a


def main():
    gs = GravSys()
    
    Sun = Star(1000000, Vec2D(0,0), Vec2D(0,-2.5), gs, "circle")
    Sun.color("gold")
    Sun.shapesize(2.4)
    Sun.pu() 

    make_star_shape("Mercury" , "maroon" , "brown" )
    Mercury = Star(1, Vec2D(70,0), Vec2D(0,295), gs, "Mercury")
    Mercury.pencolor("red")
    Mercury.shapesize(0.8)
    
    Earth = Star(12500, Vec2D(210,0), Vec2D(0,195), gs, "planet")
    Earth.pencolor("blue")
    Earth.shapesize(1)
    
    Moon = Star(5, Vec2D(220,0), Vec2D(0,295), gs, "planet")
    Moon.pencolor("white")
    Moon.shapesize(0.5)

    PLANETS = [ Mercury , Earth ]
    SATS    = [ Moon  ]

    for PLANET in PLANETS : PLANET.pd() #u()
    for SAT    in SATS    : SAT.pu()
    
    if not defining : w.tracer(1)
    gs.init()
    gs.start()

main()

