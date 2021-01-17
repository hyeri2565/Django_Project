from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import SeamUser
from django.contrib import auth
from Register_team.views import register_result
from Register_team.models import BeforeTeam,Lecture
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import IntegrityError
from django.db import OperationalError


# from Register_team import after_team


def main(request):
    return render(request, 'users/main.html')


def main2(request):
    return render(request, 'users/main2.html')


def mypage(request):  # login 회원정보와 회원과 연결된 team formation결과 가져온 mypage.html과 연결.
    seam_user = request.user
    seam_user = SeamUser.objects.get(user=seam_user)
    context = {'SeamUser': seam_user}
    u_teams = []

    try:
        if request.method == "POST":
            kid2 = seam_user.kid
            all_list = BeforeTeam.objects.filter(kid=kid2)
            lec_list = Lecture.objects.all()

            new_lec_list = []
            for j in lec_list:
                new_lec_list.append(j.name_lecture)

            result_t = []
            # for i in list(all_list):
            #     result_t = register_result(i.lecture__name)

            for i in new_lec_list:
                result_t = register_result(i)

            # result_t = [{t1, t2, t4}, {t3, t5}]
            for team in result_t:
                if kid2 in [t.kid for t in team]:
                    u_teams.append(team)

        if len(u_teams) == 0:
            context.update({'output': "가능한 조합의 팀이 없어 팀을 구성할 수 없습니다."})
            return render(request, 'users/mypage.html', context)

        else:
            output = ""
            for i in u_teams:
                for k in i:
                    output += f"Lecture Name : {k.lecture_name} / Team name : {k.team_name} / Numbers of team members : {k.num_member}/ Kakao ID of team : {k.kid} \n"

            context.update({'output': output})
            return render(request, 'users/mypage.html', context)

    except ValueError:
        context.update({'error': "아직 등록된 팀이 없습니다."})
        return render(request, 'users/main2.html', context)


def welcome(request):
    context = {}

    if request.POST.get("pw") != request.POST.get("pw2"):
        context.update({"error": "확인 비밀번호가 일치하지 않습니다."})
        return render(request, "users/adduser.html", context)

    if (len(request.POST.get("kid")) == 0) or (len(request.POST.get("id")) == 0) or (
            len(request.POST.get("pw")) == 0):
        context.update({"error": "빈칸없이 입력해주세요."})
        return render(request, "users/adduser.html", context)
    # seam_user = SeamUser()
    # SeamUser.kid = request.POST.get('kid')

    try:
        if request.POST.get("kid") in [i.kid for i in SeamUser.objects.all()]:
            context.update({"error": "가입된 카카오 아이디입니다."})
            return render(request, "users/adduser.html", context)
        else:
            pass
    except OperationalError:
        user = User.objects.create_user(username=request.POST.get('id'), password=request.POST.get('pw'))
        seam_user = SeamUser(user=user)
        seam_user.save()
        return render(request, "users/adduser_success.html", context)

    try:
        user = User.objects.create_user(username=request.POST.get('id'), password=request.POST.get('pw'))
    except IntegrityError:
        context.update({"error": "이미 가입된 학번입니다."})
        return render(request, "users/adduser.html", context)

    seam_user = SeamUser(user=user)

    seam_user.kid = request.POST.get("kid")

    seam_user.save()

    #user.save()
    #seam_user = SeamUser.objects.get(user=user)

    context.update({"SeamUser": seam_user})
    return render(request, 'users/adduser_success.html', context)


def signup(request):
    return render(request, 'users/adduser.html')


def login(request):
    context = {}
    if request.method == 'POST':
        user = auth.authenticate(request, username=request.POST.get('id'), password=request.POST.get('pw'))
        if user is not None:
            auth.login(request, user)
            seam_user = SeamUser.objects.get(user=user)
            context.update({'SeamUser': seam_user})
            return render(request, 'users/main2.html', context)
        else:
            context.update({'error': '학번이나 비밀번호 입력이 잘못되었습니다'})
            return render(request, 'users/login.html', context)

    return render(request, 'users/login.html')


def logout(request):
    auth.logout(request)
    return redirect('users:main')
