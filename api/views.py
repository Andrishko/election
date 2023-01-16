from datetime import datetime
import random
import string
from time import strptime

from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *


def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))

    return result_str


def check_time(start, finish):
    print(type(timezone.now()))
    if start < timezone.now() < finish:
        return True
    else:
        return False


@api_view(['POST'])
def gettokens(request: Request):
    tokens = []
    data = request.data
    i = 0
    while i < int(data['number']):
        user = CustomUser.objects.create_user(username=get_random_string(10), faculty=data['faculty'])
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        tokens.append(access_token)
        user.token = access_token
        user.save()

        i += 1

    return Response(tokens)


@api_view(['GET'])
def thanks(request: Request):
    return render(request, 'thanks.html')


@api_view(['GET'])
def votingexpired(request: Request):
    return render(request, 'votingExpired.html')


@api_view(['GET'])
def voted(request: Request):
    return render(request, 'youVoted.html')


# @api_view(['GET'])
# def check(request: Request, user_token):
#     data = request.data
#     user = CustomUser.objects.get(token=user_token)
#     vote = Votings.objects.get(faculty=Faculty.objects.get(faculty_name=user.faculty))
#     print(check_time(vote.start, vote.finish))
#     if check_time(vote.start, vote.finish):  # time check
#         if user.is_voted == 1:  # is voted check
#             return render(request, 'test.html')
#         else:
#             user.is_voted = True
#             user.save()
#             return render(request, 'electionfront/build/index.html')
#     else:
#         return Response("voting don`t active")


# @api_view(['POST'])
# def get_candidates(request: Request):
#     data = request.data
#     serializer_data = Candidates.objects.filter(faculty=Faculty.objects.get(faculty_name=data['faculty']).id)
#     serializer = CandidatesSerializer(instance=serializer_data, context={'request': request}, many=True)
#     print(serializer.data)
#     return Response(serializer.data)


# @api_view(['PUT'])
# def vote(request: Request):
#     data = request.data
#     print(data)
#     vote = Votings.objects.get(faculty=Faculty.objects.get(faculty_name=data['faculty']).id)
#     if check_time(vote.start, vote.finish):
#
#         goals = Goals.objects.get(candidate_name=Candidates.objects.get(
#             Q(candidate_name=data['candidate']) & Q(faculty=Faculty.objects.get(faculty_name=data['faculty']))).id)
#         goals.candidate_goals = goals.candidate_goals + 1
#         goals.save()
#         return Response("true")
#     else:
#         return Response("false")
#
#
# @api_view(['POST'])
# def get_faculty(request: Request):
#     data = request.data
#     user = CustomUser.objects.get(token=data['token'])
#     return Response(user.faculty)


@api_view(['POST'])
def get_votings(request: Request):
    data = request.data
    active_votings = []

    serializer_data = Votings.objects.filter(Q(faculty=Faculty.objects.get(faculty_name=data['faculty']).id) | Q(
        faculty=Faculty.objects.get(faculty_name='spu').id))  # отримання списку голосувань
    serializer = VotingsSerializer(instance=serializer_data, context={'request': request}, many=True)
    for i in serializer.data:
        print(i['start'])
        if check_time(datetime.strptime(i['start'], '%Y-%m-%dT%H:%M:%S%z'),
                      datetime.strptime(i['finish'], '%Y-%m-%dT%H:%M:%S%z')):
            active_votings.append({"name": i['name'], "faculty": Faculty.objects.get(
                id=i['faculty']).faculty_name})  # створення списку активних голосувань
    return Response(active_votings)


@api_view(['GET'])
def test(request: Request, user_token):
    data = request.data
    print(user_token)
    user = CustomUser.objects.get(
        token=user_token)
    vote = Votings.objects.get(faculty=Faculty.objects.get(faculty_name=user.faculty).id)

    if check_time(vote.start, vote.finish):  # time check
        if user.is_voted == 1:  # is voted check
            return render(request, 'youVoted.html')
        else:
            print(Candidates)
            candidates = Candidates.objects.filter(faculty=Faculty.objects.get(faculty_name=user.faculty).id).values()
            print(candidates)

            context = {
                "candidates": candidates,
                "token": user_token
            }
            return render(request, 'test.html', context=context)
    else:
        return render(request, 'votingExpired.html')


@api_view(['PUT'])
def votetest(request: Request):
    data = request.data
    vote = Votings.objects.get(faculty=Candidates.objects.get(id=data['candidate']).faculty)
    user = CustomUser.objects.get(token=data['token'])

    if check_time(vote.start, vote.finish):
        if user.is_voted == 1:  # is voted check
            data = {
                "status": "voted"
            }
            return JsonResponse(data)
        else:
            user.is_voted = 1
            user.save()
            goals = Goals.objects.get(candidate_name=data['candidate'])
            goals.candidate_goals = goals.candidate_goals + 1
            goals.save()
            data = {
                "status": "true"
            }
            return JsonResponse(data)
    else:

        data = {
            "status": "false"
        }
        return JsonResponse(data)
