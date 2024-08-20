# Posts are used by the ISO endpoint to collect all posts by a player.
# User is the player who made the vote
# Number is the post number within the thread
# id is the hypixel forums post id
# Date is the date the post was made
# HTML is the content of the post

class post:
    def __init__(self, author, postnum, id, date, html):
      self.author = author
      self.postnum = postnum
      self.id = id
      self.date = date
      self.HTML = html