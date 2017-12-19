#!/usr/bin/python

import requests
import sys


# import json


def rating_by_project(project_name, d_submissions):
    for student_feedback in feedback_history:
        dict_ratings[student_feedback["rating"]] += 1
        if student_feedback["project"]["name"] == project_name:
            dict_project[student_feedback["rating"]] += 1

    grade_project = dict_project[5] * 5 + dict_project[4] * 4 + dict_project[
        3] * 3 + dict_project[2] * 2 + dict_project[1]
    total_feedback_by_project = sum(dict_project.values())
    total_reviews = d_submissions.get(project_name)
    if total_feedback_by_project > 0:
        grade_project = float(grade_project) / sum(dict_project.values())
        # print dict_project
        print "    - %s is: %s in a total of %d ratings out of %s reviews " \
              "(%s%% feedback)" % (
                  get_color(project_name), get_color(round(grade_project, 2)),
                  total_feedback_by_project, total_reviews,
                  calc_percentage(total_feedback_by_project, total_reviews))


def get_total_reviews(submissions):
    d_submissions = {}
    for submission in submissions:
        if submission["result"] == "passed" or \
                submission["result"] == "failed":
            if submission["project"]["name"] in d_submissions.keys():
                d_submissions[submission["project"]["name"]] += 1
            else:
                d_submissions[submission["project"]["name"]] = 0
    return d_submissions


def calc_percentage(feedback_project, total_n_reviews):
    return "%.2f" % float(feedback_project * 100 / float(total_n_reviews))


def get_color(current_grade):
    black, red, green, yellow, blue, magenta, cyan, white = range(8)
    if isinstance(current_grade, basestring):
        return "\x1b[1;%dm" % (30 + cyan) + "%s" % current_grade + "\x1b[0m"
    elif current_grade <= 3.0:
        color = red
    elif grade <= 4.20:
        color = blue
    else:
        color = green
    return "\x1b[1;%dm" % (30 + color) + "%.2f" % current_grade + "\x1b[0m"


try:
    TOKEN = str(sys.argv[1])
except IndexError:
    TOKEN = "replace"
    if TOKEN == "replace":
        print "please insert your token above or as parameter:"
        print "use the command:$    python calc_rating.py your_token"
        sys.exit()

headers = {'Authorization': TOKEN, 'Content-Length': '0'}

# start_date 2016 jan 01(works if you started later,
# change if started before, adjust to see month by month)
start_date = "2001-01-28"
end_date = "2042-01-28"

q = raw_input('Want to filter by date? (y/N) ')

if q.upper() != "N" and q != "":
    start_date = raw_input('Enter the start date (yyyy-mm-dd): ')
    end_date = raw_input('Enter the end date (yyyy-mm-dd): ')

STUDENTS_FEEDBACK_URL_ALL = \
    'https://review-api.udacity.com/api/v1/me/' \
    'student_feedbacks?start_date=%s&end_date=%s' % (start_date, end_date)

print "Calculating... This may take a while... So, what's up?"
# print "\n=================================="
feedback_history = requests.get(STUDENTS_FEEDBACK_URL_ALL, headers=headers)

# print "Student Feedback\n" + json.dumps(feedback_history.json(),
#                                         indent=4, sort_keys=True)
# print "=================================="
feedback_history = feedback_history.json()

CERTIFICATIONS_URL = 'https://review-api.udacity.com' \
                     '/api/v1/me/certifications.json'
certification = requests.get(CERTIFICATIONS_URL, headers=headers)
# print "Certified: \n" + json.dumps(certification.json(),
#                                    indent=4, sort_keys=True)
certification = certification.json()

# print "=================================="

SUBMISSIONS_COMPLETED_URL = 'https://review-api.udacity.com/api/' \
                            'v1/me/submissions/completed'
submissions_completed = requests.get(SUBMISSIONS_COMPLETED_URL,
                                     headers=headers)
submissions_completed = submissions_completed.json()

dict_submissions = get_total_reviews(submissions_completed)

dict_ratings = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

for feedback in feedback_history:
    dict_ratings[feedback["rating"]] += 1

total_reviews = sum(dict_submissions.values())
print "Number of ratings: %d out of %s reviews " \
      "(%s%% feedback) " % (len(feedback_history), total_reviews,
                            calc_percentage(
                                len(feedback_history), total_reviews))
# print dict_ratings
for g in dict_ratings:
    print "%s stars received: %s (%s%%)" % (str(g), str(dict_ratings[g]),
                                            calc_percentage(dict_ratings[g],
                                                            total_reviews))

grade = dict_ratings[5] * 5 + dict_ratings[4] * 4 + dict_ratings[3] * 3 \
        + dict_ratings[2] * 2 + dict_ratings[1]
grade = float(grade) / len(feedback_history)

# round to 2 decimals, uncoment last line to see full
print "Your grade as a Project Reviewer is: %s" % get_color(round(grade, 2))
# print grade

project_list = []
for project in certification:
    if project["status"] == "certified":
        project_list.append(project["project"]["name"])

print "Your grade as a Project Reviewer of:"
for project in project_list:
    dict_project = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    rating_by_project(project, dict_submissions)
