from django.urls import path
from .views import MakeUser,LogIn,UserModify,UserDelete,UserGet,StuAdd,StuModify,StuDel,StuGet,CureGet,CureAns,TestGet,TestAns,Statistic,CureSave,TestResult,TestProceed,Testdid,TestReset
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [ ##만들어준 view들을 경로 지정해서 routing해줌.
    path('',MakeUser.as_view()),
    path('user/register',MakeUser.as_view()),
    path('user/sign_in',LogIn.as_view()),
    path('user/modify',UserModify.as_view()),
    path('user/delete',UserDelete.as_view()),
    path('user/get',UserGet.as_view()),
    path('student/add',StuAdd.as_view()),
    path('student/modify',StuModify.as_view()),
    path('student/delete',StuDel.as_view()),
    path('student/get',StuGet.as_view()),
    # path('swp_test/ask',SwpGet.as_view()),
    # path('swp_test/answer',SwpAns.as_view()),
    # path('ph_test/ask',PhGet.as_view()),
    # path('ph_test/answer',PhAns.as_view()),
    # path('foc_test/ask',FocGet.as_view()),
    # path('foc_test/answer',FocAns.as_view()),
    path('cure/ask',CureGet.as_view()),
    path('cure/answer',CureAns.as_view()),
    path('cure/save',CureSave.as_view()),
    path('diagnose/ask',TestGet.as_view()),
    path('diagnose/answer',TestAns.as_view()),
    path('diagnose/reset',TestReset.as_view()),
    path('statistic/get',Statistic.as_view()),
    path('diagnose/result',TestResult.as_view()),
    path('diagnose/okay',TestProceed.as_view()),
    path('diagnose/did',Testdid.as_view()),
    path('user/jwt_login',obtain_jwt_token)
]