from flask import Blueprint, render_template, redirect, url_for, request
from . import db
from .models import User, Event
from flask_login import current_user, login_required
from datetime import datetime

event_bp = Blueprint('event', __name__)

@event_bp.route('/new-event', methods=['POST', 'GET'])
@login_required
def new_post():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect('/login')

        event_title = request.form['title']
        event_description = request.form['description']
        event_club = request.form['club']
        event_location = request.form['location']
        event_dateTime = request.form['datetime']

        # Check if 'tbd' checkbox is checked
        if 'tbd' in request.form:
            event_dateTime = None  # Set to None if TBD
        else:
            event_dateTime = datetime.fromisoformat(request.form['datetime']).strftime('%B %d, %Y at %I:%M %p')

        new_event = Event(title=event_title, description=event_description, 
        club=event_club, user_id=current_user.id, location=event_location, dateTime=event_dateTime)

        try:
            db.session.add(new_event)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your event'
    else:
        events = Event.query.order_by(Event.date_created).all()

        return render_template("new-event.html", events=events, user=current_user, include_header=True)

@event_bp.route('/event/<int:id>')
def read_more(id):
    event = Event.query.get_or_404(id)
    return render_template('read-more.html', event=event, user=current_user,  include_header=True)

@event_bp.route('/delete/<int:id>')
def delete(id):
    event_to_delete = Event.query.get_or_404(id)

    try:
        db.session.delete(event_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that event'


@event_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    event = Event.query.get_or_404(id)

    if request.method == 'POST':
        event.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your event'
    else:
        return render_template('update.html', event=event, include_header=True)
