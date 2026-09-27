import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import GameProgress, LeaderboardEntry
def game_view(request): return render(request,'game.html')
@csrf_exempt
@require_http_methods(["POST"])
def save_progress(request):
    if not request.user.is_authenticated: return JsonResponse({'error':'login'},status=401)
    d=json.loads(request.body)
    p,_=GameProgress.objects.get_or_create(user=request.user,defaults={'unlocked_phases':[1]})
    p.total_score=d.get('total_score',0);p.current_phase=d.get('current_phase',1);p.unlocked_phases=d.get('unlocked_phases',[1]);p.phase_stars=d.get('phase_stars',{});p.correct_answers=d.get('correct_answers',0);p.mistakes=d.get('mistakes',0);p.best_score=max(p.best_score,d.get('total_score',0));p.save()
    if d.get('game_completed'):
        acc=(p.correct_answers/(p.correct_answers+p.mistakes)*100) if (p.correct_answers+p.mistakes)>0 else 0
        LeaderboardEntry.objects.create(user=request.user,score=p.total_score,total_stars=p.get_total_stars(),accuracy=acc)
    return JsonResponse({'ok':True})
@require_http_methods(["GET"])
def load_progress(request):
    if not request.user.is_authenticated: return JsonResponse({'error':'login'},status=401)
    try:
        p=GameProgress.objects.get(user=request.user)
        return JsonResponse({'total_score':p.total_score,'current_phase':p.current_phase,'unlocked_phases':p.unlocked_phases,'phase_stars':p.phase_stars,'correct_answers':p.correct_answers,'mistakes':p.mistakes,'best_score':p.best_score})
    except: return JsonResponse({'total_score':0,'current_phase':1,'unlocked_phases':[1],'phase_stars':{},'correct_answers':0,'mistakes':0,'best_score':0})
def leaderboard(request):
    qs=LeaderboardEntry.objects.select_related('user')[:20]
    return JsonResponse({'leaderboard':[{'username':x.user.username,'score':x.score} for x in qs]})
def register_view(request):
    if request.method=='POST':
        f=UserCreationForm(request.POST)
        if f.is_valid(): u=f.save();login(request,u);return redirect('game')
    else: f=UserCreationForm()
    return render(request,'registration/register.html',{'form':f})
def login_view(request):
    if request.method=='POST':
        u=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if u: login(request,u);return redirect('game')
    return render(request,'registration/login.html')
def logout_view(request): logout(request);return redirect('game')
@login_required
def profile_view(request):
    p=GameProgress.objects.filter(user=request.user).first()
    return render(request,'profile.html',{'progress':p,'phases':[(1,'Equipamentos'),(2,'Química'),(3,'Física'),(4,'Biologia'),(5,'Final')]})