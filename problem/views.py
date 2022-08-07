from imp import reload
from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
from datetime import date
from .models import *
import random
import requests

# Create your views here.
def intro(request):
    return render(request, 'intro.html')

def problem(request):
    while True:
        num = str(random.randrange(1000, 25377))
        base = 'https://www.acmicpc.net/problem/'
        url = base + num
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        try:
            problem_language = soup.select('.problem-label-multilang')[0].text
            if problem_language == '다국어':
                continue
        except:
            break

    problem_date = date.today()

    if Problem.objects.filter(problem_date = problem_date):
        problem_set = Problem.objects.filter(problem_date = problem_date).first()

        description_list_set = problem_set.problem_text.split('\'')
        del description_list_set[0::2]
        input_list_set = problem_set.problem_input.split('\'')
        del input_list_set[0::2]
        output_list_set = problem_set.problem_output.split('\'')
        del output_list_set[0::2]

        sample_set = Example.objects.get(problem = problem_set)
        sample_input_set = sample_set.example_input.replace('\r', '').split('\'')
        del sample_input_set[0::2]
        sample_output_set = sample_set.example_output.split('\'')
        del sample_output_set[0::2]

        return render(request, 'problems.html', {
            'problem_title': problem_set.problem_title,
            'description_list': description_list_set, 
            'input_list': input_list_set,
            'output_list': output_list_set,
            'problem_sample_input': sample_input_set,
            'problem_sample_output': sample_output_set,
        })
    else: 
        try:    
            problem_title = soup.select('#problem_title')[0].text

            problem_description = soup.select('#problem_description > p')
            description_list = []
            for description in problem_description:
                description_list.append(description.text)

            problem_input = soup.select('#problem_input > p')
            input_list = []
            for input in problem_input:
                input_list.append(input.text)

            problem_output = soup.select('#problem_output > p')
            output_list = []
            for output in problem_output:
                output_list.append(output.text)

            problem_sample_input = soup.select('#sample-input-1')
            sample_input_list = []
            for sample_input in problem_sample_input:
                sample_input_list.append(sample_input.text.strip())
            problem_sample_input = sample_input_list[0].split('\n')

            problem_sample_output = soup.select('#sample-output-1')
            sample_output_list = []
            for sample_output in problem_sample_output:
                sample_output_list.append(sample_output.text.strip())
            problem_sample_output = sample_output_list[0].split('\n')

            Problem(problem_date = problem_date,
                    problem_num = num,
                    problem_title = problem_title,
                    problem_text = description_list,
                    problem_input = input_list,
                    problem_output = output_list).save()

            Example(problem = Problem.objects.get(problem_date=problem_date),
                    example_input = problem_sample_input,
                    example_output = problem_sample_output).save()

            return render(request, 'problems.html', {
                'problem_title': problem_title,
                'description_list': description_list, 
                'input_list': input_list,
                'output_list': output_list,
                'problem_sample_input': problem_sample_input,
                'problem_sample_output': problem_sample_output,
            })
        except:
            return redirect('problem')