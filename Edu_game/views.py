import html

from django.shortcuts import render

# Create your views here.
import requests
import json
import random
from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect
from html.parser import HTMLParser

from Edu_game.models import GameCategory, GameScore
from Edu_user.models import Student


def get_category(request):
    context = {'category': GameCategory.objects.all()}
    return render(request, 'category.html', context)


def fetch_question(cat):
    r = requests.get(cat.categoryurl)
    r_as_json = json.loads(r.text)
    global question
    global correct_answer
    global options
    question = html.unescape(r_as_json['results'][0]['question'])
    options = html.unescape(r_as_json['results'][0]['incorrect_answers'])
    correct_answer = html.unescape(r_as_json['results'][0]['correct_answer'])
    options.append(correct_answer)
    random.shuffle(options)


def start_play(request, *arg, **kwargs):
    game_id = kwargs['game_id']
    cat = GameCategory.objects.get(id=game_id)
    if request.method == "GET":
        fetch_question(cat)
    if request.method == "POST":
        user_answer = request.POST.get("choice")
        score: GameScore = GameScore.objects.filter(student__id_num=request.user.username, category__category=cat)
        if "next" in request.POST:
            fetch_question(cat)
        elif 'results' in request.POST:
            return HttpResponseRedirect(f"/results/{game_id}")
        else:

            if user_answer == correct_answer:

                if score.count() == 1:
                    obj = GameScore.objects.get(student__id_num=request.user.username, category__category=cat)
                    obj.correct_answers += 1
                    obj.save()
                elif score.count() > 1:
                    print('more than two obj has found')
                else:

                    GameScore(category=cat, student=Student.objects.get(id_num=request.user.username), correct_answers=1,
                              wrong_answers=0, score=100).save()

            else:
                if score.count() == 1:
                    obj = GameScore.objects.get(student__id_num=request.user.username, category__category=cat)
                    obj.wrong_answers += 1
                    obj.save()
                elif score.count() > 1:
                    print('more than two obj has found')
                else:

                    GameScore(category=cat, student=Student.objects.get(id_num=request.user.username), wrong_answers=1,
                              correct_answers=0, score=0).save()

            fetch_question(cat)

    random.shuffle(options)
    context = {'category': cat.category,
               'options': options,
               'question': question,


               }
    return render(request, 'play.html', context)


def get_results(request, *args, **kwargs):
    game_id = kwargs.get('game_id')
    cat = GameCategory.objects.get(id=game_id)
    score_obj = GameScore.objects.get(student__id_num=request.user.username, category=cat)

    GameScore_score = round(100*score_obj.correct_answers / (score_obj.wrong_answers + score_obj.correct_answers),2
                       )
    context = {
        'score': GameScore_score,
        'game_id': game_id
    }
    return render(request, 'results.html', context)
