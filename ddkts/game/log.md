This thing has been around for a year and now I want to make it playable on the web. So here it is with Django.
I refactored the old code slightly. Importing the functions, I created views for each stage - play and answer, storing the answer in the session variables. 

However today I realised that one could look at all session values, which is bad.
So I propose to have a database that stores each game, so everything is hidden from view. This also comes with the benefit of being able to view past games and share it to your friend. Database wise, here's the description:
Game(GameID, Player, Time)
Question(GameID, QuestionNo, TrackID, CorrectAnswer, Guess)

TrackID links to the API - to display the name and artist etc we will have to make a get_track call or something. In a way this could be slow but we'll see.
It's also nice that we'll get the image from the API.
And we can definitely link it to the last.fm page, or give an iframe that includes a play button instead. Then the user can judge for themselves if they think this track is suitable. If 

Also might use user top tags for a false question.
So the process is:
- Get the user
- Get their recent tracks
- Roll randint for true or false question
- If true question, select one from the recent tracks
- If false question, select a track similar to their recent tracks.
- If none listened to in the timeframe, it should be reported. But for now, it selects a false question by default.






To prevent cheating, one could pick a random person - the person can come from their recent tracks' listeners. We 


UPDATES to bypass serialisation: removed any calling of get_similar of gamelogic
8/6/24: perhaps get_similar above ^ can make a comeback once I figure out how to serialise the track object.

trying json.dumps() to python-serialise the tracks.
else i'll just store the mbid whenever fetching tracks.
it's a little bit inconsistent in that i have to use mbid for cover image but pylast for all else.
seems like object.__dict__ might work.
now the problem is, some object's attributes are also objects... might be a chain that goes on forever. and lots of stuff i don't actually need.
i think i'll just save a dict of things i do need, accessed using get methods.
https://www.geeksforgeeks.org/convert-class-object-to-json-in-python/
looking at the track/_Opus (omg it's a protected class) definition, get_url looks useful too. 
Of course, artists also have mbids. They also have userplaycount, but you must set the Artist.username to be that of the game subject user.


9/6:
tried the track_to_dict. Seems to be incrediby slow, not sure if it's making lots of requests for tops and recents to be serialised and saved in session.
might try just mbid.

13/6:
uhh not the get problems, perhaps the dictifying itself is very slow, potentially limit track count in gamelogic instead.
or get a separate whole list for mbid - nvm. that's bad.

31/7:
added network error warning for get user
- please read up abstract user
- debating whether to add my own track object - nah when you can get stuff


11/11:
Plan:
- CACHE the MBIDs of tops and recents for each user.
- play page receives username and validates it.
- if valid, we fetch tops and recents if not in cache. cache['username'] = {'tops': [], 'similars': [], recents': []}
- mash it into one big list