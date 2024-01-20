from app import app

import sqlite3
import pandas
from flask import render_template, request, session

from models.case_model import *
from utils import get_connection



@app.route('/case', methods=['get'])
def case():
    connection = get_connection()


    if ("case" in request.values):
        session["case_id"] = request.values["case"]

    if ("evidance_select" in request.values):
        evidance_select_id = request.values["evidance_select"]
    else:
        evidance_select_id = ""

    if ("suspect_select" in request.values):
        suspect_select_id = request.values["suspect_select"]
    else:
        suspect_select_id = ""

    if ("witness_select" in request.values):
        witness_select_id = request.values["witness_select"]
    else:
        witness_select_id = ""

    if ("culprit_select" in request.values):
        culprit_select_id = request.values["culprit_select"]
    else:
        culprit_select_id = ""
    
    if ("add_evidance" in request.values):
        add_evidance_to_case(connection, evidance_select_id, session["case_id"])
    if ("add_suspect" in request.values):
        add_suspect_to_case(connection, suspect_select_id, session["case_id"])
    if ("add_witness" in request.values):
        add_witness_to_case(connection, witness_select_id, session["case_id"])
    if ("choose_culprit" in request.values):
        choose_culprit(connection, culprit_select_id, session["case_id"])

    df_case = get_case(connection)
    df_case_suspect = get_case_suspect(connection, session["case_id"])
    df_suspect_without_case = get_suspect_without_case(connection, session["case_id"])
    df_case_witness = get_case_witness(connection, session["case_id"])
    df_witness_without_case = get_witness_without_case(connection, session["case_id"])
    df_case_evidance = get_case_evidance(connection, session["case_id"])
    df_evidance_without_case = get_evidance_without_case(connection, session["case_id"])

    html = render_template(
        'case.html',
        case_id = session["case_id"],

        evidances = df_case_evidance,
        not_case_evidances = df_evidance_without_case,
        selected_evidance = evidance_select_id,
        suspects = df_case_suspect,
        not_case_suspects = df_suspect_without_case,
        selected_suspect = suspect_select_id,
        witnesses = df_case_witness,
        not_case_witnesses = df_witness_without_case,
        selected_witness = witness_select_id,
        selected_culprit = culprit_select_id,
        len = len
    )
    return html
