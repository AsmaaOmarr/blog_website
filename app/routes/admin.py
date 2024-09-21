from flask import Blueprint, flash, render_template, redirect, url_for, jsonify,request
from flask_injector import inject
from flask_login import login_required,fresh_login_required
from app.services.user import UserService
from app.services.posts import PostService
from app.decorators import role_required


admin = Blueprint("admin", __name__)


@admin.route("/admin_home")
@login_required
@fresh_login_required
@role_required(['admin'])
def admin_home():
    return render_template("/admin/home.html")

@admin.route("/users")
@inject
@fresh_login_required
@role_required(['admin'])
def list_all_users(user_service: UserService):
    return render_template("admin/users_list.html", users=user_service.get_all())

@admin.route("/posts")
@inject
@fresh_login_required
@role_required(['admin'])
def list_all_posts(post_service: PostService):
    return render_template("admin/posts_list.html", posts=post_service.get_all())


@admin.route("/update_role/<int:id>", methods=["POST"])
@fresh_login_required
@inject
@role_required(['admin'])
def update_role(id: int, user_service: UserService):
    user = user_service.get_by_id(id)
    if user:
        new_role = request.form.get('role')
        if new_role in ['admin', 'author', 'reader']:
            user_service.update_role(user, new_role)
            flash('Role updated successfully!', 'success')
        else:
            flash('Invalid role selected.', 'danger')
    else:
        flash('User not found.', 'danger')
    return redirect(url_for('admin.list_all_users'))