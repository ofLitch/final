from mysql.connector import Error


class userblockedDao:
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
    def createUserBlocked(self, id, id_blocker, id_blockade):
        """Insert a new service."""
        try:
            # Asegúrate de que la conexión esté funcionando
            cursor = self.connection.cursor()

            # Consulta SQL para insertar un nuevo servicio
            query = """
                INSERT INTO userblocked (id, id_blocker,id_blockade)
                VALUES (%s, %s, %s)
            """

            # Ejecutar la consulta con los parámetros
            cursor.execute(query, (id,int(id_blocker),int(id_blockade)))

            # Guardar los cambios
            self.connection.commit()

            print(f"blocked '{id}' inserted successfully.")

            # Cerrar el cursor
            cursor.close()

        except Error as e:
            # Capturar y mostrar el error si algo sale mal
            print(f"Error insetting blockade: {e}")

    def delete(self, id):
        """Delete a service by ID."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM usersblocked WHERE id = %s"
            cursor.execute(query, (id,))
            self.connection.commit()
            print(f"user blocked {id} deleted successfully.")
            cursor.close()
        except Error as e:
            print(f"Error deleting user blocked : {e}")

    def changeData(self, id, column, change):
        """Update a specific column for a user by ID."""
        try:
            cursor = self.connection.cursor()

            # Construimos la consulta con el nombre de la columna directamente
            query = f"UPDATE usersblocked SET {column} = %s WHERE id = %s;"

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
            query = "SELECT * FROM usersblocked WHERE id = %;"
            cursor.execute(query,id)
            user = cursor.fetchall()
            cursor.close()
            return user
        except Error as e:
            print(f"Error selecting users blocked")