class Dbclass:
    def __init__(self):
        import mysql.connector as connector

        # self.__dsn = { 'user' = 'root', 'password' = 'admin', 'host' = '127.0.0.1', 'database' = 'zeeslag' }

        self.__connection = connector.connect(user='bpgilly', password='root', host='169.254.10.1', database='Zeeslag')
        self.__cursor = self.__connection.cursor()

    def Connect(self):
        import mysql.connector as connector
        self.__connection = connector.connect(user='bpgilly', password='root', host='169.254.10.1', database='Zeeslag')
        self.__cursor = self.__connection.cursor()

    def GetMap(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM Users"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def GetUsers(self):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM Users"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def GetMapInfo(self, xCoord, yCoord):
        # Query zonder parameters
        sqlQuery = "SELECT Used FROM Map WHERE x = '{xParam}' AND y = '{yParam}'"
        sqlCommand = sqlQuery.format(xParam=xCoord, yParam=yCoord)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result[0]

    def GetMapInfoAI(self, xCoord, yCoord):
        # Query zonder parameters
        sqlQuery = "SELECT Used FROM Map WHERE x = '{xParam}' AND y = '{yParam}'"
        sqlCommand = sqlQuery.format(xParam=xCoord, yParam=yCoord)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        print(result)
        print(result[0])
        return result[0]

    def GetUserByName(self, name):
        # Query met parameters
        sqlQuery = "SELECT * FROM Users WHERE UserName = '{username}'"
        sqlCommand = sqlQuery.format(username=name)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchone()

        self.__cursor.close()

        return result

    def GetUserByID(self, ID):
        # Query met parameters
        sqlQuery = "SELECT * FROM Users WHERE UserId = '{UserID}'"
        sqlCommand = sqlQuery.format(UserID=ID)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchone()

        self.__cursor.close()

        return result

    def GetUserWonHistory(self, ID):
        # Query met parameters
        sqlQuery = "SELECT COUNT(*) FROM History WHERE Won = '{UserID}'"
        sqlCommand = sqlQuery.format(UserID=ID)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchone()

        self.__cursor.close()

        return result

    def GetUserLostHistory(self, ID):
        # Query met parameters
        sqlQuery = "SELECT COUNT(*) FROM History WHERE Lost = '{UserID}'"
        sqlCommand = sqlQuery.format(UserID=ID)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchone()

        self.__cursor.close()

        return result

    def InsertUser(self, username, password, email):
        # Query met parameters
        sqlQuery = "INSERT INTO Users (UserName, Pass, Email) VALUES ('{param1}','{param2}','{param3}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=username, param2=password, param3=email)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()

        sqlQuery = "INSERT INTO Settings (Blinking, Sound, Bigmap, HardMode) VALUES ('{param1}','{param2}','{param3}','{param4}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=True, param2=True, param3=True, param4=True)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()

        self.__cursor.close()

    def ClearMap(self):
        # Query met parameters
        sqlQuery = "UPDATE Map SET Used = 0"

        self.__cursor.execute(sqlQuery)
        self.__connection.commit()
        self.__cursor.close()

    def ClearMapAI(self):
        # Query met parameters
        sqlQuery = "UPDATE MapAI SET Used = 0"

        self.__cursor.execute(sqlQuery)
        self.__connection.commit()
        self.__cursor.close()

    def SetBoatOnMap(self, xcoord, ycoord):
        # Query met parameters
        sqlQuery = "UPDATE Map SET Used = 1 WHERE x = '{Xc}' AND y = '{Yc}'"
        sqlCommand = sqlQuery.format(Xc = xcoord, Yc = ycoord)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def SetBoatOnMapAI(self, xcoord, ycoord):
        # Query met parameters
        sqlQuery = "UPDATE MapAI SET Used = 1 WHERE x = '{Xc}' AND y = '{Yc}'"
        sqlCommand = sqlQuery.format(Xc = xcoord, Yc = ycoord)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def SetHitOnMap(self, xcoord, ycoord):
        # Query met parameters
        sqlQuery = "UPDATE Map SET Used = 2 WHERE x = '{Xc}' AND y = '{Yc}'"
        sqlCommand = sqlQuery.format(Xc=xcoord, Yc=ycoord)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def SetHitOnMapAI(self, xcoord, ycoord):
        # Query met parameters
        sqlQuery = "UPDATE MapAI SET Used = 2 WHERE x = '{Xc}' AND y = '{Yc}'"
        sqlCommand = sqlQuery.format(Xc=xcoord, Yc=ycoord)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def SetMissOnMap(self, xcoord, ycoord):
        # Query met parameters
        sqlQuery = "UPDATE Map SET Used = 3 WHERE x = '{Xc}' AND y = '{Yc}'"
        sqlCommand = sqlQuery.format(Xc=xcoord, Yc=ycoord)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def SetWinInHistoryOnPlayerID(self, player1ID, player2ID):
        sqlQuery = "INSERT INTO History (Won, Lost) VALUES ('{param1}','{param2}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=player1ID, param2=player2ID)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()

        self.__cursor.close()

        # def getDataFromDatabaseMetVoorwaarde(self, voorwaarde):
        #     # Query met parameters
        #     sqlQuery = "SELECT * FROM tablename WHERE columnname = '{param1}'"
        #     # Combineren van de query en parameter
        #     sqlCommand = sqlQuery.format(param1=voorwaarde)
	#
    #     self.__cursor.execute(sqlCommand)
    #     result = self.__cursor.fetchall()
    #     self.__cursor.close()
    #     return result
	#
    # def setDataToDatabase(self, value1):
    #     # Query met parameters
    #     sqlQuery = "INSERT INTO tablename (columnname) VALUES ('{param1}')"
    #     # Combineren van de query en parameter
    #     sqlCommand = sqlQuery.format(param1=value1)
	#
    #     self.__cursor.execute(sqlCommand)
    #     self.__connection.commit()
    #     self.__cursor.close()
