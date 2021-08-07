from django.http import HttpResponse
from django.shortcuts import render


def list_of_post(request):
    return HttpResponse('lista de posts')


def post_detail(request):
    return HttpResponse('detalhes do post')


def list_of_post_by_category(request):
    return HttpResponse('lista de posts por categoria')
