from application import app
from flask import render_template,flash,redirect,request
from .forms import TodoForm
from flask.templating import render_template_string
from werkzeug.datastructures import RequestCacheControl
from datetime import datetime
from application import db
from bson import ObjectId
@app.route("/")
def get_todos():
    todos=[]
    for todo in db.todo.find().sort("date_created",-1):
        todo["_id"]=str(todo["_id"])
        todo["date_created"]=todo["date_created"].strftime("%b %d %Y %H:%M%S")
        todos.append(todo)
    return render_template("view_todo.html",title=" layout page", todos=todos)


@app.route("/add_todo" ,methods=["POST","get"])
def add_todo():
    if request.method == "POST":
        form =TodoForm(request.form)
        todo_name=form.name.data
        todo_completed=form.completed.data
        todo_description=form.description.data
        
        db.todo.insert_one({
            "name": todo_name,
            "description": todo_description,
            "completed": todo_completed,
            "date_created": datetime.utcnow()
        })
        flash("Todo successfully added", "success")
        return redirect("/")
    else:
        form =TodoForm()
    return render_template("add_todo.html",form =form)

@app.route("/update_todo/<id>" ,methods=["POST","get"])
def update_todo(id):
    if request.method == "POST":
        form =TodoForm(request.form)
        todo_name=form.name.data
        todo_completed=form.completed.data
        todo_description=form.description.data
        
        db.todo.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": todo_name,
            "description": todo_description,
            "completed": todo_completed,
            "date_created": datetime.utcnow()
        }})
        flash("Todo successfully added", "success")
        return redirect("/")
    else:
        form =TodoForm()
        todo=db.todo.find_one_or_404({"_id":ObjectId(id)})
        form.name.data=todo.get("name",None)
        form.description.data=todo.get("description",None)
        form.completed.data=todo.get("completed",None)
        
    return render_template("add_todo.html",form =form)
@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.todo.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo successfully deleted", "success")
    return redirect("/")