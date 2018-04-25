"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')  # Gets github from form or URL arguments

    first, last, github = hackbright.get_student_by_github(github)  # Unpacks tuple
    project_grades = hackbright.get_grades_by_github(github)  # List of tuples

    #passes first, last, github to html
    html = render_template('student_info.html', first=first, last=last, github=github, project_grades=project_grades)

    #return rendered template with args
    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""


    return render_template("student_search.html")


@app.route("/student-add")  # Can be the same route as below since this is using GET method
def student_add_form():
	"""Renders html template"""

	return render_template("student_add.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    # execute function to add to db
    hackbright.make_new_student(first_name, last_name, github)

    return render_template("success.html", github=github, first_name=first_name, last_name=last_name)
    #return redirect('/success')

@app.route("/project")
def project_listing():
	"""Displays details about a student's project"""
	title = request.args.get('title')  # Get title from URL parameters

	title, description, max_grade = hackbright.get_project_by_title(title)  # (title, description, max_grade) from projects table

	return render_template("project_listing.html", title=title, description=description, max_grade=max_grade)
	


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
