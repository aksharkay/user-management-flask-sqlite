from flask import Blueprint, request, render_template, redirect, url_for
from app.models.user import User as UserModel
from app.extentions import db

bp = Blueprint("user", __name__)

@bp.route('/user/')
def showAllPage():
    users = UserModel.query.all()
    return render_template('user/show-all.html', users=users)

@bp.route('/user/', methods = ["POST"])
def store():
    new_user = UserModel(
        name = request.form["name"],
        email = request.form["email"]
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('user.showAllPage'))

@bp.route('/user/create')
def createPage():
    return render_template('user/create.html')

@bp.route('/user/update/<int:id>')
def updatePage(id):
    existing_user = db.session.get(UserModel, id)
    return render_template('user/update.html', user=existing_user)

@bp.route('/user/<int:id>', methods = ["GET", "POST", "DELETE"])
def userID(id):
    if request.method == "GET":
        return render_template('user/show-one.html', id=id)
    elif request.method == "POST":
        existing_user = UserModel.query.get(id)
        existing_user.name = request.form["name"]
        existing_user.email = request.form["email"]
        db.session.commit()
        return redirect(url_for('user.showAllPage'))
    elif request.method == "DELETE":
        user = UserModel.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return "Deleted"
