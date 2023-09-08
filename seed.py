from models import db, connect_db, User, FavoritePet, FavoriteOrg, FavPetComment, OrgComment

from app import app

db.drop_all()
db.create_all()
