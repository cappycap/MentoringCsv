import csv
from difflib import SequenceMatcher

class Participant:
    def __init__(self, data):
        self.name = data[1]
        self.pronouns = data[2]
        self.level = data[4]
        self.degree = data[5]
        self.role = data[6]
        self.support = set(data[7].split(", ")) if data[7] else set()
        self.mentor_count = 1 if data[8] == "One Person" else 2
        self.background = data[9] if self.role == "Mentor" else data[11]

    def is_higher_level(self, other):
        levels = ["Pre-Major", "Undergrad", "Graduate", "Alumni"]
        return levels.index(self.level) > levels.index(other.level)

def background_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def read_csv_data(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return [Participant(row) for row in reader]

def match_score(mentor, mentee):

    # Score comparing the background responses
    background_score = background_similarity(mentor.background, mentee.background)

    # Match based on support questions
    support_match = len(mentor.support.intersection(mentee.support))

    # Match based on degree
    degree_match = 1 if (mentor.degree == mentee.degree or 
                         (mentor.degree in ["BS in Computer Science", "MS in Computer Science"] and 
                          mentee.degree in ["BS in Computer Science", "MS in Computer Science"])) else 0
    
    return support_match + degree_match

def pair_participants(data):
    mentors = [p for p in data if p.role == "Mentor"]
    mentees = [p for p in data if p.role == "Mentee"]

    pairs = []
    for mentee in mentees:
        possible_mentors = [mentor for mentor in mentors if mentor.is_higher_level(mentee)]
        best_match = max(possible_mentors, key=lambda mentor: match_score(mentor, mentee), default=None)

        if best_match:
            pairs.append((mentee, best_match, match_score(best_match, mentee)))
            if best_match.mentor_count == 1:
                mentors.remove(best_match)
            else:
                best_match.mentor_count -= 1
    return sorted(pairs, key=lambda x: x[2], reverse=True)

if __name__ == "__main__":
    data = read_csv_data("data.csv")
    pairs = pair_participants(data)

    if not pairs:
        print("No pairings could be made.")
    else:
        for mentee, mentor, score in pairs:
            print(f"{mentee.name} (Mentee, {mentee.pronouns}) - {mentor.name} (Mentor, {mentor.pronouns}) - Match Score: {score}")
            print(f"Mentee Background: {mentee.background}")
            print(f"Mentor Background: {mentor.background}\n")
