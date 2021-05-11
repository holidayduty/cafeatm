from flask import Flask, Blueprint
import os


bp = Blueprint('hello', __name__)

bp.route('/')


def Hello():
    print('Hello World')
