from models.user import User
from models import storage

users = storage.all(User)
print(users)
