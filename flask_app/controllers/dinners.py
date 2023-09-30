from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.dinner import Dinner


# GET RANDOM DINNER
@app.route('/get_dinner')
def get_tonights_dinner():
    if 'user_id' in session:
        user = User.get_user({'id' : session['user_id']})
        dinner = Dinner.get_random_dinner()
        return render_template('view_one.html', dinner = dinner)
    return redirect('/')

# ADD HTML
@app.route('/add_dinner')
def create_dinner_html():
    if 'user_id' in session:
        user = User.get_user({'id' : session['user_id']})
        return render_template('create.html')
    return redirect('/')


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
            print(dinner.id)
            return render_template ('view_one.html', user=user, dinner=dinner)
        return redirect('/')


# EDIT DINNER HTML
@app.route('/edit_dinner/<int:dinner_id>')
def edit_dinner_html(dinner_id):
        if 'user_id' in session:
            user = User.get_user({'id' : session['user_id']})
            data = {
                'id': dinner_id
            }
            print(data)
            dinner = Dinner.get_dinner(data)
            return render_template ('edit.html', user=user, dinner=dinner)
        return redirect('/')

# DELETE DINNER
@app.route('/delete_dinner/<int:dinner_id>')
def delete_dinner(dinner_id):
    data = {
        'id': dinner_id
    }
    Dinner.delete_dinner(data)
    return redirect('/dashboard')


# FORMS ###############################################


# ADD DINNER FORM
@app.route('/add', methods=["POST"])
def add_dinner():
    if Dinner.validate_dinner(request.form):
        dinner_id = Dinner.save_dinner(request.form)
        print(dinner_id)
        return redirect(f'/view_dinner/{ dinner_id }')
    else: 
        return redirect('/add_dinner')
    
@app.route('/edit', methods=["POST"])
def edit_dinner():
    if Dinner.validate_dinner(request.form):
        dinner_id = Dinner.edit_dinner(request.form)
        print(dinner_id)
        return redirect(f'/view_dinner/{ request.form["dinner_id"] }')
    else: 
        return redirect(f'/edit_dinner/{ request.form["dinner_id"] }')