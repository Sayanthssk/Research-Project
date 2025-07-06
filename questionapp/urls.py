
from django.urls import  path

from questionapp.views import *
from . import views

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('admindash', AdminDasView.as_view(), name='admindash'),
    path('manageuser', ManageuserView.as_view(), name='manageuser'),
    path('addquest', AddquestionsView.as_view(), name='addquest'),
    path('managequest', ManageQuestView.as_view(), name='managequest'),
    path('appeared', ViewAppeared.as_view(), name='appeared'),
    path('contappeared', ControllerAppeared.as_view(), name='contappeared'),
    path('adduser', AddUserView.as_view(), name='adduser'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('manageinst', ManageInstructionView.as_view(), name='manageinst'),
    path('addinst', AddInstructionView.as_view(), name='addinst'),
    path('removeuser/<int:id>', RemoveUserView.as_view(), name='removeuser'),
    path('deleteinst/<int:id>', DeleteInstruction.as_view(), name='deleteinst'),
    path('editinst/<int:id>', EditInst.as_view(), name='editinst'),
    path('deletequest/<int:id>', DeleteQuestion.as_view(), name='deleteuquest'),

    path('controllerdash', ControllerDashView.as_view(), name='controllerdash'),
    path('instruction', InstructionView.as_view(), name='instruction'),
    # path('exam/start/', StartExamView.as_view(), name='start_exam'),
    path('exam/question/', ShowQuestionView.as_view(), name='show_question'),
    path('api/submit-result/', views.submit_result, name='submit_result'),
    path('postorspon', PostOrSpontanious.as_view(), name='postorspon'),
    path('postappeared', PostAppeared.as_view(), name='postappeared'),
    path('postorspontquest', PostorSpontQuest.as_view(), name='postorspontquest'),
    path('managepostquest', ManagePostQuestView.as_view(), name='managepostquest'),
    path('addpostquest', AddPostQuest.as_view(), name='addpostquest'),
    path('postorspontcont', ControllerPostorSpont.as_view(), name='postorspontcont'),
    path('postappearedcontroller', PostAppearedController.as_view(), name='postappearedcontroller'),
    path('contpostorspont', ControllerPostorSpont.as_view(), name='contpostorspont'),
    path('spontaneousinstruction', Spontaneousinstruction.as_view(), name='spontaneousinstruction'),
]
