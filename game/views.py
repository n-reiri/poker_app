# game/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Player

def home(request):
    """
    ホーム（ログイン）ビュー
    - 未ログイン時: AuthenticationForm を表示・処理
    - ログイン済み時: 部屋一覧へリダイレクト
    """
    if request.user.is_authenticated:
        return redirect('room_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('room_list')
    else:
        form = AuthenticationForm()

    return render(request, 'game/home.html', {'form': form})


def signup(request):
    """
    サインアップ→即ログイン→マイ部屋一覧へ
    成功メッセージを表示します。
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 認証＆ログイン
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            # 成功メッセージ
            messages.success(request, f'登録完了！ようこそ、{ username } さん。')
            return redirect('room_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def room_list(request):
    """
    マイ部屋一覧表示＋新規部屋作成
    ホスト自身の部屋だけを表示します。
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        room = Room.objects.create(name=name, host=request.user)
        # ホスト自身を参加者にも登録
        Player.objects.create(room=room, user=request.user)
        return redirect('room_list')

    rooms = Room.objects.filter(host=request.user, is_active=True)
    return render(request, 'game/room_list.html', {'rooms': rooms})


@login_required
def join_room(request, room_id):
    """
    部屋に参加（POST のみ）
    ホスト自身しか参加できないよう制限しています。
    """
    if request.method != 'POST':
        return redirect('room_list')

    room = get_object_or_404(Room, pk=room_id, host=request.user, is_active=True)
    Player.objects.get_or_create(room=room, user=request.user)
    return redirect('game', room_id=room.id)


@login_required
def game(request, room_id):
    """
    ゲーム画面
    ホストまたは参加済みユーザーのみアクセス可
    """
    room = get_object_or_404(Room, pk=room_id, is_active=True)
    is_hosted = (room.host == request.user)
    is_player = Player.objects.filter(room=room, user=request.user).exists()
    if not (is_hosted or is_player):
        return redirect('room_list')

    players = Player.objects.filter(room=room)
    return render(request, 'game/game.html', {
        'room_id': room_id,
        'players': players,
    })


@login_required
def results(request, room_id):
    """
    結果画面
    最終チップ順にソートして表示
    アクセス制御は game() と同様
    """
    room = get_object_or_404(Room, pk=room_id, is_active=True)
    is_hosted = (room.host == request.user)
    is_player = Player.objects.filter(room=room, user=request.user).exists()
    if not (is_hosted or is_player):
        return redirect('room_list')

    players = Player.objects.filter(room=room).order_by('-chips')
    return render(request, 'game/results.html', {
        'room': room,
        'players': players,
    })