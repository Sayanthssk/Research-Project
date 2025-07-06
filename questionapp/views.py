from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from questionapp.models import *
from questionapp.forms import *

# Create your views here.

class LogoutView(View):
    def get(self, request):
        return HttpResponse('''<script>alert("Logout successfully");window.location='/';</script>''')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        try:
            obj = Login.objects.get(username=username, password=password)
            request.session['user_id'] = obj.id
            # Handle based on user type
            if obj.usertype == 'admin':    
                return HttpResponse('''<script>alert("Welcome back");window.location='/admindash'</script>''')
            elif obj.usertype == 'patient':
               
                    return HttpResponse('''<script>alert("Login successfully");window.location='/controllerdash'</script>''')
            elif obj.usertype == 'controller':
                return HttpResponse('''<script>alert("Login successfully");window.location='/controllerdash'</script>''')


        except Login.DoesNotExist:
            # Handle case where login details do not exist
            return HttpResponse('''<script>alert("Invalid username or password");window.location='/'</script>''')
    

class AdminDasView(View):
    def get(self, request):
        c = SpontaniousQuestion.objects.all().count()
        return render(request, 'admindash.html',{'c': c})
    
class AddUserView(View):
    def get(self, request):
        return render(request, 'adduser.html')
    def post(self, request):
        c = User_Form(request.POST, request.FILES)
        if c.is_valid():
            reg = c.save(commit=False)
            user = Login.objects.create(username=reg.abbreviation, password=request.POST['password'], usertype=request.POST['role'])
            reg.LOGINID = user
            reg.save()
            return HttpResponse('''<script>alert("User added successfully");window.location='/manageuser'</script>''')
    

class ManageuserView(View):
    def get(self, request):
        user = User_Model.objects.all()
        return render(request, 'manageuser.html', {'c': user})
    
class RemoveUserView(View):
    def get(self, request, id):
        c = User_Model.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert('user removed successfully');window.location='/manageuser'</script>''')

class AddInstructionView(View):
    def get(self, request):
        return render(request, 'addinstruction.html')
    def post(self, request):
        c = Instruction_Form(request.POST)
        if c.is_valid():
            c.save()
            return HttpResponse('''<script>alert("Instruction added successfully");window.location='/manageinst'</script>''')
        
class ManageInstructionView(View):
    def get(self, request):
        c = Instructions_Model.objects.all()
        return render(request, 'manageinstructions.html', {'c': c})
    
class DeleteInstruction(View):
    def get(self, request, id):
        c = Instructions_Model.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert("Instruction deleted successfully");window.location='/manageinst'</script>''')
    
class EditInst(View):
    def get(self, request, id):
        c = Instructions_Model.objects.get(id=id)
        return render(request, 'editinstruction.html', {'c': c})
    def post(self, request, id):
        c = Instructions_Model.objects.get(id=id)
        form = Instruction_Form(request.POST, instance=c)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert("Instruction updated successfully");window.location='/manageinst'</script>''')

class AddquestionsView(View):
    def get(self, request):
        return render(request, 'addquestion.html')
    def post(self, request):
        c = Question_Form(request.POST, request.FILES)
        if c.is_valid():
            c.save()
            return HttpResponse('''<script>alert("Question added successfully");window.location='/managequest'</script>''')
    
class ManageQuestView(View):
    def get(self, request):
        c = SpontaniousQuestion.objects.all()
        return render(request, 'managequest.html', {'c': c})
    
class DeleteQuestion(View):
    def get(self, request, id):
        c = SpontaniousQuestion.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert("Question deleted successfully");window.location='/managequest'</script>''')

from django.views import View
from django.shortcuts import render
from collections import defaultdict
from .models import SpontaniousResult, User_Model

class ViewAppeared(View):
    def get(self, request):
        results = SpontaniousResult.objects.filter(USERID__LOGINID__usertype='patient').select_related('USERID')

        # Group results by user
        user_results = defaultdict(list)

        for res in results:
            user_results[res.USERID].append(res)

        # Build a list of structured rows for the template
        rows = []

        for user, res_list in user_results.items():
            # Fill 10 slots max
            slots = [None] * 10
            filled = 0

            for res in res_list:
                if filled < 10:
                    slots[filled] = res
                    filled += 1

            total_correct = sum(1 for r in slots if r and r.is_correct)

            rows.append({
                'user': user,
                'results': slots,
                'total_correct': total_correct
            })

        return render(request, 'viewattendeduser.html', {'rows': rows})



    
class ControllerAppeared(View):
    def get(self, request):
        results = SpontaniousResult.objects.filter(USERID__LOGINID__usertype='controller').select_related('USERID')

        # Group results by user
        user_results = defaultdict(list)

        for res in results:
            user_results[res.USERID].append(res)

        # Build a list of structured rows for the template
        rows = []

        for user, res_list in user_results.items():
            # Fill 10 slots max
            slots = [None] * 10
            filled = 0

            for res in res_list:
                if filled < 10:
                    slots[filled] = res
                    filled += 1

            total_correct = sum(1 for r in slots if r and r.is_correct)

            rows.append({
                'user': user,
                'results': slots,
                'total_correct': total_correct
            })

        return render(request, 'controllerattend.html', {'rows': rows})
    

#/////////////////////////////////////////////// completed admin module ////////////////////////////////////////////////////////////

class ControllerDashView(View):
    def get(self, request):
        return render(request, 'Controller/controllerdash.html')
    
class InstructionView(View):
    def get(self, request):
        c = Instructions_Model.objects.all()
        return render(request, 'Controller/instruction.html', {'c': c})
    
import random
import time
from django.shortcuts import render, redirect
from django.views import View
from .models import SpontaniousResult, User_Model
from django.utils import timezone
from django.http import JsonResponse


# class StartExamView(View):
#     def get(self, request):
#         # Store 10 random question IDs in session
#         all_ids = list(Question.objects.values_list('id', flat=True))
#         question_ids = random.sample(all_ids, min(10, len(all_ids)))
#         request.session['question_ids'] = question_ids
#         request.session['current_index'] = 0
#         request.session['start_time'] = str(timezone.now())

#         return redirect('show_question')
    

# from django.utils.dateparse import parse_datetime

# class ShowQuestionView(View):
#     def get(self, request):
#         index = request.session.get('current_index', 0)
#         question_ids = request.session.get('question_ids', [])

#         if not question_ids or index >= len(question_ids):
#             return redirect('controllerdash')

#         question_id = question_ids[index]
#         question = Question.objects.get(id=question_id)

#         return render(request, 'Controller/question.html', {
#             'question': question,
#             'index': index + 1,
#             'total': len(question_ids),
#         })

#     def post(self, request):
#         question_id = request.POST.get('question_id')
#         selected_option = request.POST.get('selected_option')
        
#         # Safely parse the time
#         start_time_str = request.session.get('start_time')
#         start_time = parse_datetime(start_time_str)
#         end_time = timezone.now()

#         response_time = (end_time - start_time).total_seconds()

#         question = Question.objects.get(id=question_id)
#         is_correct = selected_option == question.category

#         # Save result
#         Result.objects.create(
#             USERID=request.user,
#             QUESTIONID=question,
#             is_correct=is_correct,
#             response_time=response_time
#         )

#         # Move to next question
#         request.session['current_index'] += 1
#         request.session['start_time'] = str(timezone.now())

#         return JsonResponse({'is_correct': is_correct})


import random
import random
from django.views import View
from django.shortcuts import render


# class ShowQuestionView(View):
#     def get(self, request):
#         questions = Question.objects.order_by('?')
#         data = []
#         for q in questions:
#             options = [q.category, q.option1, q.option2, q.option3]  # category is assumed to be correct
#             random.shuffle(options)
#             data.append({
#                 'image': q.image.url,   # Ensure `q.image.url` is valid
#                 'options': options
#             })
#         return render(request, 'Controller/question.html', {'data': data})

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')


class ShowQuestionView(View):
    def get(self, request):
        questions = PostQuestion.objects.order_by('?')
        data = []
        for q in questions:
            options = [q.category, q.option1, q.option2, q.option3, q.option4, q.option5, q.option6]  # category is assumed to be correct
            random.shuffle(options)
            data.append({
                'id': q.id,
                'image': q.image.url,
                'options': options
            })

        # Get Login ID from session
        login_id = request.session.get('user_id')

        if not login_id:
            return redirect('login')  # or show error

        # Now get the User_Model with this LOGINID
        try:
            user_model = User_Model.objects.get(LOGINID_id=login_id)
        except User_Model.DoesNotExist:
            return HttpResponse("User profile not found", status=404)

        return render(request, 'Controller/question.html', {
            'data': data,
            'user_id': user_model.id
        })


    

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import SpontaniousQuestion, User_Model
from .forms import Result_Form

  
@csrf_exempt
def submit_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            user = User_Model.objects.get(id=data['USERID'])
            question = PostQuestion.objects.get(id=data['QUESTIONID'])
            selected_answer = data['selected_answer']
            response_time = float(data['response_time'])

            is_correct = (selected_answer == question.category)

            result = PostResult(
                USERID=user,
                QUESTIONID=question,
                response_time=response_time,
                is_correct=is_correct
            )
            result.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'invalid request'}, status=405)
            

class PostOrSpontanious(View):
    def get(self, request):
        return render(request, 'postOrSpontanious.html')
    
class PostAppeared(View):
    def get(self, request):
        results = PostResult.objects.filter(USERID__LOGINID__usertype='patient').select_related('USERID')

        # Group results by user
        user_results = defaultdict(list)

        for res in results:
            user_results[res.USERID].append(res)

        # Build a list of structured rows for the template
        rows = []

        for user, res_list in user_results.items():
            # Fill 10 slots max
            slots = [None] * 10
            filled = 0

            for res in res_list:
                if filled < 10:
                    slots[filled] = res
                    filled += 1

            total_correct = sum(1 for r in slots if r and r.is_correct)

            rows.append({
                'user': user,
                'results': slots,
                'total_correct': total_correct
            })
        return render(request, 'Postappearedpatients.html', {'rows':rows})
    

class PostorSpontQuest(View):
    def get(self, request):
        return render(request, 'postorspontquest.html')
    
class ManagePostQuestView(View):
    def get(self, request):
        c = PostQuestion.objects.all()
        return render(request, 'managepostquest.html', {'c': c})
    
class AddPostQuest(View):
    def get(self, request):
        return render(request, 'addpostquest.html')
    def post(self, request):
        c = PostQuestion_Form(request.POST, request.FILES)
        if c.is_valid():
            c.save()
            return HttpResponse('''<script>alert("Question added successfully");window.location='/managepostquest'</script>''')

class ControllerPostorSpont(View):
    def get(self, request):
        return render(request, 'postorspontcont.html')
    
class PostAppearedController(View):
    def get(self, request):
        results = PostResult.objects.filter(USERID__LOGINID__usertype='controller').select_related('USERID')

        # Group results by user
        user_results = defaultdict(list)

        for res in results:
            user_results[res.USERID].append(res)

        # Build a list of structured rows for the template
        rows = []

        for user, res_list in user_results.items():
            # Fill 10 slots max
            slots = [None] * 10
            filled = 0

            for res in res_list:
                if filled < 10:
                    slots[filled] = res
                    filled += 1

            total_correct = sum(1 for r in slots if r and r.is_correct)

            rows.append({
                'user': user,
                'results': slots,
                'total_correct': total_correct
            })
        return render(request, 'postappeardcontroller.html', {'rows': rows})
    

class ControllerPostorSpont(View):
    def get(self, request):
        return render(request, 'Controller/postorspontquestion.html')
    
class Spontaneousinstruction(View):
    def get(self, request):
        c = Instructions_Model.objects.all()
        return render(request, 'Controller/spontaneousinstruction.html', {'c': c})