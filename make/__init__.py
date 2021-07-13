#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint

make_bp = Blueprint("make", __name__, url_prefix="/make")

from make.views import *
