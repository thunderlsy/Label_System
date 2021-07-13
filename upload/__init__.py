#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint

upload_bp = Blueprint("upload", __name__, url_prefix="/upload")

from upload.views import *
