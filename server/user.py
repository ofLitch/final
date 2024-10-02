from mysql.connector import Error
import time


class UserDao:
    def __init__(self, connection):
        """Initialize the database connection."""
        try:
            # Load database config from JSON file
            # 3with open("config.json") as config_file:
            #    config = json.load(config_file)
            self.connection = connection
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def close_connection(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    ### CRUD Operations for service Table ###
    def createUser(self, id, nameU,number):
        """Insert a new service."""
        try:
            # Asegúrate de que la conexión esté funcionando
            cursor = self.connection.cursor()

            # Consulta SQL para insertar un nuevo servicio
            query = """
                INSERT INTO user (id, nameU,number, timeCreation)
                VALUES (%s, %s, %s,NOW())
            """
            # Ejecutar la consulta con los parámetros
            cursor.execute(query, (id, nameU,number))

            # Guardar los cambios
            self.connection.commit()

            print(f"User '{nameU}' inserted successfully for user {id}.")

            # Cerrar el cursor
            cursor.close()

        except Error as e:
            # Capturar y mostrar el error si algo sale mal
            print(f"Error inserting user: {e}")

    def delete(self, id):
        """Delete a service by ID."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM user WHERE id = %s"
            cursor.execute(query, (id,))
            self.connection.commit()
            print(f"user {id} deleted successfully.")
            cursor.close()
        except Error as e:
            print(f"Error deleting user: {e}")

    def changeData(self, id, column, change):
        """Update a specific column for a user by ID."""
        try:
            cursor = self.connection.cursor()

            # Construimos la consulta con el nombre de la columna directamente
            # Corregir la consulta SQL
            query = f"UPDATE user SET {column} = %s WHERE id = %s;"

            # Ejecutamos la consulta con los valores de cambio e id
            cursor.execute(query, (change, id))
            self.connection.commit()  # Confirma los cambios en la base de datos
            cursor.close()
            print("Change successful")
        except Error as e:
            print(f"Error doing change: {e}")
            return None

    def read(self, id):
        """Select a user by id."""
        try:
            cursor = self.connection.cursor()
            query = "SELECT id FROM user WHERE id = %s LIMIT 1;"
            cursor.execute(query, (id,))
            user = cursor.fetchone()  # Devuelve una tupla (id,)
            cursor.close()
            
            # Verificar si se encontró un usuario y retornar solo el id
            if user:
                return user[0]  # Devuelve el primer elemento de la tupla
            else:
                return None  # Si no se encuentra el usuario, devolver None
        except Error as e:
            print(f"Error selecting user: {e}")
            return None



    def readAll(self,id):
        """Select all services for all users."""
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM user WHERE id = %s LIMIT 1;"
            cursor.execute(query,(id,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Error as e:
            print(f"Error selecting user")