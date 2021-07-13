#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint

label_edit_bp = Blueprint("labeledit", __name__, url_prefix="/labeledit")
relation_edit_bp = Blueprint("relationedit", __name__, url_prefix="/relationedit")
user_edit_bp = Blueprint("useredit", __name__, url_prefix="/useredit")

from edit.views import *
