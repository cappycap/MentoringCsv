# MentoringCsv

A python script for processing CSV outputs from our Mentoring Program Google Form.

It will organize a list of students into ideal pairings and report them in descending score.

Key code describing scoring:
```py
def match_score(mentor, mentee):

    # Score comparing the background responses, no max
    background_score = background_similarity(mentor.background, mentee.background)

    # Match based on support questions, max of 4
    support_match = len(mentor.support.intersection(mentee.support))

    # Match based on degree, max of 1
    degree_match = 1 if (mentor.degree == mentee.degree or 
                         (mentor.degree in ["BS in Computer Science", "MS in Computer Science"] and 
                          mentee.degree in ["BS in Computer Science", "MS in Computer Science"])) else 0
    
    return support_match, degree_match, background_score
```
Example output:
```
------------------------------------
Jane Mentee (mentee@wwu.edu, she/her/hers) - John Mentor (mentor@wwu.edu, he/him/his)
Support Match Score: 2
Degree Match Score: 0
Background Score: 1.00
Final Score: 3.00

Mentee Background: Just hoping to meet new people in the program!
Mentor Background: Happy to mentor anyone with a passion for computer science!
```