import psycopg2
#Class database for the easier connection
class Database:
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None
    #Method to connect to the database
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print("Cannot connect with the database", e)
    #Method to close connection
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            
            