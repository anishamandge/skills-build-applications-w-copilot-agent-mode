from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections

from bson.objectid import ObjectId

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        db = connections['default'].connection
        db = db.get_database('octofit_db')
        # Drop collections if they exist
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            db[col].drop()

        # Teams
        teams = [
            {"_id": ObjectId(), "name": "Team Marvel"},
            {"_id": ObjectId(), "name": "Team DC"}
        ]
        db.teams.insert_many(teams)

        # Users
        users = [
            {"_id": ObjectId(), "name": "Iron Man", "email": "ironman@marvel.com", "team": teams[0]["_id"]},
            {"_id": ObjectId(), "name": "Captain America", "email": "cap@marvel.com", "team": teams[0]["_id"]},
            {"_id": ObjectId(), "name": "Batman", "email": "batman@dc.com", "team": teams[1]["_id"]},
            {"_id": ObjectId(), "name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": teams[1]["_id"]}
        ]
        db.users.insert_many(users)
        db.users.create_index([("email", 1)], unique=True)

        # Activities
        activities = [
            {"_id": ObjectId(), "user": users[0]["_id"], "type": "run", "distance": 5, "duration": 30},
            {"_id": ObjectId(), "user": users[1]["_id"], "type": "cycle", "distance": 20, "duration": 60},
            {"_id": ObjectId(), "user": users[2]["_id"], "type": "swim", "distance": 2, "duration": 40},
            {"_id": ObjectId(), "user": users[3]["_id"], "type": "run", "distance": 10, "duration": 50}
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"_id": ObjectId(), "user": users[0]["_id"], "points": 100},
            {"_id": ObjectId(), "user": users[1]["_id"], "points": 90},
            {"_id": ObjectId(), "user": users[2]["_id"], "points": 110},
            {"_id": ObjectId(), "user": users[3]["_id"], "points": 95}
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"_id": ObjectId(), "user": users[0]["_id"], "suggestion": "5k run"},
            {"_id": ObjectId(), "user": users[1]["_id"], "suggestion": "30 min cycling"},
            {"_id": ObjectId(), "user": users[2]["_id"], "suggestion": "1k swim"},
            {"_id": ObjectId(), "user": users[3]["_id"], "suggestion": "10k run"}
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
