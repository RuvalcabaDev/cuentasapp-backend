import hashlib
import datetime
from dotenv import load_dotenv
from peewee import MySQLDatabase, Model, CharField, DateTimeField, ForeignKeyField, TextField, IntegerField
from .Connections import ConnectionMySQL

load_dotenv()
db_connect = ConnectionMySQL()
SEP_RULES = " --- "


class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db_connect
        table_name = 'users'

    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()

    @classmethod
    def authenticate(cls, username, password):
        query = 'SELECT * FROM users WHERE username = %s;'
        print("Intentando acceder")
        db_connect.mysql_connect()
        db_connect.cursor.execute(query, (username))
        user = db_connect.cursor.fetchone()
        db_connect.connection.commit()
        print("Usuario existe:", user, sep=SEP_RULES)
        db_connect.mysql_close()
        if user and user[2] == User.create_password(password):
            return user

    def __str__(self):
        return self.username


class Movie(Model):
    title = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db_connect
        table_name = 'movies'


class UserReview(Model):
    user = ForeignKeyField(User, backref='reviews')
    movie = ForeignKeyField(Movie)
    review = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db_connect
        table_name = 'user_reviews'

    def __str__(self):
        return f'{self.user.username} - #{self.movie.title}'
