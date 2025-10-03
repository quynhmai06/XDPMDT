# admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from models import db, User

admin_bp = Blueprint("admin", __name__)

# GET /admin -> hiển thị admin.html (nếu chưa login sẽ thấy form trong template)
@admin_bp.route("/admin", methods=["GET"], endpoint="admin_dashboard")
def admin_dashboard():
    return render_template("admin.html", users=[], products=[], transactions=[])

# POST /admin/login -> xử lý form đăng nhập trong admin.html
@admin_bp.route("/admin/login", methods=["POST"], endpoint="admin_login")
def admin_login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = User.query.filter_by(username=username, is_admin=True).first()
    if not user:
        flash("❌ Không tìm thấy tài khoản admin", "error")
        return redirect(url_for("admin.admin_dashboard"))

    if not check_password_hash(user.password, password):
        flash("❌ Sai mật khẩu", "error")
        return redirect(url_for("admin.admin_dashboard"))

    session["admin_id"] = user.id
    session["is_admin"] = True
    session["username"] = user.username
    flash("✅ Đăng nhập thành công!", "success")
    return redirect(url_for("admin.admin_dashboard"))

# GET /admin/logout -> đăng xuất
@admin_bp.route("/admin/logout", methods=["GET"], endpoint="logout")
def logout():
    session.clear()
    flash("✅ Đã đăng xuất!", "success")
    return redirect(url_for("admin.admin_dashboard"))
