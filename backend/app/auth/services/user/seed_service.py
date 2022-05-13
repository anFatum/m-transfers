from backend.app.auth.models.user import User, UserRoles
from backend.app import Location
from mongoengine.errors import NotUniqueError
from flask import Flask


def seed_db(app: Flask):
    if not app.config["SEED_ADMIN"]:
        return
    user_location = Location.objects.first().id if app.config["DEBUG"] \
        else app.config["ADMIN_LOCATION"]
    try:
        admin_user = User(
            email=app.config["ADMIN_EMAIL"],
            roles=UserRoles.values(),
            plant_id=str(user_location)
        )
        admin_user.save()
    except NotUniqueError:
        admin_user = User.objects.get(email=app.config["ADMIN_EMAIL"])
        admin_user.roles = UserRoles.values()
        admin_user.plant_id = str(user_location)
        admin_user.save()
