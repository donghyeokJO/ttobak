import json
import bcrypt
import jwt
import random
import requests
import time
import datetime
import math

from .models  import User,Student,UsrStu,StuIc,Icon,TestMaster,StuTest,CureMaster,StuCure,StuCurrent,TestIdx,CureIdx,ComCure,TestCurrent,Voice,StuStatus
from . import serializers as sz

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from django.db.models import Q,Avg


class MakeUser(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        
        if User.objects.filter(usr_email=data['email']).exists():
            return JsonResponse({"message":"이미 존재하는 이메일 입니다.","code":2},status=200)

        User.objects.create(
            usr_name=data['name'],
            usr_email=data['email'],
            usr_pw= bcrypt.hashpw(data['pw'].encode("UTF-8"),bcrypt.gensalt()).decode("UTF-8")
        ).save()

        user = User.objects.latest('usr_id')


        return JsonResponse({"message":"성공적으로 회원가입 되었습니다.","u_id":user.usr_id,"code":1},status=200)



class LogIn(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)

        if not 'email' in data:
            return JsonResponse({"message":"이메일을 입력해주세요","code":4},status=200)

        if User.objects.filter(usr_email=data['email']).exclude(activated='F').exists():
            user = User.objects.get(usr_email=data['email'])

            if bcrypt.checkpw(data['pw'].encode("UTF-8"),user.usr_pw.encode("UTF-8")):
                return JsonResponse({"u_id":user.usr_id,"code":1},status=200)

            return JsonResponse({"message":"비밀번호가 일치하지 않습니다.","code":2},status=200)

        return JsonResponse({"message":"가입된 메일 주소가 존재하지 않습니다.","code":3},status=200)

class UserModify(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        uk = data['u_id']

        if User.objects.filter(usr_id = uk).exclude(activated='F').exists():
            user = User.objects.get(usr_id=uk)

            if user.usr_email != data['email']:
                if User.objects.filter(usr_email = data['email']).exists():
                    return JsonResponse({"message":"이미 존재하는 이메일입니다.","code":2},status=200)
            
            user.usr_email = data['email']
            user.usr_pw = bcrypt.hashpw(data['pw'].encode("UTF-8"),bcrypt.gensalt()).decode("UTF-8")
            user.usr_name = data['name'] 
            user.save()

            return JsonResponse({"message":"변경사항이 저장되었습니다.","code":1},status=200)

        return JsonResponse({"message":"존재하지 않는 회원입니다","code":3},status=200)

class UserDelete(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        uk = data['u_id']

        if User.objects.filter(usr_id = uk).exists():
            user = User.objects.get(usr_id=uk)
            user.usr_email = uk
            user.usr_name = ''
            user.usr_pw = ''
            user.activated = 'F'
            user.save()
            return JsonResponse({"message":"성공적으로 삭제되었습니다.","code":1},status=200)
        return JsonResponse({"message":"존재하지 않는 회원입니다.","code":2},status=200)

class UserGet(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        uk = data['u_id']

        if User.objects.filter(usr_id = uk).exists():
            user = User.objects.get(usr_id=uk)
            student = []
            sids = []
            if UsrStu.objects.filter(usr_id = uk).exists():
                usrstu = UsrStu.objects.filter(usr_id = uk)
                if usrstu.count() == 1 :
                    sid = Student.objects.get(stu_id = usrstu[0].stu_id)
                    if not sid.activated == 'F':
                        sdat = sz.StudentSerializer(instance = sid)
                        student.append(sdat.data)
                else :
                    for u in usrstu:
                        sids.append(u.stu_id)
                    for s in sids:
                        stu = Student.objects.get(pk=s)
                        if not stu.activated == 'F':
                            student.append(stu)
                    sdat = sz.StudentSerializer(data=student,many=True)
                    sdat.is_valid()
                    student = sdat.data
            return JsonResponse({"u_id":user.usr_id,"name":user.usr_name,"email":user.usr_email,"code":1,"students":student},status=200)

        return JsonResponse({"message":"존재하지 않는 회원입니다.","code":2},status=200)

class StuAdd(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        uk = data['u_id']

        if User.objects.filter(usr_id = uk).exists():
            user = User.objects.get(pk = uk)
            icon = Icon.objects.get(pk = data['ic_id'])
            cnt = 0 
            stucnt = UsrStu.objects.filter(usr_id = uk)
            for s in stucnt:
                stu_id = s.stu_id
                if Student.objects.get(pk=stu_id).activated != 'F':
                    cnt +=1
            
            if cnt > 3:
                return JsonResponse({"message":"학습자는 3명까지만 추가할 수 있습니다.","code":3},status=200)
            Student.objects.create(
                stu_name = data['name'],
                stu_birth = data['birth'],
                stu_gender = data['gender'],
                ic = icon
            ).save()
            stu = Student.objects.latest('stu_id')
            UsrStu.objects.create(
                usr = user,
                stu = stu
            )
            

            # StuIc.objects.create(
            #     stu = Student.objects.latest('stu_id'),
            #     ic = icon
            # )

            return JsonResponse({"message":"성공적으로 추가되었습니다.","s_id":stu.stu_id,"code":1},status=200)

        return JsonResponse({"message":"존재하지 않는 회원입니다.","code":2},status=200)

class StuModify(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        uk = data['u_id']
        sk = data['s_id']

        if User.objects.filter(usr_id = uk).exists():
            if Student.objects.filter(stu_id = sk).exclude(activated = 'F').exists():
                student = Student.objects.get(pk=sk)
                # icon = Icon.objects.get(pk=ic_id)
                # stu_ic = StuIc.objects.get(stu_id=sk)
                student.stu_name = data['name']
                student.stu_birth = data['birth']
                student.stu_gender = data['gender']
                student.ic_id = data['ic_id']

                student.save()

                return JsonResponse({"message":"성공적으로 수정되었습니다.","code":1},status=200)
            return JsonResponse({"message":"존재하지 않는 학습자 입니다.","code":2},status=200)
        return JsonResponse({"message":"존재하지 않는 회원입니다.","code":3},status=200)


class StuDel(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        uk = data['u_id']
        sk = data['s_id']
        
        if User.objects.filter(usr_id=uk).exists():
            if Student.objects.filter(stu_id = sk).exists():
                student = Student.objects.get(pk=sk)
                student.stu_name = ''
                # student.stu_birth = ''
                student.activated = 'F'
                student.save()
                return JsonResponse({"message":"성공적으로 삭제되었습니다.","code":1},status=200)
            return JsonResponse({"message":"존재하지 않는 학습자입니다.","code":2},status=200)
        return JsonResponse({"message":"존재하지 않는 회원입니다.","code":3},status=200)

class StuGet(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        uk = data['u_id']
        sk = data['s_id']

        if User.objects.filter(usr_id = uk).exclude(activated='F').exists():
            if Student.objects.filter(stu_id=sk).exclude(activated='F').exists():

                student = Student.objects.get(pk=sk)

                return JsonResponse({"s_id":student.stu_id,"name":student.stu_name,"birth":student.stu_birth,"gender":student.stu_gender,"ic_id":student.ic_id,"code":1,},status=200)
            return JsonResponse({"message":"존재하지 않는 학습자 입니다.","code":2},status=200)
        return JsonResponse({"message":"존재하지 않는 회원입니다.","code":3},status=200)

class TestGet(View):
    def make_swp_answer(self):
        answer = []
        for i in range(5):
            tmp = []
            ans1 = "up"
            ans2 = "up"
            x = random.randint(1,2)
            y = random.randint(1,2)
            if x == 1:
                ans1 = "down"
            if y == 1:
                ans2 = "down"
            tmp.append(ans1)
            tmp.append(ans2)
            answer.append(tmp)
        return answer
        
    def get_ph(self):
        idx_id = 2
        ques_int = random.randint(1,4)
        phs = TestMaster.objects.filter(test_idx = 2,ques_int = ques_int)
        
        phs_data = sz.PhSerializer(data = phs,many=True)
        start_id = phs[0].ques_id
        ids = [] 
        for i in range(50):
            ids.append(start_id + i)
        phs_data.is_valid()
        answer_set = []
        used = []
        ph1 = random.choice(ids)
        ph2 = random.choice(ids)
        for i in range(25):
            tmp = []
            while ph1== ph2 or ph1 in used or ph2 in used:
                ph1 = random.choice(ids)
                ph2 = random.choice(ids)
            if random.randint(1,2)==1:
                ans = ph1
            else:
                ans = ph2
            tmp.append(ph1)
            tmp.append(ph2)
            tmp.append(ans)
            used.append(ph1)
            used.append(ph2)
            answer_set.append(tmp)
            # print(answer_set)
        return phs_data.data,answer_set

    def get_foc(self,testcur):
        focus_lev = testcur.focus_lev
        qids = []
        qid = random.randint(1,10)
        for i in range(5):
            while qid in qids:
                qid = random.randint(1,10)
            qids.append(qid)
        focs = []
        for idx,q in enumerate(qids):
            foc = TestMaster.objects.get(test_idx =3,ques_level = focus_lev + idx , ques_int = q )
            focs.append(foc)
        foc_data = sz.FocSerializer(data = focs,many=True)
        foc_data.is_valid()
        return foc_data.data

    def get_tutorial(self,idx_txt):
        if idx_txt == 'swp':
            voice = []
            desc = [1,2,3,4]
            for d in desc:
                voc = Voice.objects.get(pk = d)
                voice.append(voc)
            vdat = sz.VoiceSerializer(data=voice,many = True)
            swp = TestMaster.objects.get(ques_id = 71)
            sdat = sz.SwpSerializer(instance = swp)
            vdat.is_valid()
            return vdat.data, sdat.data
        elif idx_txt == 'ph':
            voice = []
            desc = [5,37,21]
            for d in desc:
                voc = Voice.objects.get(pk = d)
                voice.append(voc)
            vdat = sz.VoiceSerializer(data=voice,many = True)
            ph = TestMaster.objects.filter(Q(ques_id = 84)| Q(ques_id=85))
            sdat = sz.PhSerializer(data = ph,many=True)
            vdat.is_valid()
            sdat.is_valid()
            return vdat.data, sdat.data
        elif idx_txt == 'foc':
            voice = []
            desc = [6,22,35,7]
            for d in desc:
                voc = Voice.objects.get(pk = d)
                voice.append(voc)
            vdat = sz.VoiceSerializer(data=voice,many = True)
            foc = TestMaster.objects.get(ques_id = 534)
            sdat = sz.PhSerializer(instance = foc)
            vdat.is_valid()
            return vdat.data, sdat.data

    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        s_id = data['s_id']
        if Student.objects.filter(pk=s_id).exists():
            student = Student.objects.get(pk=s_id)
            if not TestCurrent.objects.filter(stu_id = s_id).exists():
                TestCurrent.objects.create(
                    stu = student,
                    swp_freq = 500,
                    swp_lev = 1,
                    focus_lev = 1,
                    swp_passed = 0,
                    swp_did = 0,
                    focus_passed = 0,
                    focus_did = 0
                ).save()
            testcur = TestCurrent.objects.get(stu_id = s_id)
            idx_txt = data['idx_txt']
            if not StuTest.objects.filter(stu_id = s_id , test_txt = idx_txt).exists():
                # StuTest.objects.create(
                #     stu = student,
                #     test_txt = idx_txt
                # ).save()
                voice , sample_ques = self.get_tutorial(idx_txt)
                return JsonResponse({"voice":voice,"sample_ques":sample_ques,"code":"tutorial"},status=200)
            if TestIdx.objects.filter(idx_txt = idx_txt):
                idx_id = TestIdx.objects.get(idx_txt = idx_txt).idx_id
                if idx_id == 1:
                    swp = TestMaster.objects.get(ques_int = testcur.swp_freq,ques_level = testcur.swp_lev,test_idx = idx_id)
                    swp = sz.SwpSerializer(instance=swp)
                    answer = self.make_swp_answer() 
                    return JsonResponse({"swp":swp.data,"answers":answer,"code":1},status=200)
                if idx_id == 2:
                    ph_data ,answer = self.get_ph()
                    return JsonResponse({"phs":ph_data,"answers":answer,"code":1},status=200)
                if idx_id == 3:
                    focus = self.get_foc(testcur)
                    return JsonResponse({"focus":focus,"code":1},status=200)
            return JsonResponse({"message":"해당 학습이 존재하지 않습니다.","code":2},status=200)
        return JsonResponse({"message":"해당 학습자가 없습니다.","code":3},status=200)

class TestAns(View):
    def ans_swp(self,student,data,idx_id,swp):
        testcur = TestCurrent.objects.get(stu_id = student.stu_id)
        ori_ans1 = data['ori_answer1']
        ori_ans2 = data['ori_answer2']
        stu_ans1 = data['stu_answer1']
        stu_ans2 = data['stu_answer2']
        is_correct = 'F'
        is_review = data['is_review']
        if ori_ans1 == stu_ans1 and ori_ans2 == stu_ans2:
            is_correct = 'T'
            testcur.swp_passed += 1
            testcur.save()
        to_next_level = False
        to_next_freq = False
        StuTest.objects.create(
            stu = student,
            ques = swp,
            is_correct = is_correct,
            is_review = is_review,
            test_txt = 'swp',
        ).save()
        testcur.swp_did += 1
        testcur.save()
        if testcur.swp_did == 5:
            if testcur.swp_passed >=4:
                if TestMaster.objects.filter(ques_level = testcur.swp_lev+1,ques_int = testcur.swp_freq).exists():
                    to_next_level = True
                    testcur.swp_lev += 1
                    testcur.swp_did = 0
                    testcur.swp_passed = 0
                    testcur.save()
                elif TestMaster.objects.filter(ques_level = 1, ques_int = testcur.swp_freq*2 ).exists():
                    to_next_level = True
                    to_next_freq = True
                    testcur.swp_lev = 1
                    testcur.swp_freq = testcur.swp_freq* 2
                    testcur.swp_did = 0
                    testcur.swp_passed = 0
                    testcur.save()
                else :
                    testcur.swp_did = 0
                    testcur.swp_passed = 0 
                    testcur.save()
                    to_next_level = "모든 단계를 풀었습니다."
            else:
                if TestMaster.objects.filter(ques_level = 1, ques_int = testcur.swp_freq*2).exists():
                    to_next_freq = True
                    testcur.swp_lev = 1
                    testcur.swp_freq = testcur.swp_freq * 2
                    testcur.swp_did = 0
                    testcur.swp_passed = 0
                    testcur.save()
                else : 
                    to_next_level = "모든 단계를 풀었습니다."
        return is_correct,to_next_level,to_next_freq

    def ans_ph(self,student,data,idx_id,ph1,ph2):
        stu_answer = data['stu_answer']
        ori_answer = data['ori_answer']
        is_review = data['is_review']
        is_correct = 'F'
        if stu_answer == ori_answer:
            is_correct = 'T'
        StuTest.objects.create(
            stu = student,
            ques = ph1,
            ques2 = ph2,
            test_txt = 'ph',
            is_review = is_review,
            is_correct = is_correct
        ).save()
        return is_correct 

    def ans_foc(self,student,data,idx_id,foc):
        testcur = TestCurrent.objects.get(stu_id = student.stu_id)
        score = data['full_score']
        phone_score = data['phone_score']
        speed_score = data['speed_score']
        rhythm_score = data['rhythm_score']
        is_review = data['is_review']
        is_pass = False
        if score >= 80:
            is_pass = True
            testcur.focus_passed += 1
        StuTest.objects.create(
            stu = student,
            ques = foc,
            full_score = score,
            phone_score = phone_score,
            speed_score = speed_score,
            rhythm_score = rhythm_score,
            is_review = is_review,
            test_txt = 'foc'
        ).save()
        to_next_level = False
        is_stop =  False
        testcur.focus_did += 1
        testcur.save()
        if testcur.focus_did == 5 :
            if testcur.focus_passed >= 4:
                to_next_level = True
                if TestMaster.objects.filter(ques_level = testcur.focus_lev + 5, test_idx = 3).exists():
                    testcur.focus_lev += 5
                    testcur.focus_did = 0
                    testcur.focus_passed = 0
                    testcur.save()
                else :
                    to_next_level = "모든 문제를 학습했습니다"
                    is_stop = True
            else :
                is_stop = True
                if testcur.focus_lev != 1:
                    testcur.focus_lev -= 5
                    testcur.save()
        return is_pass, to_next_level , is_stop
            
    def ans_tutorial(self,student,idx_txt):
        StuTest.objects.create(
            stu = student,
            test_txt = idx_txt
        ).save
        return True

    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        s_id = data['s_id']
        if Student.objects.filter(pk=s_id).exists():
            student = Student.objects.get(stu_id = s_id)
            idx_txt = data['idx_txt']
            if TestIdx.objects.filter(idx_txt = idx_txt).exists():
                idx_id = TestIdx.objects.get(idx_txt=idx_txt).idx_id
                if 'tutorial' in data:
                    is_okay = self.ans_tutorial(student,idx_txt)
                    return JsonResponse({"is_okay":is_okay,"code":1},status = 200)
                ques_id = data['ques_id']
                if idx_id == 1:
                    swp = TestMaster.objects.get(pk = ques_id)
                    is_correct ,  to_next_level, to_next_freq  = self.ans_swp(student,data,idx_id,swp)
                    return JsonResponse({"is_correct":is_correct,"to_next":to_next_level,"to_next_freq":to_next_freq,"code":1},status=200)
                if idx_id == 2:
                    ques_id2 = data['ques_id2']
                    ph1 = TestMaster.objects.get(pk = ques_id)
                    ph2 = TestMaster.objects.get(pk = ques_id2)
                    is_correct = self.ans_ph(student,data,idx_id,ph1,ph2)
                    return JsonResponse({"is_correct":is_correct,"code":1},status = 200)
                if idx_id == 3:
                    foc = TestMaster.objects.get(pk = ques_id)
                    is_pass, to_next_level , is_stop = self.ans_foc(student,data,idx_id,foc)
                    return JsonResponse({"is_pass":is_pass,"to_next_level":to_next_level,"is_stop":is_stop,"code":1},status=200)
            else:
                return JsonResponse({"message":"해당하는 검사가 존재하지 않습니다.","code":2},status=200)
        else :
            return JsonResponse({"message":"해당 학습자가 존재하지 않습니다.","code":3},status=200)

class TestProceed(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        s_id = data['s_id']
        is_okay = False
        if Student.objects.filter(pk=s_id).exists():
            student = Student.objects.get(pk=s_id)
            if StuStatus.objects.filter(stu_id = s_id).exists():
                today = datetime.datetime.now()
                # today = datetime.datetime(2020,11,7)
                recent = StuStatus.objects.get(stu_id = s_id)
                recent = recent.date
                point  = today + datetime.timedelta(weeks = -1)
                point = point.date()
                if point >= recent:
                    is_okay = True
            else:
                is_okay = True
            return JsonResponse({"is_okay":is_okay,"code":1},status=200)
        else:
            return JsonResponse({"message":"해당 학습자가 존재하지 않습니다.","code":2},status=200)

class TestResult(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        s_id = data['s_id']
        if Student.objects.filter(pk=s_id).exists():
            student = Student.objects.get(pk=s_id)
            results ={}
            swp = {}
            ph = {}
            foc = {}
            if StuTest.objects.filter(stu=student,is_review='F').exists():
                date = StuTest.objects.filter(stu=student,is_review='F').order_by('-date')[0].date
                if StuTest.objects.filter(stu=student,date = date,is_review='F').exists():
                    results['총 문제 개수'] = StuTest.objects.filter(stu=student,date=date,is_review='F').count()
                    results['총 맞은 개수'] = StuTest.objects.filter(stu=student,date=date,is_review='F',is_correct='T').count()
                    swp['총 문제 개수'] = StuTest.objects.filter(stu=student,date=date,test_txt='swp',is_review='F').count()
                    swp['맞은 개수'] = StuTest.objects.filter(stu=student,date=date,test_txt='swp',is_review='F',is_correct ='T').count()
                    ph ['총 문제 개수'] = StuTest.objects.filter(stu=student,date=date,test_txt='ph',is_review='F').count()
                    ph['맞은 개수'] = StuTest.objects.filter(stu=student,date=date,test_txt='ph',is_review='F',is_correct='T').count()
                    foc['총 문제 개수'] = StuTest.objects.filter(stu=student,date=date,test_txt='foc',is_review='F').count()
                    foc['평균 발음 정확도'] = StuTest.objects.filter(stu=student,date=date,test_txt='foc').aggregate(Avg('full_score'))['full_score__avg']
                    results['청각처리속도'] = swp
                    results['음운청취력'] = ph
                    results['선택적집중력'] = foc
                    levels = [1,1,1]
                    slevels = [1,1,1]
                    every_swp = StuTest.objects.filter(stu=student,test_txt = 'swp',is_correct = 'T',date=date,is_review='F')
                    if every_swp.count() ==0:
                        levels[1] = 1
                    for s in every_swp:
                        sw = TestMaster.objects.get(pk=s.ques_id)
                        freq = sw.ques_int
                        if freq == 500:
                            if slevels[0] <= sw.ques_level +1:
                                slevels[0] = sw.ques_level +1
                        elif freq == 1000:
                            if slevels[1] <= sw.ques_level +1:
                                slevels[1] = sw.ques_level +1
                        elif freq == 2000:
                            if slevels[2] <= sw.ques_level +1:
                                slevels[2] = sw.ques_level +1
                    levels[0] = min(slevels)
                    every_ph = StuTest.objects.filter(stu=student,test_txt = 'ph',date=date,is_review='F')
                    c_ph = len([p for p in every_ph if p.is_correct == 'T'])
                    pscore = (c_ph/25) * 100
                    if pscore >= 96:
                        levels[1]= 6
                    elif pscore >= 86:
                        levels[1] =5
                    elif pscore >= 70:
                        levels[1] = 4
                    elif pscore >= 50:
                        levels[1] = 3
                    elif pscore >= 33:
                        levles[1] = 2
                    levels[2] = math.ceil(TestCurrent.objects.get(stu = student).focus_lev/5) +1
                    tot_lev = min(levels)
                    if tot_lev >=5:
                        status = '경미'
                    elif tot_lev >=3:
                        status = '저위험군'
                    elif tot_lev >=1:
                        status = '고위험군'
                    results['status'] = status
                    if StuStatus.objects.filter(stu_id = s_id).exists():
                        stustat = StuStatus.objects.get(stu_id = s_id)
                        stustat.status = status
                        stustat.save()
                    else:
                        StuStatus.objects.create(
                            stu = student,
                            status = status
                        ).save()
            return JsonResponse({"results":results,"code":1},status=200)
        else:
            return JsonResponse({"message":"해당 학습자가 존재하지 않습니다.","code":2},status=200)

class Testdid(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        s_id = data['s_id']
        if Student.objects.filter(stu_id = s_id).exists():
            student = Student.objects.get(pk=s_id)
            is_first = True
            if StuStatus.objects.filter(stu_id = s_id).exists():
                is_first = False
            else:
                if StuTest.objects.filter(stu_id = s_id).exists():
                    stucur = TestCurrent.objects.get(stu_id = s_id)
                    stucur.swp_freq = 500
                    stucur.swp_lev = 1
                    stucur.focus_lev= 1
                    stucur.swp_passed = 0
                    stucur.swp_did = 0
                    stucur.focus_passed = 0
                    stucur.focus_did = 0
                    stucur.save()
            return JsonResponse({"is_first":is_first,"code":1},status=200)
        else:
            return JsonResponse({"message":"해당 학습자가 존재하지 않습니다.","code":2},status=200)

class TestReset(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        s_id = data['s_id']
        idx_txt = data['idx_txt']
        if Student.objects.filter(stu_id = s_id).exists():
            student = Student.objects.get(pk = s_id)
            if StuTest.objects.filter(stu_id = s_id,test_txt = idx_txt).exists():
                StuTest.objects.filter(stu_id=s_id,test_txt = idx_txt).delete()
                return JsonResponse({"reset":True,"code":1},status=200)
            return JsonResponse({"message":"학습 기록이 존재하지 않습니다.","code":2},status=200)
        return JsonResponse({"message":"해당 학습자가 존재하지 않습니다.","code":3},status=200)


class CureGet(View):

    def get_read(self,read_idx,p_id,read_level):
        if CureMaster.objects.filter(pk = p_id).exists():
            t_id = CureMaster.objects.get(pk=p_id).cure_tid
            reads = CureMaster.objects.filter(cure_tid=t_id,cure_idx=read_idx,cure_level=read_level)
            read_data = sz.ReadSerializer(data = reads,many=True)
            read_data.is_valid()
            read_data = read_data.data
            voice = []
            desc = [9]
            for d in desc:
                voc = Voice.objects.get(pk = d)
                voice.append(voc)
            vdat = sz.VoiceSerializer(data=voice,many = True)
            vdat.is_valid()
            return read_data,vdat.data
        else:
            return "더 이상 치료가 존재하지 않습니다.", ''
    
    def get_review(self,s_id):
        return 1

    def get_specified(self,s_id,idx_txt):
        idx_id = CureIdx.objects.get(idx_txt = idx_txt).idx_id
        
        answer = []
        level = 1
        if idx_id == 4:
            level = random.randint(1,3)
            cures = list(ComCure.objects.filter(com_level = level))
            rand_cures = random.sample(cures,10)
            s_cures = self.serialized(rand_cures,idx_id)
        elif idx_id == 1 or idx_id == 11:
            level = random.randint(1,3)
            tid = random.randint(1,20)
            cures = list(CureMaster.objects.filter(cure_idx=idx_id,cure_level=level,cure_tid = tid))
            s_cures = self.serialized(cures,idx_id)
        elif idx_id != 7:
            cures = list(CureMaster.objects.filter(cure_idx = idx_id))
            rand_cures = random.sample(cures,10)
            s_cures = self.serialized(rand_cures,idx_id)
        if idx_id == 7 :
            cures = CureMaster.objects.filter(cure_idx = idx_id)
            cnt = cures.count()
            s_cures,answer = self.make_answer(7,cnt,1)
            s_cures = self.serialized(s_cures,7)
        s_cures.is_valid()
        return s_cures.data,answer,level

    def serialized(self,data,curr_idx):
        cure_serializer = {
            1 : sz.ReadSerializer(data=data,many=True),
            2 : sz.ReadSerializer(data=data,many=True),
            3 : sz.CountSerializer(data=data,many=True),
            4 : sz.CommonSerializer(data= data,many=True),
            5 : sz.CountSerializer(data=data,many=True),
            6 : sz.VowelsoundSerializer(data=data,many=True),
            7 : sz.ConsomatchSerializer(data=data,many=True),
            8 : sz.ConsocommonSerializer(data=data,many=True),
            9 : sz.CountSerializer(data=data,many=True),
            10 : sz.ConsosoundSerializer(data=data,many=True),
            11 : sz.ReadSerializer(data=data,many=True),
            12 : sz.ReadSerializer(data=data,many=True),
        }
        return cure_serializer[curr_idx]
    
    def make_answer(self,curr_idx,cnt,curr_level):
        answer = []
        ans_list = []
        if curr_idx == 7 :
            for i in range(10):
                tmp = []
                k = random.randrange(cnt)
                for i in range(3):
                    while k in tmp:
                        k = random.randrange(cnt)
                    tmp.append(k)
                    if k not in ans_list:
                        ans_list.append(k)
                ans = random.sample(tmp,1)
                tmp.append(ans)
                answer.append(tmp)
            
            cure = []
            cures = CureMaster.objects.filter(cure_idx = curr_idx,cure_level = curr_level)
            for a in ans_list:
                a = int(a)
                cure.append(cures[a])
            return cure,answer
                
    def get_cure(self,curr_idx,curr_level):
        answer = [] 
        if curr_idx == 4:
            if ComCure.objects.filter(com_level=curr_level).exists():
                Cures = list(ComCure.objects.filter(com_level=curr_level))
                rand_cures = random.sample(Cures,10)
                cures = sz.CommonSerializer(data=rand_cures,many=True)
                cures.is_valid()
                return cures.data,answer
            else:
                return "해당하는 문제가 존재하지 않습니다."
        if CureMaster.objects.filter(cure_idx = curr_idx,cure_level = curr_level).exists():
           Cures = list(CureMaster.objects.filter(cure_idx=curr_idx,cure_level = curr_level))
           rand_cures = Cures
           if len(Cures) > 10:
               rand_cures = random.sample(Cures,10)
           if curr_idx == 7 :
               cnt = len(Cures)
               rand_cures , answer = self.make_answer(curr_idx,cnt,curr_level)
           cures = self.serialized(rand_cures,curr_idx)
           cures.is_valid()
           return cures.data,answer

    def get_tutorial(self,student,idx_txt):
        idx_id = CureIdx.objects.get(idx_txt = idx_txt).idx_id
        voices = []
        if idx_id == 1:
            sound = [9,35,40,38,34]
            for s in sound:
                voices.append(Voice.objects.get(pk=s))
            sdat = sz.VoiceSerializer(data=voices,many=True)
            sdat.is_valid()
            # sample_ques = CureMaster.objects.get(pk=1259)
            # sample_ques = sz.CountSerializer(instance=sample_ques)
            return sdat.data
        if idx_id == 11:
            sound = [35,40,38,34]
            for s in sound:
                voices.append(Voice.objects.get(pk=s))
            sdat = sz.VoiceSerializer(data=voices,many=True)
            sdat.is_valid()

            return sdat.data
        if idx_id == 3:
            sound = [10,11,12]
            for s in sound:
                voices.append(Voice.objects.get(voc_id = s))
            sdat = sz.VoiceSerializer(data=voices,many=True)
            sdat.is_valid()
            sample_ques = CureMaster.objects.get(pk=1916)
            sample_ques = sz.CountSerializer(instance = sample_ques)
            return sdat.data,sample_ques.data
        if idx_id == 5:
            sound = [10,22,35,40,38,23]
            for s in sound:
                voices.append(Voice.objects.get(voc_id=s))
            sdat = sz.VoiceSerializer(data=voices,many = True)
            sdat.is_valid()
            sample_ques = CureMaster.objects.get(pk=1948)
            sample_ques = sz.CountSerializer(instance = sample_ques)
            return sdat.data,sample_ques.data
        if idx_id == 6:
            sound = [10,24,25]
            for s in sound:
                voices.append(Voice.objects.get(voc_id=s))
            sdat = sz.VoiceSerializer(data=voices,many=True)
            sdat.is_valid()
            sample_ques = CureMaster.objects.get(pk = 2083)
            sample_ques = sz.VowelsoundSerializer(instance = sample_ques)
            return sdat.data,sample_ques.data
        if idx_id == 7:
            sound = [10,26,41]
            for s in sound:
                voices.append(Voice.objects.get(voc_id=s))
            sdat = sz.VoiceSerializer(data=voices,many=True)
            sdat.is_valid()
            ques = [2246,2247,2248]
            sample_ques = []
            for q in ques:
                sample_q = CureMaster.objects.get(pk=q)
                sample_ques.append(sample_q)
            sample_ques = sz.ConsomatchSerializer(data = sample_ques,many=True)
            sample_ques.is_valid()
            return sdat.data, sample_ques.data
        if idx_id == 8:
            sound = [27,28]
            for s in sound:
                voices.append(Voice.objects.get(voc_id=s))
            sdat = sz.VoiceSerializer(data=voices,many=True)
            sdat.is_valid()
            sample_ques = CureMaster.objects.get(pk=4317)
            sample_ques = sz.ConsocommonSerializer(instance = sample_ques)
            return sdat.data,sample_ques.data
        if idx_id ==9:
            sound = [29,35,40,38,30]
            for s in sound:
                voices.append(Voice.objects.get(voc_id=s))
            sdat = sz.VoiceSerializer(data=voices,many=True)
            sdat.is_valid()
            sample_ques = CureMaster.objects.get(pk=2724)
            sample_ques = sz.ConsocommonSerializer(instance = sample_ques)
            return sdat.data,sample_ques.data
        if idx_id == 10:
            sound = [10,31,32]
            for s in sound:
                voices.append(Voice.objects.get(voc_id=s))
            sdat = sz.VoiceSerializer(data=voices,many=True)
            sdat.is_valid()
            sample_ques = CureMaster.objects.get(pk=3046)
            sample_ques = sz.ConsosoundSerializer(instance = sample_ques)
            return sdat.data,sample_ques.data
            

    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        s_id = data['s_id']
        if Student.objects.filter(pk=s_id).exists():
            student = Student.objects.get(pk=s_id)
            if 'idx_txt' in data:
                idx_txt = data['idx_txt']
                code = 1
                if idx_txt == 'review':
                    read, cure, answer = self.get_review(s_id)
                    return JsonResponse({"read":read,"cure":cure,"answer":answer,"code":"review"},status=200)
                else:
                    if idx_txt == 'poem':
                        tutorial = self.get_tutorial(student,idx_txt)
                        cure,answer,level = self.get_specified(s_id,idx_txt)
                        return JsonResponse({"cure":cure,"answer":answer,"read_voice":tutorial,"code":"specified"},status=200)
                    if idx_txt == "selfpoem":
                        tutorial = self.get_tutorial(student,idx_txt)
                        cure,answer,level = self.get_specified(s_id,idx_txt)
                        return JsonResponse({"cure":cure,"read_voice":tutorial,"code":"specified"},status=200)
                    cure, answer,level = self.get_specified(s_id,idx_txt)
                    tutorial , sample_ques = [],[]
                    if idx_txt == "common":
                        voices = []
                        if level == 1:
                            if not StuCure.objects.filter(stu_id = s_id,com_cure__com_id__range=(61,80)).exists():
                                sound = [13,14,12]
                                for s in sound:
                                    voices.append(Voice.objects.get(pk=s))
                                sdat = sz.VoiceSerializer(data=voices,many=True)
                                sdat.is_valid()
                                sample_ques = ComCure.objects.get(pk = 61)
                                sample_ques = sz.CommonSerializer(instance=sample_ques).data
                                tutorial = sdat.data
                                code = "tutorial"
                        elif level == 2:
                            if not StuCure.objects.filter(stu_id = s_id,com_cure__com_id__range=(81,100)).exists():
                                sound = [16,17,18]
                                for s in sound:
                                    voices.append(Voice.objects.get(pk=s))
                                sdat = sz.VoiceSerializer(data=voices,many=True)
                                sdat.is_valid()
                                sample_ques = ComCure.objects.get(pk = 81)
                                sample_ques = sz.CommonSerializer(instance=sample_ques).data
                                tutorial = sdat.data
                                code = "tutorial"
                        elif level == 3:
                            if not StuCure.objects.filter(stu_id = s_id,com_cure__com_id__range=(101,120)).exists():
                                sound = sound = [19,20,21]
                                for s in sound:
                                    voices.append(Voice.objects.get(pk=s))
                                sdat = sz.VoiceSerializer(data=voices,many=True)
                                sdat.is_valid()
                                sample_ques = ComCure.objects.get(pk = 101)
                                sample_ques = sz.CommonSerializer(instance=sample_ques).data
                                tutorial = sdat.data
                                code = "tutorial"
                        return JsonResponse({"cure":cure,"answer":answer,"tut_voice":tutorial,"sample_ques":sample_ques,"code":code},status=200)
                    else:    
                        if not StuCure.objects.filter(stu_id = s_id , cure_txt = idx_txt).exists():
                            tutorial , sample_ques = self.get_tutorial(student,idx_txt)
                            code = "tutorial"
                        return JsonResponse({"cure":cure,"answer":answer,"tut_voice":tutorial,"sample_ques":sample_ques,"code":code},status=200)
            if not StuCurrent.objects.filter(stu_id = s_id).exists():
                if not StuStatus.objects.filter(stu_id = s_id).exists():
                    # return JsonResponse({"message":"검사를 먼저 진행해주세요","code":3},status=200)
                    curr = 'count'
                else:
                    status = StuStatus.objects.get(stu_id = s_id).status
                    if status == '고위험군':
                        curr = 'count'
                    elif status == '저위험군':
                        curr = 'vowelword'
                    else :
                        curr = 'consosword'
                StuCurrent.objects.create(
                    stu = student,
                    cur_read = 'poem',
                    read_level = 1,
                    curr_level = 1,
                    cur_read_id = 1259,
                    cur_curr = curr,
                    cur_curr_last1 = 0,
                    cur_curr_last2 = 0,
                    cur_curr_last3 = 0
                ).save()
            stucur = StuCurrent.objects.get(stu_id=s_id)
            read_idx = CureIdx.objects.get(idx_txt=stucur.cur_read).idx_id
            read_id = stucur.cur_read_id
            read_level = stucur.read_level
            read, read_voice = self.get_read(read_idx,read_id,read_level)
            code = 1
            tut_voice = []
            sample_ques = []
            if stucur.cur_curr == 'common':
                sound = []
                voices = []
                if stucur.curr_level == 1:
                    if not StuCure.objects.filter(stu_id = s_id,com_cure__com_id__range=(61,80)).exists():
                        sound = [13,14,12]
                        for s in sound:
                            voices.append(Voice.objects.get(pk=s))
                        sdat = sz.VoiceSerializer(data=voices,many=True)
                        sdat.is_valid()
                        sample_ques = ComCure.objects.get(pk = 61)
                        sample_ques = sz.CommonSerializer(instance=sample_ques).data
                        tut_voice = sdat.data
                        # StuCure.objects.create(
                        #     stu = student,
                        #     com_cure = ComCure.objects.get(pk=61)
                        # )
                        code = 'tutorial'
                elif stucur.curr_level == 2:
                    if not StuCure.objects.filter(stu_id = s_id,com_cure__com_id__range=(81,100)).exists():
                        sound = [16,17,18]
                        for s in sound:
                            voices.append(Voice.objects.get(pk=s))
                        sdat = sz.VoiceSerializer(data=voices,many=True)
                        sdat.is_valid()
                        sample_ques = ComCure.objects.get(pk = 81)
                        sample_ques = sz.CommonSerializer(instance=sample_ques).data
                        tut_voice = sdat.data
                        # StuCure.objects.create(
                        #     stu = student,
                        #     com_cure = ComCure.objects.get(pk=81)
                        # )      
                        code= 'tutorial'           
                elif stucur.curr_level == 3:
                    if not StuCure.objects.filter(stu_id = s_id,com_cure__com_id__range=(101,120)).exists():
                        sound = sound = [19,20,21]
                        for s in sound:
                            voices.append(Voice.objects.get(pk=s))
                        sdat = sz.VoiceSerializer(data=voices,many=True)
                        sdat.is_valid()
                        sample_ques = ComCure.objects.get(pk = 101)
                        sample_ques = sz.CommonSerializer(instance=sample_ques).data
                        tut_voice = sdat.data
                        # StuCure.objects.create(
                        #     stu = student,
                        #     com_cure = ComCure.objects.get(pk=101)
                        # )     
                        code = 'tutorial'  
            else:
                if not StuCure.objects.filter(stu_id = s_id , cure_txt = stucur.cur_curr).exists():
                    tut_voice , sample_ques = self.get_tutorial(student,stucur.cur_curr)
                    # StuCure.objects.create(
                    #     stu = student,
                    #     cure_txt = stucur.cur_curr
                    # ).save()
                    code = 'tutorial'
                # return JsonResponse({"read":read,"read_voice":read_voice,"tut_voice":tut_voice,"sample_ques":sample_ques,"daily_cure":stucur.cur_curr,"daily_read":stucur.cur_read,"code":"tutorial"},status=200)
            curr_idx = CureIdx.objects.get(idx_txt=stucur.cur_curr).idx_id
            curr_level = stucur.curr_level
            cure , answer = self.get_cure(curr_idx,curr_level)
            return JsonResponse({"read":read,"read_voice": read_voice,"cure":cure,"daily_cure": stucur.cur_curr,"daily_read": stucur.cur_read, "tut_voice":tut_voice,"sample_ques":sample_ques,"answers": answer , "code":code},status=200)        
        return JsonResponse({"message": "존재하지 않는 학습자입니다.","code":2},status=200)

class CureAns(View):
    def update_read(self,s_id,new_read_id,read_idx):
        if CureMaster.objects.filter(pk=new_read_id).exists():
            next_read = CureMaster.objects.get(pk=new_read_id)
            new_read_idx = read_idx
            if new_read_idx != next_read.cure_idx.idx_id:
                read_order = CureIdx.objects.get(pk=next_read.cure_idx.idx_id)
                read_order = read_order.read_order
                read_order += 1 
                if CureIdx.objects.filter(read_order = read_order).exists():
                    new_read_idx = CureIdx.objects.get(read_order=read_order).idx_id
                else:
                    return False
            cure_info = CureIdx.objects.get(pk=new_read_idx)
            stucur = StuCurrent.objects.get(stu_id=s_id)
            stucur.cur_read = cure_info.idx_txt
            stucur.cur_read_id = next_read.cure_id
            stucur.read_level = next_read.cure_level
            stucur.save()
            return True
        else:
            return False
    
    def ans_read(self,student,data,idx_id):
        score = data['full_score']
        phone_score = data['phone_score']
        speed_score = data['speed_score']
        rhythm_score = data['rhythm_score']
        cure_id = data['cure_id']
        cure_txt = CureIdx.objects.get(pk=idx_id).idx_txt
        class_txt = 'A'
        is_pass = False
        is_review = data['is_review']
        is_daily = data['is_daily']
        retry = True
        class_voice = Voice.objects.get(pk = 35)
        if score >= 85:
            is_pass = True
            class_voice = Voice.objects.get(pk = 33)
            retry = False
            cure_id = int(cure_id)+1
            # class_voice = sz.VoiceSerializer(instance=class_voice)
        elif score >= 75 :
            class_txt = 'B'
        elif score >= 65:
            clsss_txt = 'C'
        else:
            class_txt = 'D'
        if rhythm_score <=0:
            class_voice = Voice.objects.get(pk=35)
            retry = True
        if speed_score <= -5 :
            class_voice = Voice.objects.get(pk=38)
            retry = True

        StuCure.objects.create(
            stu = student,
            full_score = score,
            cure_id = cure_id,
            phone_score = phone_score,
            speed_score = speed_score,
            rhythm_score = rhythm_score,
            is_review = is_review,
            is_daily = is_daily,
            cure_txt = cure_txt
        ).save()

        class_voice = sz.VoiceSerializer(instance=class_voice)
        if retry ==  True:
            good_voice = Voice.objects.get(pk=33)
            good_voice = sz.VoiceSerializer(instance = good_voice)
            voices = []
            voices.append(class_voice.data)
            voices.append(good_voice.data)
            return cure_id,class_txt,is_pass,voices,retry

        return cure_id, class_txt, is_pass, class_voice.data , retry

    def answer_alternative(self,student,data,idx_id):
        ori_answer = data['ori_answer']
        stu_answer = data['stu_answer']
        cure_id = data['cure_id']
        cure = CureMaster.objects.get(pk=cure_id)
        cure_txt = CureIdx.objects.get(pk=idx_id).idx_txt
        is_review = data['is_review']
        is_daily = data['is_daily']
        is_first = data['is_first']
        is_correct = 'F'
        correct_voice = Voice.objects.get(pk=36)
        if ori_answer == stu_answer:
            is_correct = 'T'
            correct_voice = Voice.objects.get(pk=34)
        StuCure.objects.create(
            stu = student,
            is_correct = is_correct,
            cure_id = cure_id,
            is_review = is_review,
            is_daily = is_daily,
            is_first = is_first,
            ori_answer = ori_answer,
            stu_answer = stu_answer,
            cure_txt = cure_txt
        ).save()
        s = self.update_current(data,student,cure_txt,idx_id)
        correct_voice = sz.VoiceSerializer(instance = correct_voice)
        return is_correct , s , correct_voice.data

    def update_current(self,data,student,idx_txt,idx_id):
        s_id = student.stu_id
        stucur = StuCurrent.objects.get(stu_id = s_id)
        temp1 = 0
        temp2 = 0
        cures = StuCure.objects.filter(stu = student,cure_txt = idx_txt,is_review = 'F',is_daily = 'T',is_first = 'T')
        length = cures.count()
        if length % 10 == 0:
            cures = list(cures)[-10:]
            if stucur.cur_curr_last1:
                temp1 = stucur.cur_curr_last1
            if stucur.cur_curr_last2:
                temp2 = stucur.cur_curr_last2
            tmp = 0
            for c in cures:
                if c.is_correct == 'T':
                    tmp += 1
            stucur.cur_curr_last1 = tmp * 10
            stucur.cur_curr_last2 = temp1
            stucur.cur_curr_last3 = temp2
            stucur.save()
        if stucur.cur_curr_last1 >= 90 and stucur.cur_curr_last2 >= 90 and stucur.cur_curr_last3 >= 90:
            if idx_id == 4:
                if ComCure.objects.filter(com_level = stucur.curr_level+1).exists():
                    stucur.curr_level += 1
                    stucur.cur_curr_last1 = 0
                    stucur.cur_curr_last2 = 0
                    stucur.cur_curr_last3 = 0
                    stucur.save()
                else:
                    current = CureIdx.objects.get(pk=idx_id).curr_order
                    next_cur = current + 1
                    if CureIdx.objects.filter(curr_order = next_cur).exists():
                        nextc = CureIdx.objects.get(curr_order = next_cur).idx_txt
                        stucur.cur_curr = nextc
                        stucur.cur_level = 1
                        stucur.cur_curr_last1 = 0
                        stucur.cur_curr_last2 = 0
                        stucur.cur_curr_last3 = 0
                        stucur.save()
                    else : 
                        stucur.save()
                        return False
            else :
                if CureMaster.objects.filter(cure_idx = idx_id,cure_level = stucur.curr_level+1).exists():
                    stucur.curr_level += 1
                    stucur.cur_curr_last1 = 0
                    stucur.cur_curr_last2 = 0
                    stucur.cur_curr_last3 = 0
                    stucur.save()
                else:
                    current = CureIdx.objects.get(pk=idx_id).curr_order
                    next_cur = current + 1
                    if CureIdx.objects.filter(curr_order = next_cur).exists():
                        nextc = CureIdx.objects.get(curr_order = next_cur).idx_txt
                        stucur.cur_curr = nextc
                        stucur.cur_curr_last1 = 0
                        stucur.cur_curr_last2 = 0
                        stucur.cur_curr_last3 = 0
                        stucur.save()
                    else : 
                        stucur.save()
                        return False                   
        stucur.save()
        return True

    def answer_common(self,student,data,idx_id,idx_txt):
        com_id = data['cure_id']
        com_cure = ComCure.objects.get(pk=com_id)
        ori_answer = data['ori_answer']
        stu_answer = data['stu_answer']
        is_correct = 'F'
        correct_voice = Voice.objects.get(pk=36)
        if ori_answer == stu_answer :
            is_correct = 'T'
            correct_voice = Voice.objects.get(pk=34)
        is_review  = data['is_review']
        is_daily = data['is_daily']
        is_first = data['is_first']
        StuCure.objects.create(
            stu = student,
            cure_txt = idx_txt,
            is_correct = is_correct,
            com_cure = com_cure,
            is_review = is_review,
            ori_answer = ori_answer,
            stu_answer = stu_answer,
            is_daily = is_daily,
            is_first = is_first
        ).save()
        correct_voice = sz.VoiceSerializer(instance = correct_voice)
        s = self.update_current(data,student,idx_txt,idx_id)
                   
        return is_correct , s,correct_voice.data
        
    def answer_sound(self,student,data,idx_id,idx_txt):
        score = data['full_score']
        phone_score = data['phone_score']
        speed_score = data['speed_score']
        rhythm_score = data['rhythm_score']
        cure_id = data['cure_id']
        class_txt = 'A'
        is_pass = False
        is_review = data['is_review']
        is_daily = data['is_daily']
        is_first = data['is_first']
        class_voice = Voice.objects.get(pk = 35)
        if score >= 85:
            is_pass = True
            class_voice = Voice.objects.get(pk = 33)
        elif score >= 75:
            class_txt = 'B'
        elif score >= 65:
            class_txt = 'C'
        else:
            class_txt = 'D'
        if rhythm_score <=0:
            class_voice = Voice.objects.get(pk=40)
            is_pass = False
        if speed_score <= -5 :
            class_voice = Voice.objects.get(pk=38)
            is_pass = False
        StuCure.objects.create(
            stu = student,
            full_score = score,
            cure_id = cure_id,
            phone_score = phone_score,
            speed_score = speed_score,
            rhythm_score = rhythm_score,
            is_review = is_review,
            is_daily = is_daily,
            is_first = is_first,
            cure_txt = idx_txt
        ).save()
        s = self.update_sound(data,student,idx_txt,idx_id)
        class_voice = sz.VoiceSerializer(instance=class_voice)
        if is_pass ==  False:
            good_voice = Voice.objects.get(pk=33)
            good_voice = sz.VoiceSerializer(instance = good_voice)
            voices = []
            voices.append(class_voice.data)
            voices.append(good_voice.data)
            return is_pass,class_txt,s,voices
        return is_pass , class_txt, s , class_voice.data

    def update_sound(self,data,student,idx_txt,idx_id):
        s_id = student.stu_id
        stucur = StuCurrent.objects.get(stu_id = s_id)
        temp1 = 0
        temp2 = 0
        cures = StuCure.objects.filter(stu = student,cure_txt = idx_txt,is_review = 'F',is_daily = 'T',is_first='T')
        length = cures.count()
        if length % 10 == 0:
            cures = list(cures)[-10:]
            if stucur.cur_curr_last1:
                temp1 = stucur.cur_curr_last1
            if stucur.cur_curr_last2:
                temp2 = stucur.cur_curr_last2
            tmp = 0
            for c in cures:
                if c.full_score >= 85:
                    tmp += 1
            stucur.cur_curr_last1 = tmp * 10
            stucur.cur_curr_last2 = temp1
            stucur.cur_curr_last3 = temp2
            stucur.save()
        if stucur.cur_curr_last1 >= 90 and stucur.cur_curr_last2 >= 90 and stucur.cur_curr_last3 >= 90:
            if CureMaster.objects.filter(cure_idx = idx_id,cure_level = stucur.curr_level+1).exists():
                stucur.curr_level += 1
                stucur.cur_curr_last1 = 0
                stucur.cur_curr_last2 = 0
                stucur.cur_curr_last3 = 0
                stucur.save()
            else:
                current = CureIdx.objects.get(pk=idx_id).curr_order
                next_cur = current + 1
                if CureIdx.objects.filter(curr_order = next_cur).exists():
                    nextc = CureIdx.objects.get(curr_order = next_cur).idx_txt
                    stucur.cur_curr = nextc
                    stucur.cur_curr_last1 = 0
                    stucur.cur_curr_last2 = 0
                    stucur.cur_curr_last3 = 0
                    stucur.save()
                else : 
                    stucur.save()
                    return False                   
        stucur.save()
        return True

    def answer_consomatch(self,student,data,idx_id,idx_txt):
        cure1  = data['cure_id']
        cure2 = data['cure_id2']
        cure3 = data['cure_id3']
        c1 = CureMaster.objects.get(pk = cure1)
        c2 = CureMaster.objects.get(pk=cure2)
        c3 = CureMaster.objects.get(pk=cure3)
        ori_answer = data['ori_answer']
        stu_answer = data['stu_answer']
        is_correct = 'F'
        correct_voice = Voice.objects.get(pk=36)
        if ori_answer == stu_answer:
            is_correct = 'T'
            correct_voice = Voice.objects.get(pk = 34)
        is_review = data['is_review']
        is_daily = data['is_daily']
        is_first = data['is_first']
        StuCure.objects.create(
            stu = student,
            cure_txt = idx_txt,
            cure = c1,
            cure_2 = c2,
            cure_3 = c3,
            is_correct = is_correct,
            is_review = is_review,
            is_daily = is_daily,
            is_first = is_first,
            ori_answer = ori_answer,
            stu_answer = stu_answer
        ).save()
        correct_voice = sz.VoiceSerializer(instance=correct_voice)
        s = self.update_consomatch(data,student,idx_txt,idx_id)

        return is_correct,s,correct_voice.data
   
    def update_consomatch(self,data,student,idx_txt,idx_id):
        s_id = student.stu_id
        stucur = StuCurrent.objects.get(stu_id = s_id)
        temp1 = 0
        temp2 = 0
        cures = StuCure.objects.filter(stu = student,cure_txt = idx_txt,is_review = 'F',is_daily = 'T',is_first = 'T')
        length = cures.count()
        if length % 10 == 0:
            cures = list(cures)[-10:]
            if stucur.cur_curr_last1:
                temp1 = stucur.cur_curr_last1
            if stucur.cur_curr_last2:
                temp2 = stucur.cur_curr_last2
            tmp = 0
            for c in cures:
                if c.is_correct == 'T':
                    tmp += 1
            stucur.cur_curr_last1 = tmp * 10
            stucur.cur_curr_last2 = temp1
            stucur.cur_curr_last3 = temp2
            stucur.save()
        if stucur.cur_curr_last1 >= 90 and stucur.cur_curr_last2 >= 90 and stucur.cur_curr_last3 >= 90:
            current = CureIdx.objects.get(pk=idx_id).curr_order
            next_cur = current + 1
            if CureIdx.objects.filter(curr_order = next_cur).exists():
                nextc = CureIdx.objects.get(curr_order = next_cur).idx_txt
                stucur.cur_curr = nextc
                stucur.cur_curr_last1 = 0
                stucur.cur_curr_last2 = 0
                stucur.cur_curr_last3 = 0
                stucur.save()
            else : 
                stucur.save()
                return False                   
        stucur.save()
        return True
    
    def answer_tutorial(self,student,data):
        idx_txt = data['idx_txt']
        if idx_txt == "common":
            ques_id = data['ques_id']
            StuCure.objects.create(
                stu = student,
                com_cure = ComCure.objects.get(pk = ques_id)
            ).save()
        else:
            StuCure.objects.create(
                stu = student,
                cure_txt = idx_txt
            ).save()
        return True

    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        s_id = data['s_id']
        idx_txt = data['idx_txt']
        if CureIdx.objects.filter(idx_txt = idx_txt).exists():
            i = CureIdx.objects.get(idx_txt = idx_txt)
            idx_id = i.idx_id
            if Student.objects.filter(pk=s_id).exists():
                student = Student.objects.get(pk=s_id)
                if 'tutorial' in data:
                    is_okay = self.answer_tutorial(student,data)
                    return JsonResponse({"is_okay":is_okay,"code":1},status=200)
                    
                if idx_id == 1 or idx_id == 2 or idx_id == 11 or idx_id == 12: # read
                    new_read_id , class_txt , is_pass,class_voice, retry = self.ans_read(student,data,idx_id)
                    s = self.update_read(s_id,new_read_id,idx_id)
                    if s:
                        return JsonResponse({"is_okay":is_pass,"class": class_txt,"class_voice":class_voice,"retry":retry,"code":1},status=200)
                    else:
                        return JsonResponse({"is_okay":is_pass,"class": class_txt,"class_voice":class_voice,"retry":retry,"message": "더 이상 학습할 문제가 없습니다.","code":2},status=200)
                elif idx_id == 3 or idx_id == 6 or idx_id == 8 or idx_id == 10:
                    is_correct, s ,correct_voice = self.answer_alternative(student,data,idx_id)
                    if s:
                        return JsonResponse({"is_correct":is_correct,"correct_voice":correct_voice,"code":1},status=200)
                    else:
                        return JsonResponse({"is_correct":is_correct,"correct_voice":correct_voice,"code":2,"message":"모든 문제를 학습하였습니다."},status=200)
                elif idx_id == 4:
                    is_correct,s ,correct_voice= self.answer_common(student,data,idx_id,idx_txt)
                    if s:
                        return JsonResponse({"is_corret":is_correct,"correct_voice":correct_voice,"code":1},status=200)
                    else:
                        return JsonResponse({"is_correct":is_correct,"correct_voice":correct_voice,"code":2,"message":"모든 문제를 학습하였습니다."},status=200)
                elif idx_id == 5 or idx_id == 9:
                    is_pass,class_txt, s, class_voice = self.answer_sound(student,data,idx_id,idx_txt)
                    if s:
                        return JsonResponse({"is_pass":is_pass,"class":class_txt,"class_voice":class_voice,"code":1},status=200)
                    else:
                        return JsonResponse({"is_pass":is_pass,"class":class_txt,"class_voice":class_voice,"code":2,"message":"모든 문제를 학습하였습니다."},status=200)
                elif idx_id == 7:
                    is_correct, s, correct_voice = self.answer_consomatch(student,data,idx_id,idx_txt)
                    if s:
                        return JsonResponse({"is_correct":is_correct,"correct_voice":correct_voice,"code":1},status=200)
                    else:
                        return JsonResponse({"is_correct":is_correct,"correct_voice":correct_voice,"code":2,"message":"모든 문제를 학습하였습니다."},status=200)
            else:
                return JsonResponse({"message":"해당 학습자가 존재하지 않습니다.","code":3},status=200)

        else:
            return JsonResponse({"message": "해당 학습이 존재하지 않습니다.","code":"err"},status=200)

class CureSave(View):
    @csrf_exempt
    def post(self,request):
        data = json.loads(request.body)
        s_id = data['s_id']
        date = datetime.datetime.now()
        date = date.strftime('%Y-%m-%d')
        if Student.objects.filter(pk=s_id).exists():
            student = Student.objects.filter(pk = s_id)
            if not StuCurrent.objects.filter(stu_id = s_id).exists():
                status = []
            else:
                stucur = StuCurrent.objects.get(stu_id=s_id)
                status = stucur.cur_read
                cur_lev = stucur.read_level
                cur_read = stucur.cur_read_id
                idx_id = CureIdx.objects.get(idx_txt = status).idx_id
                tid = CureMaster.objects.get(pk=cur_read).cure_tid
            # status = []
                if StuCure.objects.filter(stu_id = s_id,cure_txt = status,is_daily = 'T', full_score__gte = 85, date = date).count() >= CureMaster.objects.filter(cure_idx_id = idx_id, cure_level = cur_lev, cure_tid = tid).count():
                    status = stucur.cur_curr
                elif StuCure.objects.filter(stu_id = s_id,cure_txt = stucur.cur_curr,is_daily = 'T',date=date,is_first = 'T').count() >= 10:
                    status = stucur.cur_read
            return JsonResponse({"current":status,"code":1},status=200)
        return JsonResponse({"message":"해당 학습자가 존재하지 않습니다.","code":2},satus=200)
   
# class GetDaily(View):
#     @csrt_exempt
#     def post(self,request):
#         data = json.loads(request.body)
#         s_id = data['s_id']

#         if Student.objects.filter(pk =s_id).exists():
#             student = Student.objects.get(pk=s_id)
#             if not StuCurrent.objects.filter(stu_id = s_id).exists():

class Statistic(View):
    def test_result(self,student,date,period):
        times = []
        swp_score = {}
        ph_score = {}
        foc_score = {}
        classes = ['d','d','d']
        levels = [1,1,1]
        if period == 'day':
            for i in range(7):
                tmp = date + datetime.timedelta(days = -(6-i))
                times.append(tmp.strftime('%Y-%m-%d'))
            for t in times:
                swp_whole = StuTest.objects.filter(stu=student,date = t, test_txt = 'swp').count()
                if swp_whole == 0:
                    swp_score[t] = None
                else:
                    swp_correct = StuTest.objects.filter(stu = student,date=t,test_txt='swp',is_correct = 'T').count()
                    swp_score[t] = (swp_correct/swp_whole) * 100
                ph_whole = StuTest.objects.filter(stu = student,date=t,test_txt = 'ph').count()
                if ph_whole == 0 :
                    ph_score[t] = None
                else:
                    ph_correct = StuTest.objects.filter(stu=student,date=t,test_txt='ph',is_correct = 'T').count()
                    ph_score[t] = (ph_correct/ph_whole)*100
                
                foc_score[t] = StuTest.objects.filter(stu=student,date=t,test_txt='foc').aggregate(Avg('full_score'))['full_score__avg']
        if period == 'week':
            for i in range(7):
                tmp = date + datetime.timedelta(weeks = -(7-i))
                times.append(tmp.strftime('%Y-%m-%d'))
            for i in range(7):
                if i != 6 :
                    t = times[i]
                    t2 = times[i+1]
                else:
                    t = times[i]
                    t2 = date.strftime('%Y-%m-%d')
                swp_whole = StuTest.objects.filter(stu=student,date__range= [t,t2], test_txt = 'swp').count()
                if swp_whole == 0:
                    swp_score[t+'~'+t2] = None
                else:
                    swp_correct = StuTest.objects.filter(stu = student,date__range=[t,t2],test_txt='swp',is_correct = 'T').count()
                    swp_score[t+'~'+t2] = (swp_correct/swp_whole) * 100
                ph_whole = StuTest.objects.filter(stu = student,date__range=[t,t2],test_txt = 'ph').count()
                if ph_whole == 0 :
                    ph_score[t+'~'+t2] = None
                else:
                    ph_correct = StuTest.objects.filter(stu=student,date__range=[t,t2],test_txt='ph',is_correct = 'T').count()
                    ph_score[t+'~'+t2] = (ph_correct/ph_whole)*100
                foc_score[t+'~'+t2] = StuTest.objects.filter(stu=student,date__range=[t,t2],test_txt='foc').aggregate(Avg('full_score'))['full_score__avg']
        if period == 'month':
            mon = date.month
            year = date.year
            for i in range(7):
                times.append(mon-(6-i))
            for t in times:
                swp_whole = StuTest.objects.filter(stu=student,date__year = year,date__month= t, test_txt = 'swp').count()
                if swp_whole == 0:
                    swp_score[t] = None
                else:
                    swp_correct = StuTest.objects.filter(stu = student,date__year = year,date__month= t,test_txt='swp',is_correct = 'T').count()
                    swp_score[t] = (swp_correct/swp_whole) * 100
                ph_whole = StuTest.objects.filter(stu = student,date__year = year,date__month= t,test_txt = 'ph').count()
                if ph_whole == 0 :
                    ph_score[t] = None
                else:
                    ph_correct = StuTest.objects.filter(stu=student,date__year = year,date__month= t,test_txt='ph',is_correct = 'T').count()
                    ph_score[t] = (ph_correct/ph_whole)*100
                foc_score[t] = StuTest.objects.filter(stu=student,date__year = year,date__month= t,test_txt='foc').aggregate(Avg('full_score'))['full_score__avg']
        cscore = [0,0,0]
        if period == "week":
            for i in range(7):
                if i != 6:
                    t = times[i]
                    t2 = times[i+1]
                else:
                    t = times[i]
                    t2 = date.strftime('%Y-%m-%d')
                if swp_score[t+'~'+t2] == None:
                    cscore[0] += 0 
                else :
                    cscore[0] = cscore[0] + swp_score[t+'~'+t2]
                if ph_score[t+'~'+t2] == None:
                    cscore[1] += 0 
                else :
                    cscore[1] = cscore[1] + ph_score[t+'~'+t2]
                if foc_score[t+'~'+t2] == None:
                    cscore[2] += 0 
                else :
                    cscore[2] = cscore[2] + foc_score[t+'~'+t2]
        else:
            for i in times:
                if swp_score[i] == None:
                    cscore[0] += 0 
                else :
                    cscore[0] = cscore[0] + swp_score[i]
                if ph_score[i] == None:
                    cscore[1] += 0 
                else :
                    cscore[1] = cscore[1] + ph_score[i]
                if foc_score[i] == None:
                    cscore[2] += 0 
                else :
                    cscore[2] = cscore[2] + foc_score[i]
        for idx,c in enumerate(cscore):
            if (c/7) >= 85:
                classes[idx] = '우수'
            elif (c/7) >= 75:
                classes[idx]  ='보통'
            else:
                classes[idx] = '미흡'
        slevels = [1,1,1]
        every_swp = StuTest.objects.filter(stu=student,test_txt = 'swp',is_correct = 'T').order_by('-id')[:15]
        if every_swp.count() ==0:
            levels[1] = 1
        for s in every_swp:
            sw = TestMaster.objects.get(pk=s.ques_id)
            freq = sw.ques_int
            if freq == 500:
                if slevels[0] <= sw.ques_level +1:
                    slevels[0] = sw.ques_level +1
            elif freq == 1000:
                if slevels[1] <= sw.ques_level +1:
                    slevels[1] = sw.ques_level +1
            elif freq == 2000:
                if slevels[2] <= sw.ques_level +1:
                    slevels[2] = sw.ques_level +1
        levels[0] = min(slevels)
        every_ph = StuTest.objects.filter(stu=student,test_txt = 'ph').order_by('-id')[:25]
        c_ph = len([p for p in every_ph if p.is_correct == 'T'])
        pscore = (c_ph/25) * 100
        if pscore >= 96:
            levels[1]= 6
        elif pscore >= 86:
            levels[1] =5
        elif pscore >= 70:
            levels[1] = 4
        elif pscore >= 50:
            levels[1] = 3
        elif pscore >= 33:
            levles[1] = 2
        levels[2] = TestCurrent.objects.get(stu = student).focus_lev +1
        tot_lev = min(levels)
        if tot_lev >=5:
            status = '경미'
        elif tot_lev >=3:
            status = '저위험군'
        elif tot_lev >=1:
            status = '고위험군'
        return swp_score,ph_score,foc_score,classes,status

    def cure_result(self,student,date,period):
        times = []
        amount = {}
        score = {}
        voice_score = {}
        if period == 'day':
            for i in range(7):
                tmp = date + datetime.timedelta(days = -(6-i))
                times.append(tmp.strftime('%Y-%m-%d'))
            for t in times:
                score_whole = StuCure.objects.filter(stu=student,date = t).exclude(is_correct__isnull=True).count()
                if score_whole == 0:
                    score[t] = None
                else:
                    correct = StuCure.objects.filter(stu = student,date=t,is_correct = 'T').count()
                    score[t] = (correct/score_whole) * 100
                did = StuCure.objects.filter(stu=student,date=t).count()
                amount[t] = did
                voice_score[t] = StuCure.objects.filter(stu=student,date=t).exclude(full_score__isnull=True).aggregate(Avg('full_score'))['full_score__avg']
        
        if period == 'week':
            for i in range(7):
                tmp = date + datetime.timedelta(weeks = -(7-i))
                times.append(tmp.strftime('%Y-%m-%d'))
            for i in range(7):
                if i != 6 :
                    t = times[i]
                    t2 = times[i+1]
                else:
                    t = times[i]
                    t2 = date.strftime('%Y-%m-%d')
                score_whole = StuCure.objects.filter(stu=student,date__range=[t,t2]).exclude(is_correct__isnull=True).count()
                if score_whole == 0:
                    score[t+'~'+t2] = None
                else:
                    correct = StuCure.objects.filter(stu = student,date__range=[t,t2],is_correct = 'T').count()
                    score[t+'~'+t2] = (correct/score_whole) * 100
                did = StuCure.objects.filter(stu=student,date__range=[t,t2]).count()
                amount[t+'~'+t2] = did
                voice_score[t+'~'+t2] =StuCure.objects.filter(stu=student,date__range=[t,t2]).exclude(full_score__isnull=True).aggregate(Avg('full_score'))['full_score__avg']
        if period == "month":
            mon = date.month
            year = date.year
            for i in range(7):
                times.append(mon-(6-i))
            for t in times:
                score_whole = StuCure.objects.filter(stu=student,date__year = year,date__month= t).exclude(is_correct__isnull=True).count()
                if score_whole == 0:
                    score[t] = None
                else:
                    correct = StuCure.objects.filter(stu = student,date__year = year,date__month= t,is_correct = 'T').count()
                    score[t] = (correct/score_whole) * 100
                did = StuCure.objects.filter(stu=student,date__year = year,date__month= t).count()
                amount[t] = did
                voice_score[t] =StuCure.objects.filter(stu=student,date__year = year,date__month= t).exclude(full_score__isnull=True).aggregate(Avg('full_score'))['full_score__avg']
        classes = ['미흡','미흡','미흡']
        cscore = [0,0,0]
        if period == "week":
            for i in range(7):
                if i != 6:
                    t = times[i]
                    t2 = times[i+1]
                else:
                    t = times[i]
                    t2 = date.strftime('%Y-%m-%d')
                if score[t+'~'+t2] == None:
                    cscore[1] += 0 
                else :
                    cscore[1] = cscore[1] + score[t+'~'+t2]
                if voice_score[t+'~'+t2] == None:
                    cscore[2] += 0 
                else :
                    cscore[2] = cscore[2] + voice_score[t+'~'+t2]
                cscore[0] += amount[t+'~'+t2]
        else:
            for i in times:
                if score[i] == None:
                    cscore[1] += 0 
                else :
                    cscore[1] = cscore[1] + score[i]
                if voice_score[i] == None:
                    cscore[2] += 0 
                else :
                    cscore[2] = cscore[2] + voice_score[i]
                cscore[0] += amount[i]
        for idx,c in enumerate(cscore):
            if (c/7) >= 85:
                classes[idx] = '우수'
            elif (c/7) >= 70:
                classes[idx]  ='보통'
            else:
                classes[idx] = '미흡' 
        if cscore[0]/7 >= 30:
            classes[0] = '우수'
        elif cscore[0]/7 >= 20:
            classes[0] = '보통'
        else:
            classes[0] = '미흡'
        return amount,score,voice_score,classes   


    def post(self,request):
        data = json.loads(request.body)
        s_id = data['s_id']
        period = data['period']
        cort = data['cure_or_test']
        date = datetime.datetime.now()

        if Student.objects.filter(pk=s_id).exists():
            student = Student.objects.get(pk=s_id)
            if cort == 'test':
                # score_swp ,score_ph,score_foc, classes, result = self.test_result(student,date,period)
                score_swp,score_ph,foc_score,classes,status = self.test_result(student,date,period)
                return JsonResponse({"score_swp":score_swp,"score_ph":score_ph,"score_foc":foc_score,"class":classes,"status":status,"code":cort},status=200)
            elif cort == 'cure':
                amount , score , voice_score,classes = self.cure_result(student,date,period)
                return JsonResponse({"amount":amount,"score":score,"voice_score":voice_score,"class":classes,"code":cort},status=200)
        else:
            return JsonResponse({"message":"해당 학습자가 존재하지 않습니다.","code":2},status=200)