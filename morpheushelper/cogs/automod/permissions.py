from PyDrocsid.permission import BasePermission
from PyDrocsid.translations import translations


class Permission(BasePermission):
    manage_autokick = translations.permissions["manage_autokick"]
    manage_instantkick = translations.permissions["manage_instantkick"]