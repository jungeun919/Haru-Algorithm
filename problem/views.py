from imp import reload
from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
from datetime import date
from .models import *
import random
import requests
from django.db.models import Q

# Create your views here.
def list_crawling(level):
    if level == 'bronze': 
        bronze = []
        for problem_level in range(1, 6):
            for page in range(1, 3):
                url = f'https://solved.ac/problems/level/{problem_level}?page={page}'
                response = requests.get(url)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                problem_level_table = soup.select('.css-q9j30p > span')
                for plt in problem_level_table:
                    if plt.get('class') != None:
                        problem_level_table.remove(plt)
                for i in problem_level_table:
                    bronze.append(i.text)
        if Level.objects.all().count() == 0:
            Level(bronze = list(map(int, bronze))).save()
        else:
            Level.objects.all().update(bronze = list(map(int, bronze)))
    elif level == 'silver':
        silver = []
        for problem_level in range(6, 11):
            for page in range(1, 3):
                url = f'https://solved.ac/problems/level/{problem_level}?page={page}'
                response = requests.get(url)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                problem_level_table = soup.select('.css-q9j30p > span')
                for plt in problem_level_table:
                    if plt.get('class') != None:
                        problem_level_table.remove(plt)
                for i in problem_level_table:
                    silver.append(i.text)  
        if Level.objects.all().count() == 0:
            Level(silver = list(map(int, silver))).save()
        else:
            Level.objects.all().update(silver = list(map(int, silver)))              
        # print(len(list(map(int, silver))))
    elif level == 'gold':
        gold = []
        for problem_level in range(11, 16):
            for page in range(1, 3):
                url = f'https://solved.ac/problems/level/{problem_level}?page={page}'
                response = requests.get(url)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                problem_level_table = soup.select('.css-q9j30p > span')
                for plt in problem_level_table:
                    if plt.get('class') != None:
                        problem_level_table.remove(plt)
                for i in problem_level_table:
                    gold.append(i.text)
        if Level.objects.all().count() == 0:
            Level(gold = list(map(int, gold))).save()
        else:
            Level.objects.all().update(gold = list(map(int, gold)))
        # print(len(list(map(int, gold))))
    elif level == 'platinum':
        platinum = []
        for problem_level in range(16, 21):
            for page in range(1, 3):
                url = f'https://solved.ac/problems/level/{problem_level}?page={page}'
                response = requests.get(url)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                problem_level_table = soup.select('.css-q9j30p > span')
                for plt in problem_level_table:
                    if plt.get('class') != None:
                        problem_level_table.remove(plt)
                for i in problem_level_table:
                    platinum.append(i.text)
        if Level.objects.all().count() == 0:
            Level(platinum = list(map(int, platinum))).save()
        else:
            Level.objects.all().update(platinum = list(map(int, platinum)))
        # print(len(list(map(int, platinum))))
    elif level == 'diamond':
        diamond = []
        for problem_level in range(21, 26):
            for page in range(1, 3):
                url = f'https://solved.ac/problems/level/{problem_level}?page={page}'
                response = requests.get(url)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                problem_level_table = soup.select('.css-q9j30p > span')
                for plt in problem_level_table:
                    if plt.get('class') != None:
                        problem_level_table.remove(plt)
                for i in problem_level_table:
                    diamond.append(i.text)
        if Level.objects.all().count() == 0:
            Level(diamond = list(map(int, diamond))).save()
        else:
            Level.objects.all().update(diamond = list(map(int, diamond)))
        # print(len(list(map(int, diamond))))
    elif level == 'ruby':
        ruby = []
        for problem_level in range(26, 31):
            for page in range(1, 3):
                url = f'https://solved.ac/problems/level/{problem_level}?page={page}'
                response = requests.get(url)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                problem_level_table = soup.select('.css-q9j30p > span')
                for plt in problem_level_table:
                    if plt.get('class') != None:
                        problem_level_table.remove(plt)
                for i in problem_level_table:
                    ruby.append(i.text)
        if Level.objects.all().count() == 0:
            Level(ruby = list(map(int, ruby))).save()
        else:
            Level.objects.all().update(ruby = list(map(int, ruby)))
        # print(len(list(map(int, ruby))))
    


def crawling(level):
    if Level.objects.all().count() == 0:
        list_crawling(level)
    else:
        if level == 'bronze':
            if Level.objects.all().first().bronze == None:
                list_crawling(level)
        elif level == 'silver':
            if Level.objects.all().first().silver == None:
                list_crawling(level)
        elif level == 'gold':
            if Level.objects.all().first().gold== None:
                list_crawling(level)
        elif level == 'platinum':
            if Level.objects.all().first().platinum == None:
                list_crawling(level)
        elif level == 'diamond':
            if Level.objects.all().first().diamond == None:
                list_crawling(level)
        elif level == 'ruby':
            if Level.objects.all().first().ruby == None:
                list_crawling(level)

    level_list_set = Level.objects.all().first()
    if level == 'bronze':
        level_list = list(map(int, level_list_set.bronze[1:-1].split(', ')))
    if level == 'silver':
        level_list = list(map(int, level_list_set.silver[1:-1].split(', ')))
    if level == 'gold':
        level_list = list(map(int, level_list_set.gold[1:-1].split(', ')))
    if level == 'platinum':
        level_list = list(map(int, level_list_set.platinum[1:-1].split(', ')))
    if level == 'diamond':
        level_list = list(map(int, level_list_set.diamond[1:-1].split(', ')))
    if level == 'ruby':
        level_list = list(map(int, level_list_set.ruby[1:-1].split(', ')))
    print(level_list)

    while True:
        num = str(random.choice(level_list))
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
    problem_data_set = {}

    if Problem.objects.filter(problem_date = problem_date, problem_level = level):
        problem_set = Problem.objects.filter(problem_date = problem_date, problem_level = level).first()

        sample_set = Example.objects.get(problem = problem_set)
        sample_input_set = sample_set.example_input.split('\'')
        del sample_input_set[0::2]
        sample_output_set = sample_set.example_output.split('\'')
        del sample_output_set[0::2]

        problem_data_set = {
            'problem_title': problem_set.problem_title,
            'problem_description': problem_set.problem_text, 
            'problem_input': problem_set.problem_input,
            'problem_output': problem_set.problem_output,
            'problem_sample_input': sample_input_set,
            'problem_sample_output': sample_output_set
        }
        return problem_data_set

    else: 
        try:   
            problem_title = soup.select('#problem_title')[0].text
            print(problem_title)

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
                    problem_level = level,
                    problem_title = problem_title,
                    problem_text = problem_description,
                    problem_input = problem_input,
                    problem_output = problem_output).save()

            Example(problem = Problem.objects.filter(problem_date=problem_date, problem_level=level)[0],
                    example_input = problem_sample_input,
                    example_output = problem_sample_output).save()

            problem_data_set = {
                'problem_title': problem_title,
                'problem_description': problem_description, 
                'problem_input': problem_input,
                'problem_output': problem_output,
                'problem_sample_input': problem_sample_input,
                'problem_sample_output': problem_sample_output
            }
            return problem_data_set

        except Problem.DoesNotExist:
            return redirect('/')