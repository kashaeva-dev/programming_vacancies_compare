import os
from statistics import mean

from dotenv import load_dotenv, find_dotenv
from terminaltables import AsciiTable

from fetch_vacancies import fetch_vacancies_hh, fetch_vacancies_sj
from predict_salary import predict_salary_hh, predict_salary_sj


def get_salary_by_language_sj(languages, token):
    for language in languages:

        vacancies = fetch_vacancies_sj(language, token)
        salaries = []
        for vacancy in vacancies['vacancies']:
            salary = predict_salary_sj(vacancy)
            if salary:
                salaries.append(salary)
        if salaries:
            mean_salary = int(mean(salaries))
        else:
            mean_salary = 'Неизвестно'

        return [
                language,
                vacancies['found'],
                len(salaries),
                mean_salary,
            ]


def get_salary_by_language_hh(language):
    vacancies = fetch_vacancies_hh(language)
    salaries = []
    for vacancy in vacancies['vacancies']:
        salary = predict_salary_hh(vacancy)
        if salary:
            salaries.append(salary)
    if salaries:
        mean_salary = int(mean(salaries))
    else:
        mean_salary = 'Неизвестно'

    return [
        language,
        vacancies['found'],
        len(salaries),
        mean_salary,
    ]


def display_salary_table(salaries, table_title):
    headings = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
    ]]
    salaries_with_headings = headings + salaries
    table_instance = AsciiTable(salaries_with_headings, table_title)
    print(table_instance.table)
    print()


def main():
    languages = [
        'JavaScript', 'Java', 'Python', 'Ruby', 'PHP',
        'C++', 'C', 'Go', 'Swift', 'TypeScript', '1C',
    ]
    try:
        load_dotenv(find_dotenv())
        token = os.environ['SUPERJOB_KEY']
    except KeyError:
        print('Не получается найти переменную окружения SUPERJOB_KEY')
    else:
        salaries_by_languages_sj = []
        salaries_by_languages_hh = []
        for language in languages:
            salaries_by_languages_sj.append(get_salary_by_language_sj(language, token))
            salaries_by_languages_hh.append(get_salary_by_language_hh(language))
        display_salary_table(salaries_by_languages_sj, 'SuperJob Moscow')
        display_salary_table(salaries_by_languages_hh, 'HeadHunter Moscow')


if __name__ == "__main__":
    main()
