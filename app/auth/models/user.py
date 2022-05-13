from http import HTTPStatus
from typing import Iterable, List

from werkzeug.exceptions import abort
from sqlalchemy.exc import DatabaseError, IntegrityError
from app import db
from app.core.utils.abc import EnumWithValues
from app.core.models.mixins import SaveableModelMixin, JsonableMixin
from app.banking.models.account import Account


class UserRoles(EnumWithValues):
    ADMIN = "admin"
    APP_USER = "app_user"


class User(SaveableModelMixin, JsonableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False)
    roles = db.Column(db.String(128), nullable=False)
    pw_hash = db.Column(db.String(128), nullable=False)
    accounts = db.relationship(Account, back_populates="owner")

    def to_json(self):
        jsonable = super().to_json()
        return {
            **jsonable,
            "roles": self.iter_roles
        }

    @property
    def iter_roles(self):
        return [role for role in self.roles.split(";")]

    def __get_missing_roles(self, roles: Iterable[str]) -> List[str]:
        """
        Method returns all missing user roles
        :param roles: roles user need to have
        :type roles: Iterable[str]
        :return: missing user roles
        :rtype: List[str]
        """
        missing_roles = [
            role_name
            for role_name in roles
            if role_name not in self.iter_roles and role_name
        ]
        return missing_roles

    def __check_all_permissions(self, roles: Iterable[str]) -> bool:
        """
        Method checks if user has all permissions
        based on groups user is in.
        :param roles: list of permissions we are checking
        :type roles: Iterable
        :return: if user have all permissions we passed
        :rtype: bool
        """
        missing_roles = self.__get_missing_roles(roles)
        return not missing_roles

    def __check_any_permissions(self, roles: Iterable[str]) -> bool:
        """
        Method checks if user has any of the permissions
        based on groups user is in
        :param roles: list of permissions we are checking
        :type roles: Iterable
        :return: if user have all permissions we passed
        :rtype: bool
        """
        missing_roles = self.__get_missing_roles(roles)
        return len(missing_roles) > 0

    def check_permissions(self, roles: Iterable[str], how: str = 'all') -> bool:
        """
        Method checks if user has any of the permissions
        based on groups user is in
        :param how: How permissions should be checked
                    all - for all groups
                    any - for at least one
        :type how: str (on of the ["all", "any"]
        :param roles: list of permissions we are checking
        :type roles: Iterable
        :return: if user have all permissions we passed
        :rtype: bool
        """
        if UserRoles.ADMIN in self.iter_roles:
            return True
        if how == 'all':
            return self.__check_all_permissions(roles)
        elif how == 'any':
            return self.__check_any_permissions(roles)
        else:
            raise AttributeError("Any or all are allowed only")

    def check_permissions_or_401(self,
                                 roles: Iterable[str],
                                 how: str = 'all',
                                 message: str = "You have not enough permissions") -> None:
        """
        Checks if user has all permissions passed as parameter.
        Raises 401 Unauthorized if doesn't
        :param how: How permissions should be checked
                    all - for all groups
                    any - for at least one
        :type how: str (on of the ["all", "any"]
        :param message: message to pass in 401 response
        (default "You have no enough permissions")
        :type message: str
        :param roles: list of permissions we are checking
        :type roles: Iterable
        :return: None
        """
        if not self.check_permissions(roles, how):
            abort(HTTPStatus.UNAUTHORIZED, message)

    def has_invalid_roles(self):
        invalid_roles = [role for role in self.iter_roles
                         if role not in UserRoles.values()]
        return len(invalid_roles)

    def save(self):
        try:
            return super().save()
        except DatabaseError as e:
            if isinstance(e, IntegrityError):
                return {"err": "User with this email exists!"}
            return {"err": e.detail}
