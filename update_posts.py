# This file updates the votes and posts in the database.


#read_one_page reads a single page of posts from a game, sets the last read page to the page number, and returns the posts as a list.
def read_one_page(game, page):
    # Read the page from the game's URL
    # Parse posts into a list
    # Set last read page in database to page number
    # Return the list
    return NotImplemented


#read_from_last reads all posts from the last read page to the current page and returns the posts as a list.
def read_from_last(game):
    # Get last read page from database
    # Repeat read_one_page for each page from last read page to current page
    # Append the result from each read_one_page to a list
    # Return the list
    return NotImplemented


#update_game updates the posts and votes in the database for a game.
def update_game(game):
    # Call read_from_last to get all posts from the last read page to the current page
    # For each post in the list:
        # Check if the post is already in the database
        # If not, add the post to the database
        # If yes, update the post in the database
        # Check if the post has votes
        # If yes, update the votes in the database
    return NotImplemented