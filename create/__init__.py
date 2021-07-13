#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint

upload_bp = Blueprint("create", __name__, url_prefix="/create")

from __init__.views import *
