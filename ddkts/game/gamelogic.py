import pylast
import random
import re
import time
import datetime
import os

# need refactoring. t or f shouldn't be a separate function.


def setup(): # returns pylast.Network object
    API_KEY = os.environ.get('API_KEY')
    # print(API_KEY)
    API_SECRET = os.environ.get('API_SECRET')

    
    API_KEY="d0fdedba80f404a92cf3bb7dcda39230" 
    API_SECRET='9a15aac73a7776dcf8deee14d7a18f30' 
    # when I host this you'll see
    network = pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
    )
    return network

def get_recents_mbids(user, days=7):
    ago = datetime.datetime.timestamp(datetime.datetime.today() - datetime.timedelta(days=days))

    tops = user.get_top_tracks(limit=10)
    tops = list(map(lambda track: track.item, tops))
    print(tops)

    print('Loading listening history...')
    recents = user.get_recent_tracks(limit=20,time_from=int(ago),time_to=int(time.time()))
    
    tops = list(set([(t) for t in tops])) # this works because apparently tops are tracks themselves as a class but recent tracks are PlayedTrack items with extra data about the time stamp etc
    recents = list(set([(t.track) for t in recents]))
    # for serialisation purposes i think (hope this can be changed) they are all strigns
    return tops, recents
def get_tops_mbids(user, days=7):
    # TODO: look up how to get tops of date range 
    ago = datetime.datetime.timestamp(datetime.datetime.today() - datetime.timedelta(days=days))
    tops = user.get_top_tracks(limit=10)
    tops = list(map(lambda track: track.item.mbid, tops))
    # for serialisation purposes i think (hope this can be changed) they are all strigns
    return  tops


def game(user, tops, recents):
    r_copy = recents
    # print(len(tops), len(recents))
    # remove duplicates
    # notimplemented # if stranger, show top artists to infer
    score = 0
    for i in range(5):
        print(f'======= Round {i+1} =======')
        if len(recents) ==0:
            t_or_f = False
            question = generate_question(tops, r_copy, False)

        else:
            t_or_f = bool(random.randint(0,1))

            question = generate_question(tops, recents, t_or_f)
        
        if t_or_f:
            recents.remove(question) # stop repeats
        print('-',question,'- \n')
        # let user guess
        correct = guess(f'Do you think {user.name} has played this track in the past week? y/n ', t_or_f)
        # output result
        if correct:
            score += 1
        print(result(correct))
        print('Score:', score)
        time.sleep(1)
    print('============\nYou got', score, 'out of 5. \n')
    time.sleep(1)
    return play_again()

def get_user(username, network):
    ''' returns a user object '''
    user = network.get_user(username)
    if not user:
        print('Error:User not found/they have no played tracks')
        return None

    try:
        if user.get_recent_tracks(limit=1):
            return user # user exists
                

    except pylast.PyLastError:
        print('Error: Network error or User they have no played tracks')
        raise ConnectionRefusedError

def generate_question(t, r, t_or_f):
    ''' t means top tracks, r means recent tracks, torf is the intended correct answer.'''
    
    try:
        rando = random.choice(t)
    except IndexError:
        return None

    if t_or_f == True:
        # select one of their listened tracks
        return random.choice(r)
    else:
        #depending on difficulty selected (randomly), choose
        return random.choice(t) # for now, we just choose a top track to fool them

        # return select_similar(rando, t, r)

def select_similar(rando, t, r):
    def tag_similar(track):
        # print('Trying similar tags...')
        # too obscure so we have to generate through selecting a tag
        tags = track.get_top_tags()
        if not tags:
            return None
        tag = random.choice(tags).item
        return tag.get_top_tracks(10)

    def artist_similar(track):
        # returns a list of artist top tracks
        # print('Trying similar artists...')
        artists = track.get_artist().get_similar(5)
        if not artists:
            return None
        a = random.choice(artists).item
        return a.get_top_tracks(10)

    def track_similar(track):
        # print('Trying similar tracks...')
        t = track.get_similar(10)
        return None if not t else t

    # print(rando)
    functions = [track_similar,artist_similar, tag_similar]
    while True:
        t.remove(rando)
        # try out all functions
        for function in functions:

            try:
                similar_tracks = [t.item for t in function(rando)]
                for similar_track in similar_tracks:
                    st = similar_tracks.pop(random.randint(0,len(similar_tracks)))
                    if st not in r:
                        return st
                    # print('uhh')
            except IndexError:
                continue
            except TypeError:
                continue


        # # there are no similar tracks
        # print(f'{rando} is too indie. Retrying..')
        # both have been listened to - pick another 'base' track instead
        rando = random.choice(t)

