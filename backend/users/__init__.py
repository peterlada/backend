# -*- coding: utf-8 -*-
"""
    backend.users
    ~~~~~~~~~~~~~~

    backend users package
"""

from ..core import Service
from .models import User


class UsersService(Service):
    __model__ = User
