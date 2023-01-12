"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    # initialize the app with the extension
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(15),
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Preference(db.Model):

    __tablename__ = 'user_preference'

    user_id =db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable = False
    )

    pet_type = db.Column(
        db.Text
    )

    breed = db.Column(
        db.Text
    )

    size = db.Column(
        db.Text
    )

    gender = db.Column(
        db.Text
    )

    age = db.Column(
        db.Text
    )

    good_with_children = db.Column(
        db.Boolean
    )

    house_trained = db.Column(
        db.Boolean
    )

    special_need = db.Column(
        db.Boolean
    )

    zipcode = db.Column(
        db.Integer
    )

class FavoritePet(db.Model):

    __tablename__ ="favorite_pets"

    user_id =db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable = False
    ) 

    pet_id = db.Column(
        db.Integer,
        nullable=False
    )

        
class MaybePet(db.Model):

    __tablename__ ="maybe_pets"

    user_id =db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False
    )    

    pet_id = db.Column(
        db.Integer,
        nullable=False
    )

class FavoriteOrg(db.Model):

    __tablename__ ="favorite_orgs"

    user_id =db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable = False
    )

    org_id = db.Column(
        db.Text,
        nullable=False
    )


class Comment(db.Model):

    __tablename__ ="comments"

    user_id =db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable= False
    )    

    org_id = db.Column(
        db.Text
    )

    pet_id = db.Column(
        db.Integer
    )

