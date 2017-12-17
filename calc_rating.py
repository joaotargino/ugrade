#!/usr/bin/python

import requests
import sys
# import json

try:
    TOKEN = str(sys.argv[1])
except:
    TOKEN = ''
    
headers = {'Authorization': TOKEN, 'Content-Length': '0'}


# start_date 2016 jan 01(works if you started later,
# change if started before, adjust to see month by month)
STUDENTS_FEEDBACK_URL_ALL = \
    'https://review-api.udacity.com/api/v1/me/' \
    'student_feedbacks?start_date=2016-01-01'

print "Calculating..."
# print "\n=================================="
feedback_history = requests.get(STUDENTS_FEEDBACK_URL_ALL, headers=headers)
# print "Student Feedback\n" + json.dumps(feedback_history.json(),
#                                         indent=4, sort_keys=True)
# print "=================================="
feedback_history = feedback_history.json()

dict_ratings = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}

for feedback in feedback_history:
    dict_ratings[feedback["rating"]] += 1

print "Number of ratings: %d" % len(feedback_history)
print dict_ratings

grade = dict_ratings[5] * 5 + dict_ratings[4] * 4 + dict_ratings[3] * 3 \
        + dict_ratings[2] * 2 + dict_ratings[1]
grade = float(grade) / len(feedback_history)

# round to 2 decimals, uncoment last line to see full
print "Your grade as a Project Reviewer is: %.2f" % round(grade, 2)
print grade
