from flask import Blueprint

management = Blueprint(
    'management',
    __name__,
    template_folder='templates',
)

from management.routes import index
