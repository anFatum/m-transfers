from flask_mongoengine import BaseQuerySet, DoesNotExist


class UserGroupQuerySet(BaseQuerySet):

    def get_by_name(self, group_name):
        """
        Finds user group by its name. If not found raises 404 Not Found
        Uses icontains -> if name contains name passed as parameter
        ignoring the case
        :param group_name: group name we need to find
        :type group_name: str
        :return: found UserGroup object
        :rtype: UserGroup
        """
        try:
            return self.get(name__icontains=group_name)
        except DoesNotExist:
            return None
