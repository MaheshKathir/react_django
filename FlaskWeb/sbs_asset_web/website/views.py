from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . models import Assets
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # asset_all_details = None
    if request.method == 'POST': 
        # note = request.form.get('note')#Gets the note from the HTML
        Bay_No = request.form.get('Bay_No')
        Employee_Id = request.form.get('Employee_Id')

        if len(Employee_Id) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Assets(Bay_No=Bay_No,Employee_Id=Employee_Id, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')
            
    asset_all_details = Assets.query.all()

    return render_template("home.html", asset_all_details=asset_all_details, user=current_user)

@views.route('/filter', methods = ['POST'])
@login_required
def filter():
    if request.method == 'POST':
        # Bay_No = request.form.get('Bay_No')
        Employee_Id = request.form.get('Employee_Id')
        # print(Employee_Id)

        # Assuming Assets is your model and you have a column 'Bay_No' and 'Employee_Id'
        filtered_assets = Assets.query.filter_by(Employee_Id=Employee_Id).all()
        # print(filtered_assets)

        # Pass the filtered results to the template
        return render_template("home.html", filtered_assets=filtered_assets, user=current_user)
    

    # Handle other cases, e.g., invalid request method
    return render_template("error.html", message="Invalid request method")



@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Assets.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['asset_Id']
    print(note)
    asset = Assets.query.get_or_404(noteId)
    print(asset)

    if request.method == 'POST':
        new_employee_id  = note['new_employee_id']
        asset.Employee_Id =  new_employee_id
        filtered_assets = Assets.query.filter_by(Employee_Id=new_employee_id).all()
       
        db.session.commit()

        flash('Record updated successfully!', category='success')
       

        return render_template("home.html", filtered_assets=filtered_assets, user=current_user)
    
    # Handle other cases, e.g., invalid request method
    return render_template("error.html", message="Invalid request method")
