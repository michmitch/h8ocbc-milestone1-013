import os
from datetime import datetime
from config import db


db.create_all()

db.session.commit()
