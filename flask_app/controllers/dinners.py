from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.dinner import Dinner


@app.route('/create_dinner')
def create_dinner():
    if 'user_id' in session:
        user = User.get_user({'id' : session['user_id']})
        return render_template('create.html')
    return redirect('/')



@app.route('/add', methods=["POST"])
def add_dinner():
    if Dinner.validate_dinner(request.form):
        dinner_id = Dinner.save_dinner(request.form)
        return redirect(f'/view_dinner/{ dinner_id }')
    else: 
        return redirect('/create_dinner')
    
