from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.dinner import Dinner

# ADD HTML
@app.route('/add_dinner')
def create_dinner():
    if 'user_id' in session:
        user = User.get_user({'id' : session['user_id']})
        return render_template('create.html')
    return redirect('/')


# ADD DINNER FORM
@app.route('/add', methods=["POST"])
def add_dinner():
    if Dinner.validate_dinner(request.form):
        dinner_id = Dinner.save_dinner(request.form)
        print(dinner_id)
        return redirect(f'/view_dinner/{ dinner_id }')
    else: 
        return redirect('/add_dinner')
    

# VIEW HTML
@app.route('/view_dinner/<int:dinner_id>')
def view_dinner(dinner_id):
        if 'user_id' in session:
            user = User.get_user({'id' : session['user_id']})
            data = {
                'id': dinner_id
            }
            print(data)
            dinner = Dinner.get_dinner(data)
            return render_template ('view_one.html', user=user, dinner=dinner)
        return redirect('/')

# EDIT DINNER HTML
@app.route('/edit_dinner/<int:dinner_id>')
def edit_dinner(dinner_id):
        if 'user_id' in session:
            user = User.get_user({'id' : session['user_id']})
            data = {
                'id': dinner_id
            }
            print(data)
            dinner = Dinner.get_dinner(data)
            return render_template ('edit.html', user=user, dinner=dinner)
        return redirect('/')