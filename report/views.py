from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.http.response import JsonResponse
from report.models import Users
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from report.forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    user = Users.objects.filter(id=request.user.id).first()
    username = user.username if user else "Anonymous User!"
    print("Logged in?", request.user.is_authenticated, request.user.username)
    if request.user.is_authenticated is False:
        username = "Anonymous User!"
    print(username)
    return render(request, "index.html", {"username": username})


@csrf_exempt
def get_user(request, user_id):
    print(user_id)
    if request.method == "GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = Users.objects.filter(pk=user_id).first()
        return render(request, "base.html", {"user": user, "params": [abc, xyz]})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)

        return JsonResponse(dict(msg="You just reached with Post Method!"))


def register(request):
    msg = "### django의 form을 활용한 입력폼입니다. 디자인이 예쁘지 않은 점 양해 바랍니다. ###"
    if request.method == "POST":
        form = RegisterForm(request.POST)
        username = ""
        if form.is_valid():
            print("form is valid")
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "^^ 회원 가입 완료...!!! ^^"
        else:
            msg = "!!! 회원 가입 형식에 맞지 않은 데이터가 입력되었습니다...!!!"
        return render(request, "register.html", {"form": form, "msg": msg, "username": username})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form, "msg": msg})

def login_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원가입완료"
        return render(request, "register.html", {"form": form, "msg": msg})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})


def login_view(request):
    is_ok = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        msg = "가입되어 있지 않거나 로그인 정보가 잘못 되었습니다."
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            msg = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                user = Users.objects.get(username=username)
            except Users.DoesNotExist:
                pass
            else:
                if user.check_password(raw_password):
                    msg = None
                    login(request, user)
                    is_ok = True
                    return redirect("index")

                    # request.session["remember_me"] = remember_me

                    # if not remember_me:
                    #     request.session.set_expiry(0)
    else:
        msg = None
        form = LoginForm()
    # print("REMEMBER_ME: ", request.session.get("remember_me"))
    return render(request, "login.html", {"form": form, "msg": msg, "is_ok": is_ok})


def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def list_view(request):
    username = request.user.username
    page = int(request.GET.get("p", 1))
    users = Users.objects.all().order_by("-id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "boards.html", {"users": users, "username": username})
