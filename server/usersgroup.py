from mysql.connector import Error


class usersgroupDao:
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
    def createUserGroup(self, id, id_group, id_user):
        """Insert a new service."""
        try:
            # Asegúrate de que la conexión esté funcionando
            cursor = self.connection.cursor()

            # Consulta SQL para insertar un nuevo servicio
            query = """
                INSERT INTO usersgroup (id, id_group,id_user)
                VALUES (%s, %s, %s)
            """

            # Ejecutar la consulta con los parámetros
            cursor.execute(query, (id,int(id_group),int(id_user)))

            # Guardar los cambios
            self.connection.commit()

            print(f"group '{id}' inserted successfully for users_group")

            # Cerrar el cursor
            cursor.close()

        except Error as e:
            # Capturar y mostrar el error si algo sale mal
            print(f"Error insetting usersgroup: {e}")

    def delete(self, id):
        """Delete a service by ID."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM usersgroup WHERE id = %s"
            cursor.execute(query, (id,))
            self.connection.commit()
            print(f"user_group {id} deleted successfully.")
            cursor.close()
        except Error as e:
            print(f"Error deleting user blocked : {e}")

    def changeData(self, id, column, change):
        """Update a specific column for a user by ID."""
        try:
            cursor = self.connection.cursor()

            # Construimos la consulta con el nombre de la columna directamente
            query = f"UPDATE usersgroup SET {column} = %s WHERE id = %s;"

            # Ejecutamos la consulta con los valores de cambio e id
            cursor.execute(query, (change, id))
            self.connection.commit()  # Confirma los cambios en la base de datos
            cursor.close()
            print(f"Change succesfull")
        except Error as e:
            print(f"Error doing change: {e}")
            return None

    def read(self,id):
        """Select all services for all users."""
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM usersgroup WHERE id = %;"
            cursor.execute(query,id)
            user = cursor.fetchall()
            cursor.close()
            return user
        except Error as e:
            print(f"Error selecting users group")