from models import db, connect_db, User, UserPreference, FavoritePet, MaybePet, FavoriteOrg, Comment

from app import app

db.drop_all()
db.create_all()
