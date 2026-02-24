class StudentPerformance:
    def __init__(self, scores):
       self.scores = scores

    def score_difference(self):
        try:
            # Access first and last elements using indexing
            first = self.scores[0]
            last = self.scores[-1]
            diff = last - first
            print(f"Difference between last and first score is: {diff}")
        except IndexError:
            # Triggered when the list is empty (no index 0 or -1)
            print("No scores available to calculate difference")
        except (TypeError, ValueError):
            # Handles non-numeric entries gracefully
            print("Scores must be numeric to calculate difference")


# ---- Example Usage ----
scores = [55, 65, 75, 85]
student = StudentPerformance(scores)
student.score_difference()  # Expected: Difference between last and first score is: 30