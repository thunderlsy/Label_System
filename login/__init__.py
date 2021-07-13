#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint

login_bp = Blueprint("login", __name__, url_prefix="/login")

from login.views import *
