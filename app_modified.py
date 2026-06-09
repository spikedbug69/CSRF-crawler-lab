from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = "novashield-lab-secret"

PAGE = """
<!doctype html>
<html>
<body>
<h2>NovaShield Security Portal</h2>

<p><b>Current Recovery Email:</b> {{ email }}</p>

<form action="/update-email" method="POST">
    <label>Recovery Email:</label><br>
    <input name="email" value="{{ email }}" required>
    <button type="submit">Update Email</button>
</form>

{% if updated %}
<p style="color:green;">Email updated successfully.</p>
{% endif %}

<hr>
<p><b>Lab Note:</b> This form intentionally has no CSRF protection for educational testing.</p>
</body>
</html>
"""

@app.before_request
def seed_user():
    if "email" not in session:
        session["email"] = "spike@lab.local"

@app.get("/")
def index():
    return render_template_string(
        PAGE,
        email=session["email"],
        updated=request.args.get("updated") == "1"
    )

@app.post("/update-email")
def update_email():
    new_email = request.form.get("email", "").strip()
    if new_email:
        session["email"] = new_email
    return redirect(url_for("index", updated=1))

if __name__ == "__main__":
    app.run(debug=True)
