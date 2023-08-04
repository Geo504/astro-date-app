import datetime
from flask import request

from models.users import User
from models.profile_info import Profile
from utils.db import db

def like_profile(user):
    user_likes = request.json.get('user_likes')
    user_db = User.query.get(user["id"])

    liked_user_db = []

    for liked in user_likes:
        liked_user = User.query.get(liked)
        if liked_user:
            liked_user_db.append(liked_user)

    user_db.likes_to = liked_user_db
    db.session.commit()

    return user_db.serialize_with_likes()



def info_profile(user):
    profile_data = Profile.query.filter_by(user_id=user["id"]).first()
    born_date = datetime.datetime.strptime(request.json.get("date_born"), "%Y-%m-%dT%H:%M:%S")

    if profile_data:
        profile_data.profile_image = request.json.get("profile_image")
        profile_data.zodiac_sign = request.json.get("zodiac_sign")
        profile_data.location = request.json.get("location")
        profile_data.gender = request.json.get("gender")
        profile_data.love_interest = request.json.get("love_interest")
        profile_data.date_born = born_date
        db.session.commit()
        
        user_updated = User.query.get(user["id"])
        return user_updated.serialize_with_profile()
    else:
        new_profile_data = Profile(**request.json)
        new_profile_data.user_id = user["id"]
        new_profile_data.date_born = born_date

        db.session.add(new_profile_data)
        db.session.commit()

        user_updated = User.query.get(user["id"])

        return user_updated.serialize_with_profile()