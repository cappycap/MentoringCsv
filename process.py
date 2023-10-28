import csv
from difflib import SequenceMatcher

class Participant:
    def __init__(self, data):
        self.name = data[1]
        self.pronouns = data[3]
        self.email = data[2]
        self.level = data[4]
        self.degree = data[5]
        self.role = data[6]
        self.support = set(data[7].split(", ")) if self.role == "Mentor" else set(data[10].split(", "))
        self.mentor_count = 1 if data[8] == "One Person" else 2
        self.background = data[9] if self.role == "Mentor" else data[11]

    def is_higher_level(self, other):
        levels = ["Pre-Major", "Undergrad", "Graduate", "Alumni"]
        return levels.index(self.level) > levels.index(other.level)

def background_similarity(a, b):
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())
    return len(a_words.intersection(b_words))

def read_csv_data(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return [Participant(row) for row in reader]

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
def pair_participants(data):
    mentors = [p for p in data if p.role == "Mentor"]
    mentees = [p for p in data if p.role == "Mentee"]

    pairs = []

    for mentee in mentees:
        possible_mentors = [mentor for mentor in mentors if mentor.is_higher_level(mentee)]

        # Compute the match score and final score within the key function
        def compute_score(mentor):
            support_match, degree_match, background_score = match_score(mentor, mentee)
            final_score = support_match + degree_match + background_score
            return final_score

        best_match = max(possible_mentors, key=compute_score, default=None)

        if best_match:
            pairs.append((mentee, best_match, match_score(best_match, mentee)))
            if best_match.mentor_count == 1:
                mentors.remove(best_match)
            else:
                best_match.mentor_count -= 1

    return sorted(pairs, key=lambda x: sum(x[2]), reverse=True)

if __name__ == "__main__":
    data = read_csv_data("data.csv")
    pairs = pair_participants(data)

    if not pairs:
        print("No pairings could be made.")
    else:
        for mentee, mentor, scores in pairs:
            support_match, degree_match, background_score = scores
            final_score = support_match + degree_match + background_score
            print(f"------------------------------------")
            print(f"{mentee.name} ({mentee.email}, {mentee.pronouns}) - {mentor.name} ({mentor.email}, {mentor.pronouns})")
            print(f"Support Match Score: {support_match}")
            print(f"Degree Match Score: {degree_match}")
            print(f"Background Score: {background_score:.2f}")
            print(f"Final Score: {final_score:.2f}\n")
            print(f"Mentee Background: {mentee.background}")
            print(f"Mentor Background: {mentor.background}\n")
