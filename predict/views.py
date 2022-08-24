from __future__ import absolute_import, division, print_function, unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Game
##
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from users.models import Profile
from tensorflow.keras import *
from datetime import datetime
from pytz import timezone
from django.template import loader
import requests, json, time, operator, pickle, random
import functools
import numpy as np
import pandas as pd
import tensorflow as tf
import seaborn as sns
import random
##test
####ffffffffasdfasdf
#helloaadsfasdf
#asdsfsasdfasdasdfasd


def saveEdit(request,pk,change,**kwargs):

    changes = change[7:].split('-')
    changes.pop(-1)
    print(changes)
    context = {}
    user = request.user
    g = Game.objects.filter(pk=pk)
    csvid = g.values('csvid')[0]['csvid']
    path = 'csv/'+str(user.username)+str(csvid)+'.csv'
    csv = open(path,'r')
    first=True
    data = ''
    header = ''
    for line in csv.readlines():
        if first:
            header = line
            first = False
        else:
            data = line
    data = data.split(',')
    header= header.split(',')
    print(data,'-------')

    data.pop(0)
    header.pop(0)
    data.pop(0)
    header.pop(0)

    labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']

    for c in changes:
        x = c.split(':')
        n=17*int(x[0])-17+int(x[1])
        data[n-2]=x[2]
        print(n)
        print(data[n-2])
    print(data,'fffffffffffff')


    writeCSVHeader(labels, path)
    def w(data, path, g):
        ss = '1,'+str(g.values('gameid')[0]['gameid'])
        for st in data:
            ss+=','+st
        print('$$$$$$$$$',ss)
        printp=(path)
        f = open(path,'a')
        f.write(ss+'\n')
    w(data, path,g)
    LABEL_COLUMN = 'winner'
    LABELS = [0, 1]
    l = labels
    p = predict(l, LABELS,LABEL_COLUMN,path)
    print(p)

    p = float(p[0])
    g.update(prediction=p)

    return redirect('home-predict')



##
def editGame(request,pk,**kwargs):
    context = {}
    user = request.user
    g = Game.objects.filter(pk=pk)
    csvid = g.values('csvid')[0]['csvid']

    def get_labels():
        lol= []
        ll = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
        for l in ll:
            lol.append(l.upper())
        return lol
    context['labels']= get_labels()
    context['asdf']= 'oof'

    path = 'csv/'+str(user.username)+str(csvid)+'.csv'
    csv = open(path,'r+')
    header = ''
    data= ''
    first = True
    for line in csv.readlines():
        if first:
            header = line
            first = False
        else:
            data = line
            break
    data = data.split(',')
    header= header.split(',')
    print(data,'ooooof')
    data.pop(0)
    data.pop(0)
    header.pop(0)
    header.pop(0)
    players = {}
    oofnog = []#skrt
    for i in range(0,6):
        oofnog.append(g.values('p'+str(i))[0]['p'+str(i)])
    url = 'https://www.balldontlie.io/api/v1/players/'
    resp = []

    for id in oofnog:
        obj = load_obj('2019PlayerNamesByID')

        found = False
        for x in obj:

            if int(x) == int(id):
                found = True
                print('found-------')
                resp.append(obj[x])

        if not found:
            r = req(url+str(id))
            fn = r['first_name']
            ln = r['last_name']
            full = fn+' '+ln
            resp.append(full)

    c = 0
    for oof in range(1,7):
        n=17*oof-17
        temp = [str(oof)]
        for f in range(n,n+17):
            temp.append(data[f])

        players.update({ resp[c] : temp })
        c+=1


    context['stats']= players
    context['home']=g.values('home')[0]['home']
    context['visitor']=g.values('visitor')[0]['visitor']
    context['gamedate']=g.values('gamedate')[0]['gamedate']
    context['home_score']=g.values('home_score')[0]['home_score']
    context['visitor_score']=g.values('visitor_score')[0]['visitor_score']
    context['home_spread']=g.values('home_spread')[0]['home_spread']
    context['visitor_spread']=g.values('visitor_spread')[0]['visitor_spread']
    context['prediction']=g.values('prediction')[0]['prediction']
    context['finished']=g.values('finished')[0]['finished']
    context['winner'] = g.values('winner')[0]['winner']
    print(players)

    return render(request, 'predict/edit.html',context)
def predictToday(request,**kwargs):
    #print(request)




    print('predictToday------------------############-------------')
    return redirect('home-predict')

def getScore(request,pk,**kwargs):
    url = 'https://www.balldontlie.io/api/v1/games/'
    user= request.user
    g = Game.objects.filter(pk=pk).values('gameid')
    g = g[0]
    url += g['gameid']
    r = req(url)
    h = r['home_team_score']
    print('url====',url)

    v= r['visitor_team_score']
    if r['status'] == "Final":
        prediction = Game.objects.filter(pk=pk).values('prediction')[0]['prediction']
        finished = Game.objects.filter(pk=pk).values('finished')[0]['finished']
        if not finished: # add not back
            if prediction >= .5 and h >v:#win p home
                asdf = float(Profile.objects.values('gain')[0]['gain']) + float(prediction) - float(.5)
                Profile.objects.update(gain=asdf)
                Profile.objects.update(correct=Profile.objects.values('correct')[0]['correct']+1)
                Game.objects.filter(pk=pk).update(winner=1)
            if prediction < .5 and h < v:#win p visitor
                asdf = float(Profile.objects.values('gain')[0]['gain']) + float(.5) -float(prediction)
                Profile.objects.update(gain=asdf)
                Profile.objects.update(correct=Profile.objects.values('correct')[0]['correct']+1)
                Game.objects.filter(pk=pk).update(winner=0)
            if prediction < .5 and h > v:#loose p vis
                asdf = float(Profile.objects.values('loss')[0]['loss']) + float(.5) - float(prediction)
                Profile.objects.update(loss=asdf)
                Game.objects.filter(pk=pk).update(winner=1)
            if prediction >= .5 and h < v:#loose p home
                print('asdf')
                asdf = float(Profile.objects.values('loss')[0]['loss']) + float(prediction) - float(.5)
                Profile.objects.update(loss=asdf)
                Game.objects.filter(pk=pk).update(winner=0)
            print(Game.objects.filter(pk=pk).values('winner')[0]['winner'])
            Profile.objects.update(predictions=Profile.objects.values('predictions')[0]['predictions']+1)
        Game.objects.filter(pk=pk).update(finished=True)
    Game.objects.filter(pk=pk).update(home_score=h)
    Game.objects.filter(pk=pk).update(visitor_score=v)
    return redirect('home-predict')

def todaysGames(self):
    url = 'https://www.balldontlie.io/api/v1/games?dates[]='
    eastern = timezone('America/Los_Angeles')
    fmt = '%Y-%m-%d'
    loc_dt = datetime.now(eastern)
    #naive_dt = datetime.now()
    url+=loc_dt.strftime(fmt)
    print(url)
    r = req(url)
    games = []
    for game in range(len(r['data'])):
        habv = r['data'][game]['home_team']['abbreviation']
        hfn = r['data'][game]['home_team']['full_name']
        hscore = str(r['data'][game]['home_team_score'])
        vabv = r['data'][game]['visitor_team']['abbreviation']
        vfn = r['data'][game]['visitor_team']['full_name']
        vscore = str(r['data'][game]['visitor_team_score'])
        status = r['data'][game]['status']
        if hscore != '0' or vscore != '0':
            x = hfn+' '+hscore+' v '+vfn+' '+vscore+' : '+status
        else:
            x = hfn+' '+' v '+vfn+' '+' : '+status
        games.append(x)
    return games





class GameListView(ListView, LoginRequiredMixin):
    model = Game
    template_name = 'predict/home.html'
    ordering = ['-date_posted']
    paginate_by = 10
    context_object_name = 'games'
    context = 'games'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(GameListView, self).get_context_data(**kwargs)
        x = todaysGames(self)
        context['today'] = x
        context['correct'] = Profile.objects.filter(user=user).values('correct')[0]['correct']
        context['numpred'] =  Profile.objects.filter(user=user).values('predictions')[0]['predictions']
        if Profile.objects.filter(user=user).values('predictions')[0]['predictions'] >= 1:
            context['pc'] = round(Profile.objects.filter(user=user).values('correct')[0]['correct']/Profile.objects.filter(user=user).values('predictions')[0]['predictions']*100,1)
        else:

            context['pc'] = 'Predict some Games'
        context['gain'] =  Profile.objects.filter(user=user).values('gain')[0]['gain']
        context['loss'] =  Profile.objects.filter(user=user).values('loss')[0]['loss']
        context['lg'] = Profile.objects.filter(user=user).values('gain')[0]['gain'] - Profile.objects.filter(user=user).values('loss')[0]['loss']
        #context['form'] = GameForm()
        context['ordering']= ['-date_posted']
        return context
    def get_queryset(self, **kwargs):
        user = self.request.user
        return Game.objects.filter(author=user).order_by('-date_posted')

    def form_valid(self, form):
        print('-------------------')
        form.instance.author = self.request.user
        season = '2021'

        path = 'csv/'+str(form.instance.pk)+'.csv'
        labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
        x = form.instance.gamedate
        y = form.instance.home.upper()
        z = form.instance.visitor.upper()
        date=x
        homeAbv=y
        visitorAbv=z
        found, gameid = futureGame(date, homeAbv,visitorAbv,path,season,labels)
        if found:
            form.instance.gameid = gameid
        return super().form_valid(form)


class TodaysGamesCreate(LoginRequiredMixin, CreateView):
    model = Game
    template_name = 'predict/new.html'
    fields = ['gamedate']
    csvid = random.randint(1,100000)
    def form_valid(self, form, **kwargs):
        form.instance.author = self.request.user
        season = '2019'
        form.instance.csvid = self.csvid
        path = 'csv/'+str(self.request.user)+str(self.csvid)+'.csv'
        print(path)
        labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
        x = form.instance.gamedate
        #y = form.instance.home.upper()
        #z = form.instance.visitor.upper()






class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    template_name = 'predict/new.html'
    fields = ['home', 'visitor','gamedate','home_spread','visitor_spread']
    csvid = random.randint(1,100000)
    def form_valid(self, form, **kwargs):
        form.instance.author = self.request.user
        season = '2019'
        form.instance.csvid = self.csvid
        path = 'csv/'+str(self.request.user)+str(self.csvid)+'.csv'
        print(path)
        labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
        x = form.instance.gamedate
        y = form.instance.home.upper()
        z = form.instance.visitor.upper()
        date=x
        homeAbv=y
        visitorAbv=z
        found, gameid, playerids = futureGame(date, homeAbv,visitorAbv,path,season,labels)
        if found:

            form.instance.p0 = playerids[0]
            form.instance.p1 = playerids[1]
            form.instance.p2 = playerids[2]
            form.instance.p3 = playerids[3]
            form.instance.p4 = playerids[4]
            form.instance.p5 = playerids[5]

            LABEL_COLUMN = 'winner'
            LABELS = [0, 1]
            l = labels
            #p = predict(l, LABELS,LABEL_COLUMN,path)
            #form.instance.prediction = float(p[0])
            form.instance.gameid = gameid

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(GameCreateView, self).get_context_data(**kwargs)
        x = todaysGames(self)
        context['today'] = x
        context['csvid'] = self.csvid
        print(self.csvid,'---------------------------')
        return context


def futureGame(date,homeAbv,visitorAbv,path, season,labels):
    print(season)
    url = 'https://www.balldontlie.io/api/v1/games?dates[]='
    url+=date
    response = req(url)
    nOsTAtsYET = {}
    found = False
    gameid = 0
    playerids = []
    for game in range(len(response['data'])):
        ha = response['data'][game]['home_team']['abbreviation']
        va = response['data'][game]['visitor_team']['abbreviation']
        if ha==homeAbv and va==visitorAbv:
            print('found---------------')
            found = True
            gameid = response['data'][game]['id']
            data = nextGame(gameid)
            data.update({'home_team_id':response['data'][game]['home_team']['id']})
            data.update({'visitor_team_id':response['data'][game]['visitor_team']['id']})
            playerIdByTeamID = load_obj('2019PlayerIdByTeamID')
            for player in playerIdByTeamID[str(data['home_team_id'])]:
                data['home_team_players'].update({ player : nOsTAtsYET})
            for player in playerIdByTeamID[str(data['visitor_team_id'])]:
                data['visitor_team_players'].update({ player : nOsTAtsYET})
            data.update({'home_team_score' : response['data'][game]['home_team_score']})
            data.update({'visitor_team_score' : response['data'][game]['home_team_score']})
            getPlayerAvg(data,season)#gets players stats by player ids
            minuteConversion(data)#chops off seconds se we only have mins
            sortByPlayTime(data)#sorts player into two groups good players and team players

            writeCSVHeader(labels, path)
            playerids=writeCSV(data, path, labels)
    print(found,'---------')
    return found, gameid,playerids

#------------------------------------------------------------------------#
def sortByPlayTime(data):
    derp = ['home', 'visitor']
    for foo in derp:
        for i in range(3):
            maxMin = 0
            id = ''
            for player in data[foo+'_team_players']:
                old = maxMin
                maxMin = max(maxMin, int(data[foo+'_team_players'][player]['min']))
                if maxMin > old:#this line messed me up i had >= and could figure out why it wasnt working finally got it.
                    id = player
            try:
                data[foo+'_good_players'].update({id : data[foo+'_team_players'][id]})
                data[foo+'_team_players'].pop(int(id), None)
            except KeyError:
                print('key error')
    return data
#------------------------------------------------------------------------#
def minuteConversion(data):
    #chop seconds off...
    derp = ['home', 'visitor']
    for foo in derp:#iter home visitor
        for player in data[foo+'_team_players']:#iter players
            min = ''
            if data[foo+'_team_players'][player] != '':#takes care of non values
                time = data[foo+'_team_players'][player]['min']
                if str(type(time)) == "<class 'str'>":
                    for char in time:#iter charecters in time
                        if char != ':':
                            min += str(char)
                        else:
                            break
                    data[foo+'_team_players'][player].update({'min' : min})
                        #print(data[foo+'_team_players'][player]['min'])
    return data
#------------------------------------------------------------------------#
#gets season average stats by player ids.....
def getPlayerAvg(data,season,**kwargs):
    url = 'https://www.balldontlie.io/api/v1/season_averages?season='
    url += season+'&player_ids[]='
    teams = ['home', 'visitor']
    playerStats = load_obj(season+'playerStats')
    print('loaded # player stats: ', len(playerStats))
    for team in teams:
        badPlayer = False
        badPlayerid = 0#gosh i hope there is only ever 1 of these on each team else smh nooo
        for playerid in data[team+'_team_players']:
            foundSaved = False
            #check if player has been saved
            for splayerid in playerStats:
                if playerid == splayerid:
                        data[team+'_team_players'].update({playerid : {}})#here it is again#soo anoying
                        for statName in playerStats[playerid]:
                            data[team+'_team_players'][playerid].update({statName :playerStats[playerid][statName]})
                        print('found saved -----------####-------------id: ', playerid)
                        foundSaved = True
                        break
            #get unsaved season averages
            if not foundSaved:
                uurl = url+str(playerid)
                response = req(uurl)

                data[team+'_team_players'].update({playerid : {}})
                print(len(response['data']))
                if len(response['data']) != 0:#this is sad it means a player didnt play a single game all season
                    for statName in response['data'][0]:
                        data[team+'_team_players'][playerid].update({ statName: response['data'][0][statName]})
                    playerStats.update({playerid : {}})
                    for statName in data[team+'_team_players'][playerid]:
                        playerStats[playerid].update({statName : data[team+'_team_players'][playerid][statName]})
                    print('not saved -----------####-------------id: ', playerid)
                else:
                    badPlayer = True
                    badPlayerid = playerid
        if badPlayer:
            print('badplayer#--------', badPlayerid)
            data[team+'_team_players'].pop(badPlayerid, None)
            badPlayer=False

    save_obj(playerStats, season+'playerStats')
    return data

#------------------------------------------------------------------------#


#clears data of last game and gets ready for next
def nextGame(gameid):
    data = {}
    data.update({'gameid' : gameid})
    data.update({'home_team_players' : {}})
    data.update({'visitor_team_players' : {}})
    data.update({'home_good_players' : {}})
    data.update({'visitor_good_players' : {}})
    #data.update({'home_team_id' : 0})
    #data.update({'visitor_team_id' : 0})
    return data

#------------------------------------------------------------------------#
def writeCSV(data, path, labels):
    derp = ['home', 'visitor']
    if data['home_team_score']>=data['visitor_team_score']:
        line = '1'
    else:
        line = '0'
    playerids = []
    if data['gameid'] != 'tooFewPlayers':
        print('writing----------------------------------')
        line+=','+str(data['gameid'])
        for foo in derp:
            for goodPlayer in data[foo+'_good_players']:
                playerids.append(str(data[foo+'_good_players'][goodPlayer]['player_id']))
                for label in labels:
                    line+=','+str(data[foo+'_good_players'][goodPlayer][label])
            #for averages
            #for label in labels:
                #line+=','+str(data[foo+'_team_players']['avg'][label])
        c = line.count(',')
        #if c == 229:
        csv = open(path,'a')#appending
        csv.write(line+'\n')

        #else:
            #print('+++++##########RED ALERT SUMTHING WENT WRONG AND MADE IT PAST ALL CHECKS ')
    else:
        print('gameid: -------------',data['gameid'],len(data['home_team_players']))
        print('gameid: -------------',data['gameid'],len(data['visitor_team_players']))
    return playerids
#------------------------------------------------------------------------#
def writeCSVHeader(labels, path):
    header = 'winner,gameid'
    derp = ['home_', 'visitor_']
    for foo in derp:
        for i in range(1,4):
            for label in labels:
                header+=','+foo+str(i)+'_'+label
    csv = open(path,'w')
    csv.write(header+'\n')
    csv.close()
    return header
#------------------------------------------------------------------------#
def req(url):
    proxy = load_obj('proxy')
    dict = {}
    p = random.randint(0,len(proxy)-1)
    dict.update({'http' : proxy[p]})
    r = requests.get(url)
    print('proxy: ', proxy[p], 'url: ', url, 'response: ', r)
    if str(r) != '<Response [200]>':#means we request too fast.
        time.sleep(5)
        req(url)
    #time.sleep(.1)
    return r.json()
#------------------------------------------------------------------------#
def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
#------------------------------------------------------------------------#TensorFlow Time

def predict(l, LABELS,LABEL_COLUMN, path):
    def sss(l):
        s = ''
        derp = ['home_', 'visitor_']
        for foo in derp:
            for i in range(1,4):
                for label in l:
                    s+=foo+str(i)+'_'+label+','
        return s
#------------------------------------------------------------------------#
    foo = 'winner,gameid,'
    s = sss(l)
    fdsa = foo + s
#------------------------------------------------------------------------#
    def create_columns(s):
        csv_columns = []
        a = ''
        for char in s:
            if char != ',':
                a += char
            else:
                csv_columns.append(a)
                a = ''
        return csv_columns
#------------------------------------------------------------------------#
    def defaults(fdsa):
        d = []
        for i in range(0,len(create_columns(fdsa))):
            d.append(0.0)
        return d
#------------------------------------------------------------------------#
    def get_dataset(file_path,epochs, **kwargs):
        dataset = tf.data.experimental.make_csv_dataset(
          file_path,
          batch_size= 25,
          label_name=LABEL_COLUMN,
          na_value="?",
          num_epochs=epochs,
          ignore_errors=True,
          **kwargs)
        return dataset
#------------------------------------------------------------------------#
    class PackNumericFeatures(object):
      def __init__(self, names):
        self.names = names
      def __call__(self, features, labels):
        numeric_features = [features.pop(name) for name in self.names]
        numeric_features = [tf.cast(feat, tf.float32) for feat in numeric_features]
        numeric_features = tf.stack(numeric_features, axis=-1)
        features['numeric'] = numeric_features
        return features, labels
#------------------------------------------------------------------------#
    def normalize_numeric_data(data, mean, std):
        # Center the data
        return (data-mean)/std
#------------------------------------------------------------------------#
    def prep(file_path, fdsa, s,epochs):
        dataset = get_dataset(file_path, select_columns=create_columns(fdsa), column_defaults = defaults(fdsa),epochs=epochs)
        NUMERIC_FEATURES = create_columns(s)
        packed_dataset = dataset.map(PackNumericFeatures(NUMERIC_FEATURES))
        desc = pd.read_csv(file_path)[NUMERIC_FEATURES].describe()
        #print(desc)
        MEAN = np.array(desc.T['mean'])
        STD = np.array(desc.T['std'])
        normalizer = functools.partial(normalize_numeric_data, mean=MEAN, std=STD)
        numeric_column = tf.feature_column.numeric_column('numeric', shape=[len(NUMERIC_FEATURES)])
        numeric_columns = [numeric_column]
        numeric_layer = tf.keras.layers.DenseFeatures(numeric_columns)
        preprocessing_layer = tf.keras.layers.DenseFeatures(numeric_columns)

        return preprocessing_layer, packed_dataset
#------------------------------------------------------------------------#

    preprocessing_layer, test_dataset = prep('ffasdf.csv', fdsa, s,epochs =1)
    model = tf.keras.Sequential([
        preprocessing_layer,
        tf.keras.layers.Dense(300, activation='relu'),
        tf.keras.layers.Dense(300, activation='relu'),
        #tf.keras.layers.Dense(1000, activation='relu'),
        #tf.keras.layers.Dense(500, activation='relu'),
        tf.keras.layers.Dense(1,activation='sigmoid'),
    ])
    model.compile(
        loss='binary_crossentropy',
        optimizer='adamax',
        metrics=['accuracy'])

    model.load_weights('./checkpoints/my_checkpoint')
    preprocessing_layer, test_dataset = prep(path, fdsa, s,epochs = 1)
    predictions = model.predict(test_dataset,steps=1)
    return predictions[0]
