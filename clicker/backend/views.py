from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .forms import UserForm
from .models import Core, Boost
from .serializer import CoreSerializer, BoostSerializer


@login_required
def index(request):
    core = Core.objects.get(user=request.user)
    boosts = Boost.objects.filter(core=core) 
    return render(request, 'index.html', {'core': core, 'boosts': boosts})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@api_view(['GET'])
@login_required
def call_click(request):
    core = Core.objects.get(user=request.user)
    is_levelup = core.click()
    if is_levelup:
        Boost.objects.create(core=core, price=core.coins, power=core.level * 2)
    core.save()
    return Response({'core': CoreSerializer(core).data, 'is_levelup': is_levelup})


@api_view(['POST']) 
def update_coins(request): 
    coins = request.data['current_coins']
    core = Core.objects.get(user=request.user)

    is_levelup, boost_type = core.set_coins(coins)
   
    if is_levelup: 
        Boost.objects.create(core=core, price=core.coins, power=core.level*2, type=boost_type) # Создание буста. Добавили атрибут type.
    core.save()

    return Response({
        'core': CoreSerializer(core).data, 
        'is_levelup': is_levelup,
    })


@api_view(['GET'])
def get_core(request):
    core = Core.objects.get(user=request.user)
    return Response({'core': CoreSerializer(core).data})


@api_view(['GET'])
@login_required
def buy_boost(request, id):
    core = Core.objects.get(user=request.user)
    boost = Boost.objects.get(id=id)
    if core.coins > 0:
        core.click_power += boost.power
        core.coins -= boost.price
        core.save()
        return Response({'coins': core.coins})
    return Response("Not enough money", status=400)


class Register(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form': form})    
  
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            core = Core(user=user)
            core.save()
            return redirect('index')
        return render(request, 'register.html', {'form': form})
    
    
class Login(APIView):
    form = UserForm()
    
    def get(self, request):
        return render(request, 'login.html', {'form': self.form})
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('index')
        return render(request, 'login.html', {'form': self.form, 'invalid': True})
    

class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer
    
    
    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = Boost.objects.filter(core=core)
        return boosts
    
    def partial_update(self, request, pk):
        coins = request.data['coins']
        boost = self.queryset.get(pk=pk)

        is_levelup = boost.levelup(coins)
        if not is_levelup:
            return Response({ "error": "Не хватает денег" })
        old_boost_stats, new_boost_stats = is_levelup

        return Response({
            "old_boost_stats": self.serializer_class(old_boost_stats).data,
            "new_boost_stats": self.serializer_class(new_boost_stats).data,
        })
