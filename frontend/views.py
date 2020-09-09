from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from web.models import Player, PlayerList

# Create your views here.


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "frontend/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('show_index')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            player = Player(name=user, wins=0, loses=0, ties=0)
            player.save()
            player_list = PlayerList(player=player, ready_to_play=False)
            player_list.save()

            login(request, user)
            return redirect('show_index')
    else:
        form = UserCreationForm()
    return render(request, 'frontend/signup.html', {'form': form})


@login_required(login_url='login/')
def show_index(request):
    user = str(request.user)
    player = Player.objects.get(name=request.user)
    return render(request, 'frontend/index.html', {'username': user, 'player': player})


@login_required(login_url='login/')
def show_game(request, room_name):
    user = str(request.user)
    return render(request, 'frontend/game.html', {'room_name': room_name, 'username': user})
