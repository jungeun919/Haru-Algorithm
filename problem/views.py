from django.shortcuts import redirect
from bs4 import BeautifulSoup
from datetime import date
from .models import *
import random
import requests
import urllib.request
import json

def fetch_problems_for_level(level):
    level_ranges = {
        'bronze': (1, 6),
        'silver': (6, 11),
        'gold': (11, 16),
        'platinum': (16, 21),
        'diamond': (21, 26),
        'ruby': (26, 31)
    }

    problems = []
    if level in level_ranges:
        problems = []
        base_url = 'https://solved.ac/problems/level/{}?page={}'
        for level_num in range(*level_ranges[level]):
            for page in range(1, 3):
                response = requests.get(base_url.format(level_num, page))
                if response.status_code == 200:
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    problem_num = soup.select('.css-q9j30p')[0].text
                    problems.append(problem_num)
    return problems

def list_crawling(level):
    problems = fetch_problems_for_level(level)
    
    # create or update level objects
    level_object, created = Level.objects.get_or_create()
    setattr(level_object, level, problems)
    level_object.save()

def category_api(num):
    url = f'https://solved.ac/api/v3/problem/show?problemId={num}'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    if response.getcode() == 200:
        response_body = response.read()
        problem_api_str = response_body.decode('utf-8')
        problem_api = json.loads(problem_api_str)
        category_list = []
        for category in problem_api['tags']:
            category_list.append(category['displayNames'][0]['name'])
    return category_list

def get_problem_data_from_db(problem_date, level):
    problem_set = Problem.objects.filter(problem_date = problem_date, problem_level = level).first()

    if not problem_set:
        return None

    sample_set = Example.objects.get(problem = problem_set)
    sample_input_set = sample_set.example_input.split('\'')[1::2]
    sample_output_set = sample_set.example_output.split('\'')[1::2]

    problem_data_set = {
        'problem_title': problem_set.problem_title,
        'problem_category': problem_set.problem_category,
        'problem_description': problem_set.problem_text, 
        'problem_input': problem_set.problem_input,
        'problem_output': problem_set.problem_output,
        'problem_sample_input': sample_input_set,
        'problem_sample_output': sample_output_set
    }
    return problem_data_set

def get_problem_html(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def parse_problem_data(html, num):
    soup = BeautifulSoup(html, 'html.parser')
    
    problem_title = soup.select_one('#problem_title').text

    problem_category = str(category_api(num))[1:-1].replace('\'', '')

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

    problem_data = {
        'problem_title': problem_title,
        'problem_category': problem_category,
        'problem_description': problem_description, 
        'problem_input': problem_input,
        'problem_output': problem_output,
        'problem_sample_input': problem_sample_input,
        'problem_sample_output': problem_sample_output
    }
    return problem_data

def save_problem_and_example(problem_data, problem_date, level, num):
    Problem(problem_date = problem_date,
        problem_num = num,
        problem_level = level,
        problem_title = problem_data['problem_title'],
        problem_category = problem_data['problem_category'],
        problem_text = problem_data['problem_description'],
        problem_input = problem_data['problem_input'],
        problem_output = problem_data['problem_output']).save()

    Example(problem = Problem.objects.filter(problem_date=problem_date, problem_level=level)[0],
            example_input = problem_data['problem_sample_input'],
            example_output = problem_data['problem_sample_output']).save()

def get_today_problem_data(level):
    problem_date = date.today()
    problem_data_set = get_problem_data_from_db(problem_date, level)

    if problem_data_set:
        return problem_data_set
    else:
        level_obj = Level.objects.first()
        if not level_obj or getattr(level_obj, level, None) is None:
            list_crawling(level)
            level_obj = Level.objects.first()
        
        level_data = getattr(level_obj, level, "")
        level_list = [problem.strip('\'') for problem in level_data[1:-1].split(', ')]

        num = str(random.choice(level_list))
        base = 'https://www.acmicpc.net/problem/'
        url = base + num
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

        try:
            html = get_problem_html(url, headers)
            if html:
                problem_data = parse_problem_data(html, num)
                save_problem_and_example(problem_data, problem_date, level, num)
                return problem_data
        
        except Exception:
            return redirect('/')