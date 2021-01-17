from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.db import OperationalError


def register(request):
    all_lecture = Lecture.objects.all()
    context = {'all_lecture': all_lecture}
    return render(request, "Register_team/choose_option.html", context)


def register_complete(request):
    context = {}

    try:
        if request.POST.get('team_name') in [i.team_name for i in BeforeTeam.objects.all()]:
            context.update({"error": "이미 존재하는 이름입니다. 다른 이름으로 등록해주세요."})
            return render(request, "Register_team/choose_option.html", context)
    except OperationalError:
        pass

    # try:
    #     if request.POST.get('lecture') in [i.name_lecture for i in Lecture.objects.all()]:
    #         pass
    #     else:
    #         context.update({"error": "이번 학기에 열리지 않는 과목입니다."})
    #         return render(request, "Register_team/choose_option.html", context)
    # except OperationalError:
    #     pass

    seam_user = request.user
    seam_user = SeamUser.objects.get(user=seam_user)
    lecture_temp = list(Lecture.objects.filter(name_lecture=request.POST.get('lecture')))[0]
    register_team = BeforeTeam(lecture=lecture_temp)
    register_team.members_ability1 = request.POST.get('members_ability1')
    register_team.kid = seam_user.kid
    register_team.team_name = request.POST.get('team_name')
    register_team.num_member = int(request.POST.get('num_member'))

    if request.POST.get('members_ability1') is 'on':
        register_team.members_ability1 = True
    else:
        register_team.members_ability1 = False

    if request.POST.get('members_ability2') is 'on':
        register_team.members_ability2 = True
    else:
        register_team.members_ability2 = False

    if request.POST.get('members_ability3') is 'on':
        register_team.members_ability3 = True
    else:
        register_team.members_ability3 = False

    if request.POST.get('members_ability4') is 'on':
        register_team.members_ability4 = True
    else:
        register_team.members_ability4 = False

    if request.POST.get('members_ability5') is 'on':
        register_team.members_ability5 = True
    else:
        register_team.members_ability5 = False

    register_team.save()
    context.update({'BeforeTeam': register_team})
    return render(request, 'Register_team/register_complete.html', context)

"""def register_complete(request):
    context = {}

    try:
        user = User.objects.create_user(username=request.POST.get('id'))
    except IntegrityError:
        context.update({"error": "이미 등록된 팀입니다"})
        return render(request, "Register_team/choose_option.html", context)

    before_team = BeforeTeam.objects.get(user=user)
    context.update({"BeforeTeam": before_team})
    user.team_name = request.POST.get("id")
    return render(request, 'Register_team/register_complete.html', context)
    """


def register_result(name_lec):
    team_list = list(BeforeTeam.objects.filter(lecture__name_lecture=name_lec))
    temp = list(Lecture.objects.filter(name_lecture=name_lec))
    temp = temp[0]
    m = temp.num_max
    candidate = [] #혹시 겹칠까봐 set 으로 정의

    #candidate에 인원이 max_num과 max_num-1에 해당하는 가능한 모든 조합을 조합으로 저장 -> 그냥 list 로 진행하도록 변
    for num1, i in enumerate(team_list):
        for num2, j in enumerate(team_list[num1+1:]):
            if (m-1) <= (i.num_member + j.num_member) <= m:
                candidate.append({num1, num1+num2+1}) #두 팀의 조합
            else:
                try:
                    for num3, k in enumerate(team_list[num1+num2+2:]):
                        if num1!=num2 and num2!=num3 and num1!=num3:
                            if (m-1)<=(i.num_member + j.num_member + k.num_member)<=m:
                                candidate.append({num1, num1+num2+1, num1+num2+num3+2}) #세 팀의 조합
                                #네 팀의 조합은 없앰 두 팀 혹은 세 팀만 존재, 네 개의 조합도 필요할까?
                except IndexError:
                    continue

    candidate_2 = []
    for n1, can1 in enumerate(candidate):
        for n2, can2 in enumerate(candidate[n1+1:]):
            if not (can1 & can2):
                candidate_2.append([can1, can2])

    # candidate_2 is the dic which has three teams of which each elements has no same elements
    for n1, can1 in enumerate(candidate):
        for n2, can2 in enumerate(candidate[n1+1:]):
            for n3, can3 in enumerate(candidate[n1+n2+2:]):
                if not ((can1 & can2) or (can1 & can3) or (can2 & can3)):
                    candidate_2.append([n1, n1+n2+1, n1+n2+n3+2])

    if len(candidate_2)<=1:
        candidate_3 = [j for i in candidate_2 for j in i]
        # candidate_3 is a list with set elements
        return candidate_3


    # BeforeTeam 객체를 score 에 담기([[]], 이중리스)
    # score = [[team_list[elem].members_ability1 for u in teams for elem in u] for teams in candidate_2]

    score = []
    for teams in candidate_2:
        to_select = []
        for elem in teams:
            score_1 = []
            score_2 = []
            score_3 = []
            score_4 = []
            score_5 = []
            for u in elem:
                score_1.append(team_list[u].members_ability1)
                score_2.append(team_list[u].members_ability2)
                score_3.append(team_list[u].members_ability3)
                score_4.append(team_list[u].members_ability4)
                score_5.append(team_list[u].members_ability5)
            if sum(score_1)>0:
                score_1 = 1
            else:
                score_1 = 0
            if sum(score_2)>0:
                score_2 = 1
            else:
                score_2 = 0
            if sum(score_3)>0:
                score_3 = 1
            else:
                score_3 = 0
            if sum(score_4) > 0:
                score_4 = 1
            else:
                score_4 = 0
            if sum(score_5) > 0:
                score_5 = 1
            else:
                score_5 = 0

            t_score = score_1 + score_2 + score_3 + score_4 + score_5
            to_select.append(t_score)

        # calculate the difference of ability among the teams. the least different combination(optimal combination, balanced combination) should be selected.
        score.append(sum(to_select))

    final = score.index(max(score))
    candidate_3 = candidate_2[final]

    # candidate_3 is a list with set elements
    return candidate_3
