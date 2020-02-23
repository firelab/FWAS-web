from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from loguru import logger

from ..models import User
from ..utils import safe_next_url
from .decorators import anonymous_required
from .forms import LoginForm

user = Blueprint("user", __name__, template_folder="templates")


@user.route("/login", methods=["GET", "POST"])
@anonymous_required()
def login():
    form = LoginForm(next=request.args.get("next"))

    if form.validate_on_submit():
        account = User.find_by_identity(request.form.get("identity"))

        if account and account.authenticated(password=request.form.get("password")):
            logger.debug(f"Login successful for {account.email}")
            if login_user(account, remember=True) and account.is_active:
                account.update_activity_tracking(request.remote_addr)

                next_url = request.form.get("next")
                if next_url:
                    return redirect(safe_next_url(next_url))

                return redirect(url_for("user.dashboard"))

            flash("This account has been disabled.", "error")
        else:
            logger.warning("Invalid identity or password")
            flash("Identity or password is incorrect.", "error")
    else:
        logger.warning("Invalid form validation on login page.")

    return render_template("user/login.html", form=form)


@user.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("user/dashboard.html")


@user.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("user.login"))


@user.route("/signup", methods=["GET", "POST"])
def signup():
    pass


@user.route("/reset", methods=["GET", "POST"])
def begin_password_reset():
    pass
