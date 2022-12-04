import pymysql
import os


class ConnectionMySQL:
    cursor = None
    connection = None

    def mysql_connect(self):
        self.connection = pymysql.connect(
            host=os.getenv("HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            port=3306,
            db=os.getenv("DATABASE_NAME")
        )
        self.cursor = self.connection.cursor()
        print("¡Conexión establecida!")

    def mysql_close(self):
        print("¡Conexión cerrada!")
        self.connection.close()
