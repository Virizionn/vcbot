import cloudscraper
from bs4 import BeautifulSoup
import pytz
import datetime
import re

from database import get_all_posts, add_post_to_db, add_vote_to_db, get_game_attr

#These definitions match database.py
class post:  #object to store post data
    def __init__(self, id, author, HTML, postnum, date):
      self.id = id
      self.author = author
      self.HTML = HTML
      self.postnum = postnum
      self.date = date

class vote: #store votes
    def __init__(self, voter, target, url, postnum, game):
        self.voter = voter
        self.target = target
        self.url = url
        self.postnum = postnum
        self.game = game

#read_from_last reads all posts from the last read page to the current page and returns the posts as a list.
def read_from_last(url, last_page_number):

    scrapedPosts = []  #list of post objects
    prev_post_number = -1

    for i in range(last_page_number, 1000):

        #cloudscraper is a library that bypasses cloudflare protection - similar to requests
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url + str(i))
        soup = BeautifulSoup(response.content, 'html.parser')

        firstpostnumber = int(
        soup.find("article", class_='message').find(
            "ul", {
                "class":
                "message-attribution-opposite message-attribution-opposite--list"
            }).text.replace(",", "").replace("\n", "").replace(
                "#", ""))  #first post number of the page
       
        print("Scraping page {} with first post number {}".format(i, firstpostnumber))

        if firstpostnumber == prev_post_number:
            print("Detected end of thread.")
            break

        prev_post_number = firstpostnumber

        #Extract relevant info to create a post object
        for message in soup.find_all("article", class_='message'):

            username = message.find(class_='username').get_text().replace(
                "\n", "").replace(" ", "")
            postnumber = int(
                message.find(
                    "ul", {
                        "class":
                        "message-attribution-opposite message-attribution-opposite--list"
                    }).text.replace("\n", "").replace(",", "").replace("#", ""))
            timestamp = int(message.find("time").get("data-time"))

            # Get a timezone object for the desired timezone
            tz = pytz.timezone('US/Eastern')

            # Convert the timestamp to a datetime object
            dt = datetime.datetime.fromtimestamp(timestamp, tz)
            postdate = dt.strftime('%Y-%m-%d %H:%M %Z')

            postid = message.find("a", rel='nofollow')["href"]
            postid = int(postid[postid.find("post-") + 5:])

            #add post to list
            scrapedPosts.append(
                post(postid, username, str(message), postnumber, postdate))
          
    return scrapedPosts


#update_game updates the posts and votes in the database for a game.
def update_game(game):

    # Call read_from_last to get all posts from the last read page to the current page
    # For each post in the list:
        # Check if the post is already in the database
        # If not, add the post to the database
        # If yes, update the post in the database
        # Check if the post has votes
        # If yes, update the votes in the database
    stored_posts = get_all_posts(game)

    #sort posts by post number
    stored_posts.sort(key=lambda x: x["postnum"])

    #get the last post number
    if stored_posts != []:
        last_post_number = stored_posts[-1]["postnum"]
        last_page_number = last_post_number//20 + 1 #20 posts per page
    else:
        last_post_number = 0
        last_page_number = 1
    
    #need to update this to get the actual thread url from database
    url = get_game_attr(game, "url")
    new_posts = read_from_last(url, last_page_number)

    for post in new_posts:
        if post.postnum > last_post_number:
            add_post_to_db(post, game)

            #check for votes
            message = post.HTML
            message = BeautifulSoup(message, 'html.parser')

            text = (message.find(class_='bbWrapper')).get_text()
         
            for quote in (message.find_all("blockquote")):
                #delete quote from text
                text = text.replace(quote.get_text(), "")

            #check if there's a vote within valid tags
            #Use a regex to find what the LAST text string starting with <vote> and ending with </vote> is
            #Not case sensitive. Stripped. Returns name of target
            matches = re.findall(r'\[vote\](.*?)\[/vote\]', text, re.IGNORECASE | re.DOTALL)
            target = matches[-1].strip() if matches else None

            if target != None:
                v = vote(post.author, target, "google.ca", post.postnum, game)
                print(post.author, target, "google.ca", post.postnum, game)
                add_vote_to_db(v, game)
    

    return

