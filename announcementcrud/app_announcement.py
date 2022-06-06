import markdown
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from usercrud.query import user_by_id
from usercrud.model import Announcement
from datetime import datetime
import pytz

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_announcement = Blueprint('announcement', __name__,
                             url_prefix='/announcement',
                             template_folder='templates/announcement/',
                             static_folder='static',
                             static_url_path='static')


def ann_all_alc():
    table = Announcement.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready


@app_announcement.route('/')
@login_required
def announcement():
    # defaults are empty, in case user data not found
    user = ""
    list_announcement = []
    print("in announcement")
    # grab user database object based on current login
    uo = user_by_id(current_user.userID)

    # if user object is found
    if uo is not None:
        user = uo.read()  # extract user record (Dictionary)
        if uo.announcement is None:
            print("about to die")
        for content in uo.announcement:  # loop through each user note
            print(content)
            content = content.read()  # extract note record (Dictionary)
            content['content'] = markdown.markdown(content['content'])  # convert markdown to html
            list_announcement.append(content)  # prepare note list for render_template
        if list_announcement is not None:
            list_announcement.reverse()
    # render user and note data in reverse chronological order(display latest notes rec on top)
    print(list_announcement)
    return render_template('announcement.html', user=user, ann=list_announcement)


# Notes create/add
@app_announcement.route('/create/', methods=["POST"])
@login_required
def create():
    """gets data from form and add to Notes table"""
    if request.form:
        # construct a Notes object
        content_object = Announcement(
            request.form.get("content"), datetime.now(pytz.timezone('America/Los_Angeles')).strftime("%H:%M:%S %p %Z, %a %m/%d/%Y"), current_user.userID
        )
        # create a record in the Notes table with the Notes object
        content_object.create()
    return redirect(url_for('announcement.announcement'))