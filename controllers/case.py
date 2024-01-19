from app import app

import sqlite3
import pandas
from flask import render_template, request, session

from utils import get_connection



@app.route('/case', methods=['get'])
def case():
    connection = get_connection()
    
    html = render_template(
        'case.html',
        len = len
    )
    return html
