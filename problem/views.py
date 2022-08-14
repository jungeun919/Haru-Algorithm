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
def crawling():
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
            problem_img = soup.select('#problem_description > p >img')
            if len(problem_img) > 0:
                print(problem_img[0].text)
            break

    problem_date = date.today()
    problem_data_set = {}

    if Problem.objects.filter(problem_date = problem_date):
        problem_set = Problem.objects.filter(problem_date = problem_date).first()

        sample_set = Example.objects.get(problem = problem_set)
        sample_input_set = sample_set.example_input.split('\'')
        del sample_input_set[0::2]
        sample_output_set = sample_set.example_output.split('\'')
        del sample_output_set[0::2]

        problem_data_set['problem_title'] = problem_set.problem_title
        problem_data_set['problem_description'] = problem_set.problem_text
        problem_data_set['problem_input'] = problem_set.problem_input
        problem_data_set['problem_output'] = problem_set.problem_output
        problem_data_set['problem_sample_input'] = sample_input_set
        problem_data_set['problem_sample_output'] = sample_output_set

        return problem_data_set
        
        # return render(request, 'problems.html', {
        #     'problem_title': problem_set.problem_title,
        #     'problem_description': problem_set.problem_text, 
        #     'problem_input': problem_set.problem_input,
        #     'problem_output': problem_set.problem_output,
        #     'problem_sample_input': sample_input_set,
        #     'problem_sample_output': sample_output_set,
        # })

    else: 
        try:    
            problem_title = soup.select('#problem_title')[0].text

            problem_description_cw = soup.select('#problem_description')
            problem_description = str(problem_description_cw)[1:-1]

            problem_input_cw = soup.select('#problem_input')
            problem_input = str(problem_input_cw)[1:-1]

            problem_output_cw = soup.select('#problem_output')
            problem_output = str(problem_output_cw)[1:-1]

            problem_sample_input_cw = soup.select('#sample-input-1')
            sample_input_list = []
            for sample_input in problem_sample_input_cw:
                sample_input_list.append(sample_input.text.strip())
            problem_sample_input_1 = sample_input_list[0].split('\n')
            problem_sample_input = [input.strip() for input in problem_sample_input_1]

            problem_sample_output = soup.select('#sample-output-1')
            sample_output_list = []
            for sample_output in problem_sample_output:
                sample_output_list.append(sample_output.text.strip())
            problem_sample_output_1 = sample_output_list[0].split('\n')
            problem_sample_output = [output.strip() for output in problem_sample_output_1]

            Problem(problem_date = problem_date,
                    problem_num = num,
                    problem_title = problem_title,
                    problem_text = problem_description,
                    problem_input = problem_input,
                    problem_output = problem_output).save()

            Example(problem = Problem.objects.get(problem_date=problem_date),
                    example_input = problem_sample_input,
                    example_output = problem_sample_output).save()

            problem_data_set = {}
            problem_data_set['problem_title'] = problem_set.problem_title
            problem_data_set['problem_description'] = problem_set.problem_text
            problem_data_set['problem_input'] = problem_set.problem_input
            problem_data_set['problem_output'] = problem_set.problem_output
            problem_data_set['problem_sample_input'] = sample_input_set
            problem_data_set['problem_sample_output'] = sample_output_set

            return problem_data_set

            # return render(request, 'problems.html', {
            #     'problem_title': problem_title,
            #     'problem_description': problem_description , 
            #     'problem_input': problem_input,
            #     'problem_output': problem_output,
            #     'problem_sample_input': problem_sample_input,
            #     'problem_sample_output': problem_sample_output,
            # })
        except:
            return redirect('problem')