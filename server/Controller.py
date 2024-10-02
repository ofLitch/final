import socket
import json
from groupsss import groupDao
from user import UserDao
from userblocked import userblockedDao
from usersgroup import usersgroupDao
from friendships import friendshipsDao
import mysql.connector
from mysql.connector import Error
from View  import *


class Controller:
    def __init__(self,host , port):
        """Initialize with the DAO instances."""
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))

        print(f"UDP Server initialized and listening on {self.host}:{self.port}")
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                database="bbaplicacion",   ## como leer json
                user="root",
                password="root"
            )
            self.groupBD = groupDao(self.connection)
            self.userBD = UserDao(self.connection)
            self.userblockedBD = userblockedDao(self.connection)
            self.usergroupBD = usersgroupDao(self.connection)
            self.friendshipsBD = friendshipsDao(self.connection)

        except Error as e:
            print(f"Error connecting to database: {e}")

    def close_connection(self):
        """Close the database connections."""
        if self.connection.is_connected():

            self.groupBD.close_connection()
            self.userBD.close_connection()
            self.userblockedBD.close_connection()
            self.usergroupBD.close_connection()
            self.connection.close()

            print("MySQL connection is closed.")



# funciones usuario-----------------

    def add_user(self, id, nameU,number):
        """Add a new user to the database."""
        response = self.userBD.createUser(id, nameU,number)
        print(response)

    def delete_user(self, id):
        """Add a new user to the database."""
        response = self.userBD.delete(id)
        print(response)

    def change_data_user(self, id, column, change):
        response = self.userBD.changeData(id, column, change)
        print(response)

    def read_data_user(self,id):
        response = self.userBD.read(id)
        print(response)
        return response

    def read_all(self,id):
        response = self.userBD.readAll(id)
        print(response)
        return response

# funciones grupo------------------------

    def add_group(self, idG, nameG):
        response = self.groupBD.createGroup(idG, nameG)
        print(response)

    def delete_group(self, id):
        """Add a new user to the database."""
        response = self.groupBD.delete(id)
        print(response)

    def change_data_group(self, idG, column, change):
        response = self.groupBD.changeData(idG, column, change)
        print(response)

    def read_data_group(self,id):
        response = self.groupBD.read(id)
        print(response)

#funciones bloqueo de usuario-------------------

    def add_user_blocked(self, id, id_blocker, id_blockade):
        """Add a new service for a user."""
        response = self.userblockedBD.createUserBlocked(id, id_blocker,id_blockade)
        print(response)
    def delete_user_blocked(self,id):
        response = self.userblockedBD.delete(id)
        print(response)

    def change_data_user_blocked(self, id, column, change):
        response = self.userblockedBD.changeData(id, column, change)
        print(response)

    def read_data_user_blocked(self,id):
        response = self.userblockedBD.read(id)
        print(response)

# funciones de ingreso de usuarios en grupo-------------

    def add_user_in_group(self, id, id_group, id_user):
        """Find all services for a specific user."""
        response = self.usergroupBD.createUserGroup(id,id_group, id_user)
        print(response)

    def delete_user_in_group(self,id):
        response = self.usergroupBD.delete(id)
        print(response)

    def change_data_user_group(self, id, column, change):
        response = self.usergroupBD.createUserGroup(id, column, change)
        print(response)

    def read_data_user_group(self,id):
        response = self.usergroupBD.read(id)
        print(response)

# funciones ingreso amigos---------------------

    def add_user_frienship(self, id, id_user, id_friend):
        """Find all services for a specific user."""
        self.friendshipsBD.createFriendShip(id, id_user, id_friend)
        response = self.read_all(id_friend)
        return response

    def delete_friendship(self, id):
        response = self.friendshipsBD.delete(id)
        print(response)

    def change_friendship(self, id, column, change):
        response = self.friendshipsBD.changeData(id, column, change)
        print(response)

    def read_friendship(self,id):
        response = self.friendshipsBD.read(id)
        print(response)
#Funciones de busqueda----------------------------------

    def listen(self, buffer_size=2048):
        try:
            print("Waiting suggest...")
            while True:
                data, client_address = self.server_socket.recvfrom(buffer_size)
                decrypted_message = data.decode()
                return [decrypted_message, client_address]
        except Exception as e:
            print(f"Error while receiving message: {e}")

    def control(self):
        listenIn = self.listen()
        while True:
            # Parsear el mensaje JSON
            try:
                listenIn = self.listen()
                json_data = json.loads(listenIn[0])     # lectura de method
                method = json_data.get("method")
                if method == 'connection':
                    self.server_socket.sendto(jsonOK.encode('utf-8'), listenIn[1])
                
                if  method == "register":
                    self.funcRegister(listenIn)
                    
                if method == "login":
                    self.server_socket.sendto(json_munu.encode('utf-8'), listenIn[1])
                    listenID = self.listen()
                    json_data = json.loads(listenID[0])
                    method =  json_data.get("method")

                    
                messageID = json_data.get("id") # obtenion id para verificacion
                if method == 'getMenuFunc':
                    self.getMenuFunc(listenID)
                elif method == 'getMenuFuncGroup':
                    self.getMenuFuncGroup(listenID)
                elif method == 'getMenuFunc3Table':
                    self.getMenuFunc3Table(listenID)
                if method == 'deleteUser':
                    self.deleteUser(listenID, listenIn, messageID)
                elif method == 'updateUser':
                    self.updateUser(listenID, listenIn, messageID)
                elif method == 'messageUser':
                    self.messageUser(listenID, listenIn, messageID)
                elif method == 'readDataUser':
                    self.readDataUser(listenID, listenIn, messageID)
                elif method == 'createGroup':
                    self.createGroup(listenID, listenIn, messageID)
                elif method == 'updateGroup':
                    self.updateGroup(listenID, listenIn, messageID)
                elif method == 'deleteGroup':
                    self.deleteGroup(listenID, listenIn, messageID)
                elif method == 'readGroup':
                    self.readGroup(listenID, listenIn, messageID)
                elif method == 'deleteFriend':
                    self.deleteFriend(listenID, listenIn, messageID)
                elif method == 'updateFriend':
                    self.updateFriend(listenID, listenIn, messageID)
                elif method == 'createFriend':
                    self.createFriend(listenID, listenIn, messageID)
                elif method == 'readFriend':
                    self.readFriend(listenID, listenIn, messageID)
                elif method == 'usersInGroups':
                    self.usersInGroups(listenID, listenIn, messageID)
                elif method == 'updateUsersInGroups':
                    self.updateUsersInGroups(listenID, listenIn, messageID)
                elif method == 'insertUsersInGroups':
                    self.insertUsersInGroups(listenID, listenIn, messageID)
                elif method == 'readUsersInGroups':
                    self.readUsersInGroups(listenID, listenIn, messageID)
                elif method == 'deleteBlock':
                    self.deleteBlock(listenID, listenIn, messageID)
                elif method == 'updateBlock':
                    self.updateBlock(listenID, listenIn, messageID)
                elif method == 'createBlock':
                    self.createBlock(listenID, listenIn, messageID)
                elif method == 'readBlock':
                    self.readBlock(listenID, listenIn, messageID)
            except Error as e:
                print("not posible")
                self.close_connection()     

    def funcLogin(self, listenIn):
        listenOption = self.listen()
        json_data = json.loads(listenOption[0])
        
        messageID = json_data.get("id") # obtenion id para verificacion
        try:
            search = self.read_data_user(int(messageID)) # uso de read para realizar la busqueda
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenIn[1])
        except:
            print("don't find")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'),listenIn[1])
            
    def funcRegister(self, listenIn):
        self.server_socket.sendto(jsonOK.encode('utf-8'),listenIn[1])
        data_register = {
            "add the data": [
                "id",
                "name",
                "phone"
            ]
        }
        json_data_register = json.dumps(data_register)
        self.server_socket.sendto(json_data_register.encode('utf-8'),listenIn[1])
        listenDataR = self.listen()
        listenDataRMessages = json.loads(listenDataR[0])
        
        if listenDataRMessages.get("data", False) !=  False:
            id = listenDataRMessages['data'].get("id")
            name = listenDataRMessages['data'].get("name")
            number = listenDataRMessages['data'].get("phone")
            try:
                self.add_user(id,name,number)
                response = json.dumps({"id": id})
                self.server_socket.sendto(response.encode('utf-8'), listenIn[1])
            except:
                print("error add user")
                self.server_socket.sendto(jsonNoOK.encode('utf-8'),listenIn[1])

    def getMenuFunc (self, listenID):
        self.server_socket.sendto(json_munu_func.encode('utf-8'), listenID[1])
    def getMenuFuncGroup (self, listenID):
        self.server_socket.sendto(json_menu_funcGroup.encode('utf-8'), listenID[1])
    def getMenuFunc3Table (self, listenID):
        self.server_socket.sendto(json_munu_func3table.encode('utf-8'), listenID[1])
    def deleteUser (self, listenID, listenIn, messageID):
        try:
            self.delete_user(int(messageID))
            self.server_socket.sendto(jsonOK.encode('utf-8'),listenIn[1])
            print("1")
        except:
            print("error delete")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'),listenIn[1])
    def updateUser (self, listenID, listenIn, messageID):
        json_data_listen = json.loads(listenIn[0])
        id =  json_data_listen.get("id")
        
        json_munu_change = json.dumps(menu_change)
        self.server_socket.sendto(json_munu_change.encode('utf-8'), listenID[1]) # envia lista de opciones
        listenDataChange = self.listen()
        json_data_listen = json.loads(listenDataChange[0])
        option = json_data_listen.get("option", "nameU")
        if option == '1':
            column = "nameU"
        if option == '2':
            column = "number"

        self.server_socket.sendto(json_change.encode('utf-8'), listenID[1])

        listenChange = self.listen()
        listenChangeArrive = json.loads(listenChange[0])
        listenChangeArriveMessage = listenChangeArrive.get("option")
        listenChangeData = listenChangeArriveMessage
        
        try:
            self.change_data_user(id,column,listenChangeData)
            self.server_socket.sendto(jsonOK.encode('utf-8'),listenIn[1])
        except:
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenIn[1])
            print("error change")
    def messageUser(self, listenID, listenIn, messageID):
        # Primer envío al cliente para confirmar la IP
        json_informationClientB = json.dumps(informationClientB)
        self.server_socket.sendto(json_informationClientB.encode('utf-8'), listenID[1])
        listenMessages = self.listen()  # Escuchar el mensaje de vuelta
        json_dataMessage = json.loads(listenMessages[0])
        ip = json_dataMessage.get("IP")  # Obtener la IP

        # Segundo envío al cliente para confirmar el puerto
        json_informationClientB2 = json.dumps(informationClientB2)
        self.server_socket.sendto(json_informationClientB2.encode('utf-8'), listenID[1])
        listenMessages = self.listen()  # Escuchar el mensaje de vuelta
        json_dataMessage = json.loads(listenMessages[0])
        port = json_dataMessage.get("PORT")  # Obtener el puerto

        try:
            print("Waiting for messages...")
            while True:
                # Recibir datos del cliente
                data, client_address = self.server_socket.recvfrom(2046)
                print(data)
                # Reenviar los datos al cliente receptor (según IP y puerto obtenidos)
                self.server_socket.sendto(data, (ip, int(port)))

        except Exception as e:
            print(f"Error while receiving message: {e}")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenIn[1])

    def readDataUser (self, listenID, listenIn, messageID):
        try:
            json_data_listen = json.loads(listenIn[0])
            id =  json_data_listen.get("id")
            all_data_user = self.read_all(id)
            data_dict = {
                "id": str(all_data_user[0]),
                "name": str(all_data_user[1]),
                "phone": str(all_data_user[2]),
                "creation_count": str(all_data_user[3])
            }
            json_data_dict = json.dumps(data_dict)
            self.server_socket.sendto(json_data_dict.encode('utf-8'), listenIn[1])
        except:
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenIn[1])
            print("error read user")
    def createGroup (self, listenID, listenIn, messageID):
        json_dataGroup = json.dumps(dataGroup)
        self.server_socket.sendto(json_dataGroup.encode('utf-8'),listenID[1])
        listenDataGroup = self.listen()
        json_dataMessage = json.loads(listenDataGroup[0])
        idG = json_dataMessage.get("id")
        nameG = json_dataMessage.get("Name")
        try:
            self.add_group(int(idG),nameG)
            self.server_socket.sendto(jsonOK.encode('utf-8'),messageID)
        except:
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), messageID)
            print("error add group")
    def updateGroup (self, listenID, listenIn, messageID):
        menu_changeG = {
            "options to upload": "name",
        }
        json_changeG = json.dumps(menu_changeG)
        self.server_socket.sendto(json_changeG.encode('utf-8'), listenID[1])

        listenChange = self.listen()
        listenChangeDataMessage = json.loads(listenChange[0])
        listenChangeData = listenChangeDataMessage.get("name")
        try:
            self.change_data_group(int(messageID), "nameG", listenChangeData)
            self.server_socket.sendto(jsonOK.encode('utf-8'), messageID)
        except:
            print("error change data group")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'),listenID[1])
    def deleteGroup (self, listenID, listenIn, messageID):
        idGroupDelete = {
            "Data": "ID group"
        }
        json_idGroupDelete = json.dumps(idGroupDelete)
        self.server_socket.sendto(json_idGroupDelete.encode('utf-8'), listenID[1])

        listenDeleteGroup = self.listen()
        listenDeleteGroupMessage = json.loads(listenDeleteGroup[0])
        id_GroupDelete = listenDeleteGroupMessage.get("id")
        try:
            self.delete_group(int(id_GroupDelete))
            self.server_socket.sendto(jsonOK.encode('utf-8'), messageID)
        except:
            print("error delete group")
            self.server_socket.sendto (jsonNoOK.encode('utf-8'), listenID[1])
    def readGroup (self, listenID, listenIn, messageID):
        data_Group = {
            "id":"id group"
        }

        jsonData_group= json.dumps(data_Group)
        self.server_socket.sendto(jsonData_group, listenID[1])

        listenIDgroup = self.listen()
        listenIDgroupMessage = json.loads(listenIDgroup[0])
        id_group = listenIDgroupMessage.get("id")
        try:
            Data_Group = self.read_data_group(int(id_group))
            self.server_socket.sendto(jsonOK.encode('utf-8'), messageID)

            Data_Group_list = {
                "id": Data_Group[0],
                "name": Data_Group[1],
                " creation": Data_Group[2],
            }

            json_Data_Group_list = json.dumps(Data_Group_list)
            self.server_socket.sendto(json_Data_Group_list, listenID[1])
        except:
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), messageID)
            print("error read data group")
    def deleteFriend (self, listenID, listenIn, messageID):
        idFriendDelete = {
            "Data": "ID friendship"
        }
        json_idFriendDelete = json.dumps(idFriendDelete)
        self.server_socket.sendto(json_idFriendDelete.encode('utf-8'),listenID[1])

        listenDeleteFriendship = self.listen()
        listenDeleteFriendshipMessage = json.loads(listenDeleteFriendship[0])
        IdfriendshipDelete = listenDeleteFriendshipMessage.get("id")

        try:
            self.delete_friendship(int(IdfriendshipDelete))
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenIn[1])
        except:
            print("error delete friendship")
            self.server_socket.sendto (jsonNoOK.encode('utf-8'),listenIn[1])
    def updateFriend (self, listenID, listenIn, messageID):
        id_friendship = {
            "options to update":"id_friendship"
        }

        json_id_friendship = json.dumps(id_friendship)
        self.server_socket.sendto(json_id_friendship.encode('utf-8'),listenID[1])
        listenIDfriendShip = self.listen()
        listenIDfriendShipMessage = json.loads(listenIDfriendShip[0])
        idFriendship = listenIDfriendShipMessage.get("id")

        self.server_socket.sendto(json_change.encode('utf-8'), listenID[1])
        listenChange = self.listen()
        listenChangeMessage = json.loads(listenChange[0])
        change = listenChangeMessage.get("change")

        try:
            self.change_friendship(idFriendship,"id",change)
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenIn[1])
        except:
            print("error changefriendship")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenIn[1])
    def createFriend (self, listenID, listenIn, messageID):
        json_data_listen = json.loads(listenIn[0])
        id =  json_data_listen.get("id")
        data_relationship = {
            "add the data": [
                "id_relationship"
            ]
        }
        data_relationship2 = {
            "add the data": [
                "id_friend"
            ]
        }
        json_relationship = json.dumps(data_relationship)
        self.server_socket.sendto(json_relationship.encode('utf-8'),listenID[1])
        listenDataR = self.listen()
        listenDataRMessage = json.loads(listenDataR[0])
        id_relationship = listenDataRMessage.get("id_relationship")
        
        json_relationship2 = json.dumps(data_relationship2)
        self.server_socket.sendto(json_relationship2.encode('utf-8'),listenID[1])
        listenDataR2 = self.listen()
        listenDataRMessage2 = json.loads(listenDataR2[0])
        id_friend = listenDataRMessage2.get("id_friend")

        try:
            response = self.add_user_frienship(int(id_relationship.get("id_relationship")),int(id),int(id_friend.get("id_friend")))
            data_dict = {
                "id": str(response[0]),
                "name": str(response[1]),
                "phone": str(response[2]),
                "creation_count": str(response[3])
            }
            json_data_dict = json.dumps(data_dict)
            print(json_data_dict)
            self.server_socket.sendto(json_data_dict.encode('utf-8'), listenIn[1])
        except:
            print("error add_user_friendship")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenIn[1])
    def readFriend (self, listenID, listenIn, messageID):
        data_relationship = {
            "enter":"id_relationship"

        }
        json_data_relationship = json.dumps(data_relationship)
        self.server_socket.sendto(json_data_relationship.encode('utf-8'),listenID[1])
        listenDataR = self.listen()
        listenDataRMessage = json.loads(listenDataR[0])
        id = listenDataRMessage.get("id_relationship")
        try:
            datos = self.read_friendship(int(id))
            Data = {
                "id": datos[0],
                "id_user": datos[1],
                "id_friend": datos[2],
                "creation_group": datos[3],
            }
            jsonData = json.dumps(Data)
            self.server_socket.sendto(jsonData.encode('utf-8'), listenID[1])
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenIn[1])
        except:
            print("error read friendship")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenIn[1])
    def usersInGroups (self, listenID, listenIn, messageID):
        idUserGroupDelete = {
            "Data": "ID user in group"
        }
        json_idGroupDelete = json.dumps(idUserGroupDelete)
        self.server_socket.sendto(json_idGroupDelete.encode('utf-8'), listenID[1])

        listenDeleteGU = self.listen()
        listenDeleteGUMessage = json.loads(listenDeleteGU[0])
        IdGUDelete = listenDeleteGUMessage.get("id")

        try:
            self.delete_user_in_group(int(IdGUDelete))
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenID[1])
        except:
            print("error delete user in group")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenIn[1])
    def updateUsersInGroups (self, listenID, listenIn, messageID):
        id_UG = {
            "options to update":"id_user in group"
        }

        json_id_UG = json.dumps(id_UG)
        self.server_socket.sendto(json_id_UG.encode('utf-8'),listenID[1])
        listenIDUG = self.listen()
        listenIDUGMessage = json.loads(listenIDUG[0])
        idUG = listenIDUGMessage.get("id")

        self.server_socket.sendto(json_change.encode('utf-8'), listenID[1])
        listenChange = self.listen()
        listenChangeMessage = json.loads(listenChange[0])
        change = listenChangeMessage.get("change")
        try:
            self.change_data_user_group(idUG,"id",change)
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenID[1])
        except:
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenID[1])
            print("error change data user group")
    def insertUsersInGroups (self, listenID, listenIn, messageID):
        data_UG = {
            "add the data": [
                "id_user_group",
                "id_group"
            ]
        }
        json_UG = json.dumps(data_UG)
        self.server_socket.sendto(json_UG.encode('utf-8'),listenID[1])
        listenDataUG = self.listen()
        listenDataRMessage = json.loads(listenDataUG[0])
        id_group = listenDataRMessage.get("id_group")
        id_user_group = listenDataRMessage.get("id_user_group")
        try:
            self.add_user_in_group(int(id_user_group),int(id_group),int(messageID))
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenID[1])
        except:
            print("error add user in group")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'),listenID[1])
    def readUsersInGroups (self, listenID, listenIn, messageID):
        dataUG = {
            "enter":"id_user_group"

        }
        json_data_UG = json.dumps(dataUG)
        self.server_socket.sendto(json_data_UG.encode('utf-8'),listenID[1])
        listenDataR = self.listen()
        listenDataRMessage = json.loads(listenDataR[0])
        id = listenDataRMessage.get("id_user_group")

        try:
            datos = self.read_data_user_group(int(id))
            Data = {
                "id": datos[0],
                "id_group": datos[1],
                "id_user": datos[2],
            }
            jsonData = json.dumps(Data)
            self.server_socket.sendto(jsonData.encode('utf-8'), listenID[1])
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenID[1])

        except:
            print("error read data user group")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenID[1])
    def deleteBlock (self, listenID, listenIn, messageID):
        idBlockDelete = {
            "Data": "ID user_blocking"
        }
        json_idBDelete = json.dumps(idBlockDelete)
        self.server_socket.sendto(json_idBDelete.encode('utf-8'), listenID[1])

        listenDeleteB = self.listen()
        listenDeleteGUMessage = json.loads(listenDeleteB[0])
        IdGUDelete = listenDeleteGUMessage.get("id")

        try:
            self.delete_user_blocked(int(IdGUDelete))
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenID[1])
        except:
            print("error delete user blocked")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenIn[1])
    def updateBlock (self, listenID, listenIn, messageID):
        id_B = {
            "options to update": "id_user_blocked"
        }

        json_id_B = json.dumps(id_B)
        self.server_socket.sendto(json_id_B.encode('utf-8'), listenID[1])
        listenB = self.listen()
        listenBMessage = json.loads(listenB[0])
        idB = listenBMessage.get("id")

        self.server_socket.sendto(json_change.encode('utf-8'), listenID[1])
        listenChange = self.listen()
        listenChangeMessage = json.loads(listenChange[0])
        change = listenChangeMessage.get("change")
        try:
            self.change_data_user_blocked(idB, "id", change)
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenID[1])
        except:
            print("error change data user blocked")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenID[1])
    def createBlock (self, listenID, listenIn, messageID):
        data_B = {
            "add the data": [
                "id_user_blocked",
                "id_blockade"
            ]
        }
        json_B = json.dumps(data_B)
        self.server_socket.sendto(json_B.encode('utf-8'), listenID[1])
        listenDataB = self.listen()
        listenDataRMessage = json.loads(listenDataB[0])
        id_user_blocked = listenDataRMessage.get("id_user_blocked")
        id_blockade = listenDataRMessage.get("id_blockade")

        try:
            self.add_user_blocked(int(id_user_blocked), int(messageID), int(id_blockade))
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenID[1])
        except:
            print("error add user blocked")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenID[1])
    def readBlock (self, listenID, listenIn, messageID):
        dataB= {
            "enter": "id_user_blocked"

        }
        json_data_B = json.dumps(dataB)
        self.server_socket.sendto(json_data_B.encode('utf-8'), listenID[1])
        listenDataR = self.listen()
        listenDataRMessage = json.loads(listenDataR[0])
        id = listenDataRMessage.get("id_user_group")
        try:
            datos = self.read_data_user_blocked(int(id))
            Data = {
                "id_user_blockade": datos[0],
                "id_blocker": datos[1],
                "id_blockade": datos[2]
            }
            jsonData = json.dumps(Data)
            self.server_socket.sendto(jsonData.encode('utf-8'), listenID[1])
            self.server_socket.sendto(jsonOK.encode('utf-8'), listenID[1])
        except:
            print("error read data user blocked")
            self.server_socket.sendto(jsonNoOK.encode('utf-8'), listenID[1])
    
    
jsonOK = json.dumps(dataSend)
jsonNoOK = json.dumps(NoOK)
json_munu = json.dumps(menu_dict)
json_munu_func = json.dumps(menu_funcUser)
json_menu_funcGroup = json.dumps(menu_funcGroup)
json_munu_func3table =json.dumps(menu_func3table)
json_change = json.dumps(change)
    
    
if __name__ == "__main__":
    view = Controller("127.0.0.1", 12000)
    view.control()


