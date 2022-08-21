
from typing import Dict, List, Any
import chess
import sys
import time
import argparse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from cube.sunfish import *
from cube.tools import *



def index(request):
    context = {}
    return render(request, 'cube/index.html',context)
def about(request):
    context = {}
    return render(request, 'cube/about.html',context)

def cube(request):
    context = {}
    return render(request, 'cube/cube.html',context)
def cchess(request):
    context = {}
    return render(request, 'cube/chess.html',context)




def nextMoveSunFish(request):
    context = {}
    print('sunfish move!')
       
    url = request.build_absolute_uri()
    print(url)
    
    surl = url.split('?from=')
    _from = surl[1][0]+surl[1][1]
    surl = url.split('&to=')
    _to = surl[1][0]+surl[1][1]
    

    sub = url.split('&fen=')
    subS = sub[1]
    fen = subS.split("%2F")
    finalFen = ""
    for f in fen:
        finalFen+=f+"/"
        
    finalFen = finalFen.rstrip(finalFen[-1])
    ff=finalFen
    ff +=' w KQkq - 0 1'
    fff=finalFen
    fff +=' b KQkq - 0 1'



    print('from:',_from)
    print('to:',_to)
    print('fen ===========', finalFen)


    pos = parseFEN(ff)
    print_pos(pos)
    f = getMove(pos[0],_from,_to)
 

    return JsonResponse({'asdf': f})
 




def test(request):
    if request.is_ajax():
        request_data = request.POST
        print("Raw Data: " + str(request_data))
        return HttpResponse("OK")
