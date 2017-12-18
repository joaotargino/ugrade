#!/usr/bin/python

import requests
import sys
import json


def rating_by_project(project_name):
    for student_feedback in feedback_history:
        dict_ratings[student_feedback["rating"]] += 1
        if student_feedback["project"]["name"] == project_name:
            dict_project[student_feedback["rating"]] += 1

    grade_project = dict_project[5] * 5 + dict_project[4] * 4 + dict_project[
        3] * 3 + dict_project[2] * 2 + dict_project[1]
    total_feedback_by_project = sum(dict_project.values())
    if total_feedback_by_project > 0:
        grade_project = float(grade_project) / sum(dict_project.values())
        # print dict_project
        print "    - %s is: %s in a total of %d ratings" % (
            project_name, getColor(round(grade_project, 2)),
            total_feedback_by_project)


def getColor(grade):
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    if grade <= 3.0:
        color = RED
    elif grade <= 4.20:
        color = BLUE
    else:
        color = GREEN
    return "\x1b[1;%dm" % (30 + color) + "%.2f" % grade + "\x1b[0m"


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

STUDENTS_FEEDBACK_URL_ALL = \
    'https://review-api.udacity.com/api/v1/me/' \
    'student_feedbacks?start_date=%s&end_date=%s' % (start_date, end_date)

print "Calculating..."
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

dict_ratings = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}

for feedback in feedback_history:
    dict_ratings[feedback["rating"]] += 1

print "Number of ratings: %d" % len(feedback_history)
print dict_ratings

grade = dict_ratings[5] * 5 + dict_ratings[4] * 4 + dict_ratings[3] * 3 \
        + dict_ratings[2] * 2 + dict_ratings[1]
grade = float(grade) / len(feedback_history)

# round to 2 decimals, uncoment last line to see full
print "Your grade as a Project Reviewer is: %s" % getColor(round(grade, 2))
# print grade

project_list = []
for project in certification:
    if project["status"] == "certified":
        project_list.append(project["project"]["name"])

print "Your grade as a Project Reviewer of:"
for project in project_list:
    dict_project = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    rating_by_project(project)
