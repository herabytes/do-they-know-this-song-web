
import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.core.cache import cache
from . import gamelogic

# Create your views here.

network = gamelogic.setup()

# def track_to_useful_dict(t):
#     """ converts Track object into a dict that can be turned into json by Django. Only includes useful things:
#     mbid,
#     name,
#     artist"""
#     print("dictified")
#     print(t)
#     return {
#         "mbid": t.get_mbid(),
#         "title":str(t)
#     }


def index(request):
    if request.method == "GET":
        return render(request, 'game/index.html')
    
def play(request):
    ''' instantiates a game. '''
    if request.method == "POST":
        try:
            subjectUser = gamelogic.get_user(request.POST["username"], network)
        except ConnectionRefusedError:
            messages.add_message(request, messages.ERROR, message="Network error")
            return HttpResponseRedirect(reverse(index))

        request.session["subjectUser"] = str(subjectUser)
    
        if subjectUser == None:
            messages.add_message(request, messages.ERROR, message="User does not exist")
            return HttpResponseRedirect(reverse(index))
        tops, recents = gamelogic.tops_and_recents(subjectUser)
        # request.session["tops"] = [track_to_useful_dict(t) for t in tops]
        # print("Tops saved in session")
        # request.session["recents"] = [track_to_useful_dict(t) for t in recents]
        # print("Recents saved in session")

        print("redirecting to question page")
        # ideally from now on the server is just sitting here like hey front end if you want a new question i'll throw one at you, it's all curated
        # actually no i want this game to be available to go on for as long as you like and if you quite a game you'll still have stuff saved
        # therefore generate question on the go
        

        # but how??? the problem is that it's hard to serialise the tops and recents and make generate_question work.
        # unfortunately, for now the way to do this is to request the recents AND get the questions all ready in the same view.
        # we can choose to do this in play or question.
        # or we can scrap generating similar
        return HttpResponseRedirect(reverse('question'))
    else:
        return HttpResponseRedirect(reverse('index'))
    
    
def question(request):
    # t_or_f = bool(random.randint(0,1))
    # request.session["t_or_f"] = t_or_f
    print("are we good?")
    track = gamelogic.generate_question(request.session["tops"], request.session["recents"], t_or_f)
    # print(track.get_mbid())

    request.session["track"] = track
    # request.session["track_id"] = track.get_mbid()

    return render(request, 'game/game.html', context={
        # 'track': track,
        # 'subjectUser': request.session["subjec"],
        # 'timeframe': "week" this is stupid because you can access session variables in the template bruh
    })

def answer(request):
    
    if request.method == "POST":
        
        return render(request, 'game/game.html', context={
                        "correct": request.POST["answer"] == str(request.session["t_or_f"])
                    })


