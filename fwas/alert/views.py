from flask import Blueprint, render_template
from flask_login import login_required

alert = Blueprint("alert", __name__, template_folder="templates")


@alert.route("/alerts")
@login_required
def list_alerts():
    return render_template("alert/list.html")
