#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint

index_bp = Blueprint("index", __name__, url_prefix="/index")

from index.views import *
