from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.login import Login

@app.route('/exam_models')
def exam_index():
    if not "user_id" in session:
        return redirect('/')
    return "at the exam index"