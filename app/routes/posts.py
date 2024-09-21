from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_injector import inject
from app.services.posts import PostService
from app.forms.posts.create_post import CreateForm
from app.forms.posts.edit_post import EditForm
from flask_login import current_user
from app.decorators import role_required


posts = Blueprint("posts", __name__)

@posts.route("/")
@inject
def list_all(post_service: PostService):
    if current_user.role=="author":
        return render_template("author/author_home.html", posts=post_service.get_all_AuthorPosts(user_id=current_user.id))
    else:
        return render_template("reader/reader_home.html", posts=post_service.get_all())


@posts.route("/create")
@role_required(['author'])
def create():
    return render_template("/posts/create.html", form=CreateForm())

@posts.route("/", methods=["POST"])
@inject
def store(post_service: PostService):
    create_form = CreateForm()

    if create_form.validate_on_submit():
        post_service.create(
            title = create_form.title.data,
            content = create_form.content.data,
            user_id = current_user.id
        )

        return redirect(url_for("posts.list_all"))

    return render_template("/posts/create.html", form=create_form)

@posts.route("/<id>")
@inject
def view(post_service: PostService, id):
    post = post_service.get_by_id(id)

    if not post:
        return redirect(url_for("posts.list_all"))

    return render_template("posts/view.html", post=post)

@posts.route("/<id>/edit")
@inject
@role_required(['author','admin'])
def edit(post_service: PostService, id):
    post = post_service.get_by_id(id)

    if not post:
        return redirect(url_for("posts.list_all"))

    edit_form = EditForm()
    edit_form.title.data = post.title
    edit_form.content.data = post.content

    return render_template("posts/edit.html", form=edit_form, post=post)

@posts.route("/<id>", methods=["POST"])
@inject
def update(post_service: PostService, id):
    post = post_service.get_by_id(id)

    if not post:
        return redirect(url_for("posts.list_all"))

    edit_form = EditForm()

    if edit_form.validate_on_submit():
        post_service.update(
            post,
            edit_form.title.data,
            edit_form.content.data,
        )
        if current_user.role == "author":
            return redirect(url_for("posts.list_all"))
        else:
            return redirect(url_for("admin.list_all_posts"))


    return render_template("posts/view.html", post=post)

@posts.route("/<id>", methods=["DELETE"])
@inject
@role_required(['author','admin'])
def delete(post_service: PostService, id):
    post = post_service.get_by_id(id)
    if post:
        post_service.delete(post)

    return jsonify({"msg": "Product deleted successfully"})

@posts.route("/like/<post_id>", methods=["POST"])
@inject
@role_required('reader')
def toggle_like(post_service: PostService, post_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401

    post_service.toggle_like(post_id, current_user.id)

    post = post_service.get_by_id(post_id)
    
    return jsonify({"likes": post.likes}), 200