from object_types import vote, post, phase

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mafia"]


def add_vote_to_db(vote, game):
    col = db["votes"]
    myquery = { "postnum": vote.postnum, "game": game }
    newvalues = { "$set": { "voter": vote.voter, "target": vote.target, "url": vote.url, "postnum": vote.postnum, "game": game } }
    col.update_one(myquery, newvalues, upsert=True)
    return


def get_votes_by_range(game, start, end):
    col = db["votes"]
    res = col.find({ "game": game, "postnum": { "$gte": start, "$lte": end } })
    return list(res)


def get_votes_by_voter(game, player):
    col = db["votes"]
    res = col.find({ "game": game, "voter": player })
    return list(res)


def get_votes_by_target(game, player):
    col = db["votes"]
    res = col.find({ "game": game, "target": player })
    return list(res)


def add_post_to_db(post, game):
    col = db["posts"]
    myquery = { "post_id": post.id }
    newvalues = { "$set": { "post_id": post.id, "author": post.author, "content": post.HTML, "postnum": post.postnum, "date":post.date, "game": game } }
    col.update_one(myquery, newvalues, upsert=True)
    return


def get_posts_by_authors(game, authors):
    col = db["posts"]
    res = col.find({ "game": game, "author": { "$in": authors } })
    return list(res).sort({"postnum": 1})  # sort the database objects by p#


def add_phase_to_db(phase, game):
    col = db["phases"]
    myquery = { "postnum": phase.postnum, "game": game }
    newvalues = { "$set": { "postnum": phase.postnum, "phase": phase.phase_name, "game": game } }
    col.update_one(myquery, newvalues, upsert=True)
    return


def add_alias_to_db(name, alias):
    col = db["aliases"]
    myquery = { "alias": alias }
    newvalues = { "$set": { "alias": alias, "name": name } }
    col.update_one(myquery, newvalues, upsert=True)
    return


# In addition to this, I'll need a function to update database keys.
# Should be similar to updateData from the replit code.
def update_key_in_db(key, value):
    col = db["data"]
    q = { "key": key }
    col.delete_one(q)
    col.insert_one({ "key": key, "value": value })
    return


# I'll also need a function to get data from the database.
def get_data_from_db(key):
    col = db["data"]
    q = { "key": key }
    res = col.find_one(q)
    if res is None:
        return None
    return res["value"]


