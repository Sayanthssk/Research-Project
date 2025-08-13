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

from django.views import View
from django.shortcuts import render
from collections import defaultdict
from .models import SpontaniousResult

# class ViewAppeared(View):
#     def get(self, request):
#         # Get all results for patients only
#         results = SpontaniousResult.objects.filter(
#             USERID__LOGINID__usertype='patient'
#         ).select_related('USERID').order_by('USERID', 'id')  # Order by user and result ID

#         user_results = defaultdict(list)
#         for res in results:
#             user_results[res.USERID].append(res)

#         rows = []

#         for user, res_list in user_results.items():
#             # Make sure we have exactly 49 results, fill with None if less
#             slots = res_list[:49] + [None] * (49 - len(res_list))

#             total_correct = sum(1 for r in slots if r and r.is_correct)

#             rows.append({
#                 'user': user,
#                 'results': slots,
#                 'total_correct': total_correct
#             })

#         return render(request, 'viewattendeduser.html', {'rows': rows})


from collections import defaultdict, Counter
from django.views import View
from django.shortcuts import render
from .models import SpontaniousResult

class ViewAppeared(View):
    def get(self, request):
        results = SpontaniousResult.objects.select_related('USERID', 'QUESTIONID').filter(
            USERID__LOGINID__usertype='patient'
        ).order_by('USERID', 'id')

        user_results = defaultdict(list)
        all_labels = []
        label_count = Counter()

        # Build unique label per question
        for res in results:
            q = res.QUESTIONID
            if q:
                prefix = ""
                if q.Main_category and "without" in q.Main_category.lower():
                    prefix += "WO"
                elif q.Main_category and "with" in q.Main_category.lower():
                    prefix += "WC"
                else:
                    prefix += "UK"

                if q.Sub_category:
                    if "high" in q.Sub_category.lower():
                        prefix += "H"
                    elif "medium" in q.Sub_category.lower():
                        prefix += "M"
                    elif "low" in q.Sub_category.lower():
                        prefix += "L"
                    else:
                        prefix += "X"

                base_label = f"{prefix}_{q.category}"
                label_count[base_label] += 1
                full_label = f"{base_label}{label_count[base_label]}"

                all_labels.append(full_label)
                user_results[res.USERID].append((full_label, res))

        sorted_labels = sorted(all_labels, key=lambda x: (x.split('_')[0], x.split('_')[1]))

        rows = []
        for user, res_pairs in user_results.items():
            result_map = {}
            for label, res in res_pairs:
                result_map[label] = {
                    'is_correct': res.is_correct,
                    'response_time': res.response_time
                }

            row = {
                'user': user,
                'result_map': result_map,
                'total_correct': sum(1 for r in result_map.values() if r['is_correct']),
                'flattened_results': []
            }

            # Align results with labels
            for label in sorted_labels:
                if label in result_map:
                    row['flattened_results'].append(result_map[label])
                else:
                    row['flattened_results'].append({'is_correct': None, 'response_time': None})

            rows.append(row)

        return render(request, 'viewattendeduser.html', {
            'rows': rows,
            'labels': sorted_labels
        })





    
from collections import defaultdict, Counter
from django.shortcuts import render
from django.views import View
from .models import SpontaniousResult

class ControllerAppeared(View):
    def get(self, request):
        results = SpontaniousResult.objects.select_related('USERID', 'QUESTIONID').filter(
            USERID__LOGINID__usertype='controller'
        ).order_by('USERID', 'id')

        user_results = defaultdict(list)
        all_labels = []
        label_count = Counter()

        # Build unique label per question
        for res in results:
            q = res.QUESTIONID
            if q:
                prefix = ""
                if q.Main_category and "without" in q.Main_category.lower():
                    prefix += "WO"
                elif q.Main_category and "with" in q.Main_category.lower():
                    prefix += "WC"
                else:
                    prefix += "UK"

                if q.Sub_category:
                    if "high" in q.Sub_category.lower():
                        prefix += "H"
                    elif "medium" in q.Sub_category.lower():
                        prefix += "M"
                    elif "low" in q.Sub_category.lower():
                        prefix += "L"
                    else:
                        prefix += "X"

                base_label = f"{prefix}_{q.category}"
                label_count[base_label] += 1
                full_label = f"{base_label}{label_count[base_label]}"

                all_labels.append(full_label)
                user_results[res.USERID].append((full_label, res))

        sorted_labels = sorted(all_labels, key=lambda x: (x.split('_')[0], x.split('_')[1]))

        rows = []
        for user, res_pairs in user_results.items():
            result_map = {}
            for label, res in res_pairs:
                result_map[label] = {
                    'is_correct': res.is_correct,
                    'response_time': res.response_time
                }

            row = {
                'user': user,
                'result_map': result_map,
                'total_correct': sum(1 for r in result_map.values() if r['is_correct']),
                'flattened_results': []
            }

            # Align results with labels
            for label in sorted_labels:
                if label in result_map:
                    row['flattened_results'].append(result_map[label])
                else:
                    row['flattened_results'].append({'is_correct': None, 'response_time': None})

            rows.append(row)

        return render(request, 'controllerattend.html', {
            'rows': rows,
            'labels': sorted_labels
        })


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
        data = []

        # First, fetch 7 demo questions
        demo_questions = DemoQuestion.objects.order_by('?')[:7]

        # Add DB-stored options for each demo question
        for dq in demo_questions:
            demo_options = [
                dq.category,  # assumed correct
                dq.option1,
                dq.option2,
                dq.option3,
                dq.option4,
                dq.option5,
                dq.option6
            ]
            # Remove any None values if some options are blank
            demo_options = [opt for opt in demo_options if opt]
            random.shuffle(demo_options)
            data.append({
                'id': f'demo-{dq.id}',  # Mark as demo
                'image': dq.image.url,
                'options': demo_options
            })

        # Then fetch all real questions
        questions = PostQuestion.objects.order_by('?')

        for q in questions:
            options = [
                q.category,  # assumed correct
                q.option1,
                q.option2,
                q.option3,
                q.option4,
                q.option5,
                q.option6
            ]
            options = [opt for opt in options if opt]
            random.shuffle(options)
            data.append({
                'id': q.id,
                'image': q.image.url,
                'options': options
            })

        # Get Login ID from session
        login_id = request.session.get('user_id')
        if not login_id:
            return redirect('login')  

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
            question_id = data['QUESTIONID']
            user = User_Model.objects.get(id=data['USERID'])
            selected_answer = data['selected_answer']
            response_time = float(data['response_time'])

            # Check if it's a demo question
            if str(question_id).startswith('demo-'):
                # Remove the "demo-" prefix to get actual ID
                demo_id = str(question_id).replace('demo-', '')
                demo_question = DemoQuestion.objects.get(id=demo_id)

                is_correct = (selected_answer == demo_question.category)

                demo_result = DemoResult(
                    USERID=user,
                    QUESTIONID=demo_question,
                    response_time=response_time,
                    is_correct=is_correct
                )
                demo_result.save()

                return JsonResponse({'status': 'success', 'type': 'demo'})

            # If not a demo question, save in PostResult
            question = PostQuestion.objects.get(id=question_id)
            is_correct = (selected_answer == question.category)

            result = PostResult(
                USERID=user,
                QUESTIONID=question,
                response_time=response_time,
                is_correct=is_correct
            )
            result.save()

            return JsonResponse({'status': 'success', 'type': 'real'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'invalid request'}, status=405)
            

class PostOrSpontanious(View):
    def get(self, request):
        return render(request, 'postOrSpontanious.html')
    
from django.shortcuts import render
from django.views import View
from collections import defaultdict
from .models import PostResult, PostQuestion

# class PostAppeared(View):

#     def get(self, request):
#         results = PostResult.objects.filter(USERID__LOGINID__usertype='patient').select_related('USERID', 'QUESTIONID')
#         questions = list(PostQuestion.objects.order_by('id'))

#         user_results = defaultdict(lambda: [None] * len(questions))
#         question_id_index = {q.id: idx for idx, q in enumerate(questions)}

#         for res in results:
#             idx = question_id_index.get(res.QUESTIONID.id)
#             if idx is not None:
#                 user_results[res.USERID][idx] = res

#         rows = []
#         for user, answers in user_results.items():
#             total_correct = sum(1 for r in answers if r and r.is_correct)
#             rows.append({
#                 'user': user,
#                 'results': answers,
#                 'total_correct': total_correct
#             })

#         # --- New: Label categories like Happy1, Happy2, etc ---
#         category_count = defaultdict(int)
#         labeled_questions = []

#         for q in questions:
#             category_count[q.category] += 1
#             label = f"{q.category}{category_count[q.category]}"
#             labeled_questions.append({'question': q, 'label': label})

#         return render(request, 'Postappearedpatients.html', {
#             'rows': rows,
#             'questions': labeled_questions,
#         })




from collections import defaultdict
from django.views import View
from django.shortcuts import render

class PostAppeared(View):
    def get(self, request):
        # ======================
        # 1) POST RESULTS
        # ======================
        post_results = PostResult.objects.filter(
            USERID__LOGINID__usertype='patient'
        ).select_related('USERID', 'QUESTIONID')

        post_questions = list(PostQuestion.objects.order_by('id'))
        post_q_index = {q.id: idx for idx, q in enumerate(post_questions)}
        post_user_results = defaultdict(lambda: [None] * len(post_questions))

        for res in post_results:
            idx = post_q_index.get(res.QUESTIONID.id)
            if idx is not None:
                post_user_results[res.USERID][idx] = res

        post_rows = []
        for user, answers in post_user_results.items():
            total_correct = sum(1 for r in answers if r and r.is_correct)
            post_rows.append({
                'user': user,
                'results': answers,
                'total_correct': total_correct
            })

        post_category_count = defaultdict(int)
        post_labeled_questions = []
        for q in post_questions:
            post_category_count[q.category] += 1
            label = f"{q.category}{post_category_count[q.category]}"
            post_labeled_questions.append({'question': q, 'label': label})

        # ======================
        # 2) DEMO RESULTS
        # ======================
        demo_results = DemoResult.objects.filter(
            USERID__LOGINID__usertype='patient'
        ).select_related('USERID', 'QUESTIONID')

        demo_questions = list(DemoQuestion.objects.order_by('id'))
        demo_q_index = {q.id: idx for idx, q in enumerate(demo_questions)}
        demo_user_results = defaultdict(lambda: [None] * len(demo_questions))

        for res in demo_results:
            idx = demo_q_index.get(res.QUESTIONID.id)
            if idx is not None:
                demo_user_results[res.USERID][idx] = res

        demo_rows = []
        for user, answers in demo_user_results.items():
            total_correct = sum(1 for r in answers if r and r.is_correct)
            demo_rows.append({
                'user': user,
                'results': answers,
                'total_correct': total_correct
            })

        demo_category_count = defaultdict(int)
        demo_labeled_questions = []
        for q in demo_questions:
            demo_category_count[q.category] += 1
            label = f"{q.category}{demo_category_count[q.category]}"
            demo_labeled_questions.append({'question': q, 'label': label})

        # ======================
        # 3) RENDER BOTH TABLES
        # ======================
        return render(request, 'Postappearedpatients.html', {
            # post table
            'rows': post_rows,
            'questions': post_labeled_questions,
            # demo table
            'demo_rows': demo_rows,
            'demo_questions': demo_labeled_questions,
        })

    

class PostorSpontQuest(View):
    def get(self, request):
        return render(request, 'postorspontquest.html')
    
class ManagePostQuestView(View):
    def get(self, request):
        c = PostQuestion.objects.all()
        return render(request, 'managepostquest.html', {'c': c})
    
class DeletePostQuestion(View):
    def get(self, request, id):
        c = PostQuestion.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert("Question deleted successfully");window.location='/managepostquest'</script>''')
    
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
        results = PostResult.objects.filter(USERID__LOGINID__usertype='controller').select_related('USERID', 'QUESTIONID')
        questions = list(PostQuestion.objects.order_by('id'))

        user_results = defaultdict(lambda: [None] * len(questions))
        question_id_index = {q.id: idx for idx, q in enumerate(questions)}

        for res in results:
            idx = question_id_index.get(res.QUESTIONID.id)
            if idx is not None:
                user_results[res.USERID][idx] = res

        rows = []
        for user, answers in user_results.items():
            total_correct = sum(1 for r in answers if r and r.is_correct)
            rows.append({
                'user': user,
                'results': answers,
                'total_correct': total_correct
            })

        # 🆕 Label questions using category counts like Happy1, Happy2
        category_count = defaultdict(int)
        labeled_questions = []

        for q in questions:
            category_count[q.category] += 1
            label = f"{q.category}{category_count[q.category]}"
            labeled_questions.append({'question': q, 'label': label})

        return render(request, 'postappeardcontroller.html', {
            'rows': rows,
            'questions': labeled_questions
        })
    

class ControllerPostorSpontuser(View):
    def get(self, request):
        return render(request, 'Controller/postorspontquestion.html')
    
class Spontaneousinstruction(View):
    def get(self, request):
        c = Instructions_Model.objects.all()
        return render(request, 'Controller/spontaneousinstruction.html', {'c': c})
    

# from django.views import View
# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import SpontaniousQuestion, SpontaniousResult, User_Model
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# import json

# import random
# from django.views import View
# from django.shortcuts import render
# from .models import SpontaniousQuestion

# from django.views import View
# from django.shortcuts import render, HttpResponse
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from .models import SpontaniousQuestion, SpontaniousResult, User_Model
# import random, json


class SpontaniousQuestionView(View):
    def get(self, request):
        def fetch_random(category, subcategory):
            return list(
                SpontaniousQuestion.objects.filter(
                    Main_category__iexact=category,
                    Sub_category__iexact=subcategory
                )
            )

        # Step 1: Get Login ID from session
        login_id = request.session.get('user_id')
        if not login_id:
            return HttpResponse("Login ID not found in session", status=401)

        # Step 2: Resolve User_Model from Login ID
        try:
            user_model = User_Model.objects.get(LOGINID_id=login_id)
        except User_Model.DoesNotExist:
            return HttpResponse("User profile not found", status=404)

        # Step 3: Fetch question groups
        groups = [
            fetch_random("Without Occlusion", "High Intensity"),
            fetch_random("Without Occlusion", "Medium Intensity"),
            fetch_random("Without Occlusion", "Low Intensity"),
            fetch_random("With Occlusion", "High Intensity"),
            fetch_random("With Occlusion", "Medium Intensity"),
            fetch_random("With Occlusion", "Low Intensity"),
        ]

        for group in groups:
            random.shuffle(group)

        all_questions = sum(groups, [])

        data = [
            {
                "id": q.id,
                "image": q.image.url,
                "options": [q.category, q.option1, q.option2, q.option3, q.option4],
                "answer": q.category
            }
            for q in all_questions
        ]

        return render(request, 'Controller/spontaniousquestion.html', {
            'data': data,
            'user_id': user_model.id  # Correct USER ID from User_Model
        })



@method_decorator(csrf_exempt, name='dispatch')
class SubmitSpontaniousResultView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user_id = data.get('USERID')
            question_id = data.get('QUESTIONID')
            selected = data.get('selected_answer')
            response_time = data.get('response_time')

            if not all([user_id, question_id, selected, response_time]):
                return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)

            question = SpontaniousQuestion.objects.get(id=question_id)
            user = User_Model.objects.get(id=user_id)

            is_correct = (selected == question.category)

            result = SpontaniousResult.objects.create(
                USERID=user,
                QUESTIONID=question,
                response_time=response_time,
                is_correct=is_correct
            )

            return JsonResponse({'status': 'success', 'is_correct': is_correct})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)