from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .forms import CodeExecutorForm
from post.models import Post
from .models import UserCheck
# from django.contrib.auth.models import User
from .compilerUtils import Compiler, Language, generate_test_case

from problem.models import Problem, Example
from datetime import date
from problem.views import crawling
from django.db.models import Q


def intro(request):
    return render(request, 'FE_templates/main2.html')

def aboutus(request):
    return render(request, 'FE_templates/aboutus.html')

# 컴파일 실행
def runCode(request):
    level = request.GET.get('level')
    problem_data_set = crawling(level)

    # 유저 판별 (최대 입력 횟수 : 2)
    if request.user.is_authenticated:
        login_user = request.user
        print("login_user:", login_user)
    else:
        print("User is not logged in.")

    template_data = {}

    # 오늘 날짜에 해당하는 문제 가져오기
    today = date.today()

    problem = Problem.objects.filter(problem_date=today, problem_level=level).first()
    example = Example.objects.get(problem=problem)

    if request.method == 'POST':
        if request.user.is_authenticated:
            login_user = request.user
            print("login_user:", login_user)

            if UserCheck.objects.all().filter(user=login_user, current_date=today, level=level):
                user = UserCheck.objects.all().filter(user=login_user, current_date=today, level=level).get()

            else: # 유저 없으면 저장
                user = UserCheck(
                    problem = problem,
                    user = login_user,
                    fail = 0, # 실패횟수
                    current_date = today,
                    level = level,
                    is_correct = 0
                )
                user.save()
            
        form = CodeExecutorForm(request.POST)

        if form.is_valid():
            executor = Compiler()
            # 입력 값, 테스트케이스 값 채우기
            code = form.cleaned_data['code']
            input_data = example.example_input
            expected_output = example.example_output

            input_string = input_data[1:-2]
            input_data = [x.strip("' ") for x in input_string.split(sep=",")]

            expected_string = expected_output[1:-2]
            expected_output = [x.strip("' ") for x in expected_string.split(sep=",")]

            test_case = generate_test_case(input_data, expected_output)

            executor.add_test_case(test_case)
            lan = Language(int(form.cleaned_data['language']))

            # 채점
            if lan == Language.PYTHON:
                executor.set_code(code)
                executor.set_language(lan)
                execution_result = executor.execute()

                template_data['result'] = execution_result.name
                executor.delete_code_file()
                if executor.hasExecuted:
                    checked_values = executor.compare_outputs()
                    if checked_values[0] == False:
                        if request.user.is_authenticated:
                            login_user = request.user
                            print("login_user:", login_user)
                            # 실패했을 경우에만 횟수 업데이트
                            user.fail += 1
                            user.current_date = today
                            user.save()
                            template_data['fail'] = user.fail

                    display_data = []
                    outputs = executor.get_output()
                    errors = executor.get_errors()
                    for i in range(len(outputs)):
                        if executor.hasErrors:
                            e = errors[i]
                        else:
                            e = "No errors!"
                        temp_tuple = (i+1, checked_values[i], outputs[i], e)
                        display_data.append(temp_tuple)
                    template_data['display_data'] = display_data

                    if template_data['result'] == 'ACC':
                        if request.user.is_authenticated:
                            login_user = request.user
                            print("login_user:", login_user)

                            # 게시물 저장 (회원)
                            post = Post()
                            post.problem = problem
                            post.code = request.POST['code']
                            post.pub_date = timezone.now()
                            post.disclosure = 'private'
                            post.writer = login_user.username
                            post.title = 0
                            post.body = 0
                            post.save()
                            
                            # 성공 여부 업데이트
                            user.is_correct = 1
                            user.save()
                        
                        else:
                            # 게시물 저장 (비회원)
                            post = Post()
                            post.problem = problem
                            post.code = request.POST['code']
                            post.pub_date = timezone.now()
                            post.disclosure = 'private'
                            post.writer = 0
                            post.title = 0
                            post.body = 0
                            post.save()

                        template_data['post_id'] = post.id
                        template_data['problem'] = post.problem
                        template_data['code'] = post.code
                        return render(request, 'FE_templates/correct.html', template_data)

                    else:                            
                        form = CodeExecutorForm()
                        template_data['form'] = form
                        template_data['level'] = level
                        template_data['problem_title'] = problem_data_set['problem_title']
                        template_data['problem_description'] = problem_data_set['problem_description']
                        template_data['problem_input'] = problem_data_set['problem_input']
                        template_data['problem_output'] = problem_data_set['problem_output']
                        template_data['problem_sample_input'] = problem_data_set['problem_sample_input']
                        template_data['problem_sample_output'] = problem_data_set['problem_sample_output']
                        
                        return render(request, 'FE_templates/incorrect1.html', template_data)                        

        else:
            return HttpResponse("Form is not valid")

    # 폼 띄우기
    else:
        form = CodeExecutorForm()
        template_data['form'] = form
        return render(request, 'FE_templates/index.html',
        {   
            'level': level,
            'form': template_data['form'],
            'problem_title': problem_data_set['problem_title'],
            'problem_description': problem_data_set['problem_description'], 
            'problem_input': problem_data_set['problem_input'], 
            'problem_output': problem_data_set['problem_output'], 
            'problem_sample_input': problem_data_set['problem_sample_input'],
            'problem_sample_output': problem_data_set['problem_sample_output'] 
        })
