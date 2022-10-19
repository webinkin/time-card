from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
import os
from forms import TimeInput
import requests
import datetime


app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)



@app.route('/', methods=['GET', 'POST'])
def home():
    form = TimeInput()
    if request.method == "POST":
        date = form.date.data
        print(date)
        new_date = date.isocalendar()
        week = new_date[1]

        date = date.strftime("%m/%d/%Y")
        arrival = form.arrived.data
        departure = form.departed.data
        working_time = datetime.datetime.combine(datetime.date.today(), departure) - datetime.datetime.combine(
            datetime.date.today(), arrival)
        time = working_time.total_seconds()
        hours = int(time / 3600)
        left_over_seconds = time % 3600
        minutes = left_over_seconds / 60
        percent_of_hour = minutes / 60
        hours_worked = hours + percent_of_hour
        now = datetime.datetime.now()
        now = now.strftime("%m/%d/%Y")

        sheety_params = {
            "hour": {
                "recorded": now,
                "date": date,
                "hours": hours_worked,
                "week": week
            }
        }
        endpoint = os.environ.get("SHEETY_ENDPOINT")
        response = requests.post(url=endpoint, json=sheety_params)
        return redirect(url_for('success'))
    return render_template("index.html", form=form)

@app.route('/success')
def success():
    return render_template('success.html')



if __name__ == "__main__":
    app.run(port=9000, debug=True)
