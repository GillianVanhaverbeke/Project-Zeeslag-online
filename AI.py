import random

class AIPlayer():
    boats = [1, 1, 2]

    delay = 0.005

    HP = 0
    LengthMap = 3
    coords = [0, 0]

    def __init__(self):
        self.HP = 0

        for i in self.boats:
            self.HP += self.boats[i]

    def SetBoatsAI(self):
        from DbClass import Dbclass
        db = Dbclass()

        db.ClearMapAI()
        for boat in self.boats:
            self.SetBoatOnMap(boat)


    def SetBoatOnMap(self, boatLength):
        from DbClass import Dbclass
        db = Dbclass()
        coord = [random.randrange(0, 8), random.randrange(0, 8)]

        for l in range(boatLength):
            db.Connect()
            used = db.GetMapInfo(coord[0] + l, coord[1])

            if used == 0:
                db.Connect()
                db.SetBoatOnMapAI(coord[0] + l, coord[1])

    def ShootBoatAI(self):
        from DbClass import Dbclass
        db = Dbclass()

        coord = [random.randrange(0, 8), random.randrange(0, 8)]
        used = db.GetMapInfo(coord[0], coord[1])

        if used == 0:
            db.Connect()
            db.SetHitOnMapAI(coord[0], coord[1])
