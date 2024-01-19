from app import app

import sqlite3
import pandas
from flask import render_template, request, session

from models.index_model import *
from utils import get_connection



@app.route('/', methods=['get', 'post'])
def index():
    connection = get_connection()
    
    #----Дела----#
    df_case = get_case(connection)
    df_suspect = get_suspect(connection)
    df_witness = get_witness(connection)
    df_evidance = get_evidance(connection)

    if ("suspect-filter" in request.values):
        df_selected_suspect = get_selected_suspect(connection, request.values.getlist("suspect-filter"))
    else:
        df_selected_suspect = get_selected_suspect(connection, [])
    
    if ("witness-filter" in request.values):
        df_selected_witness = get_selected_witness(connection, request.values.getlist("witness-filter"))
    else:
        df_selected_witness = get_selected_witness(connection, [])
        
    if ("evidance-filter" in request.values):
        df_selected_evidance = get_selected_evidance(connection, request.values.getlist("evidance-filter"))
    else:
        df_selected_evidance = get_selected_evidance(connection, [])

    if ("actuality-filter" in request.values):
        selected_actuality = request.values.get("actuality-filter")
    else:
        selected_actuality = ""

    if ("filter" in request.values):
        df_case = get_filter_case(connection, request.values.getlist("suspect-filter"), request.values.getlist("witness-filter"), request.values.getlist("evidance-filter"), selected_actuality)
    #----Дела----#
        
    #----Ближайшие допросы----#
    inter_num = 5
    df_closest_interogations = get_closest_interogations(connection)

    if ("inter_num" in request.values):
        inter_num = int(request.values["inter_num"])

    df_work_schedule = get_work_schedule(connection)
    week_days = df_work_schedule["weekday"].tolist()

    if ("set_date" in request.values):
        date = request.values["date"]
        time = request.values["time"]
        inter_id = request.values["inter_id"]
        date_time = ' '.join([date, time])
        set_new_inter_date(connection, inter_id, date_time)

    if ("set_testimony" in request.values):
        testimony = request.values["testimony"]
        inter_id = request.values["inter_id"]
        set_new_testimony(connection, inter_id, testimony)


    #----Ближайшие допросы----#

    html = render_template(
        'index.html',
        cases = df_case,
        suspects = df_suspect,
        witnesses = df_witness,
        evidances = df_evidance,
        selected_suspects = df_selected_suspect,
        selected_witnesses = df_selected_witness,
        selected_evidances = df_selected_evidance,
        selected_actuality = selected_actuality,
        inter_num = inter_num,
        closest_interogations = df_closest_interogations,
        inter_dates = df_closest_interogations["Дата и время допроса"].tolist(),
        week_days_schedule = week_days,
        len = len,
        int = int
    )

    connection.close()
    return html
