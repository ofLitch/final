from mysql.connector import Error


class groupDao:
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

    def createGroup(self, idG, nameG):
        """Insert a new service."""
        try:

            cursor = self.connection.cursor()

            query = """
                INSERT INTO groupys (id, nameG, timeCreation)
                VALUES (%s, %s, NOW())
            """
            cursor.execute(query, (idG, nameG))

            # Guardar los cambios
            self.connection.commit()

            print(f"Group '{nameG}' inserted successfully with id: {idG}.")

            # Cerrar el cursor
            cursor.close()

        except Error as e:
            # Capturar y mostrar el error si algo sale mal
            print(f"Error inserting group no pOosIBLE: {e}")

    def delete(self, idG):
        """Delete a service by ID."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM groupys WHERE id = %s"
            cursor.execute(query, (idG,))
            self.connection.commit()
            print(f"group {idG} deleted successfully.")
            cursor.close()
        except Error as e:
            print(f"Error deleting group: {e}")

    def changeData(self, idG, column, change):
        """Update a specific column for a user by ID."""
        try:
            cursor = self.connection.cursor()

            # Corregir la consulta SQL
            query = f"UPDATE groupys SET {column} = %s WHERE id = %s;"

            # Ejecutamos la consulta con los valores de cambio e id
            cursor.execute(query, (change, idG))
            self.connection.commit()  # Confirma los cambios en la base de datos
            cursor.close()
            print("Change successful")
        except Error as e:
            print(f"Error doing change: {e}")
            return None

    def read(self, id):
        """Select all services for all users."""
        try:
            cursor = self.connection.cursor()
            query = "SELECT grupo FROM group WHERE id = %;"
            cursor.execute(query,id)
            group = cursor.fetchall()
            cursor.close()
            return group
        except Error as e:
            print(f"Error selecting groups")