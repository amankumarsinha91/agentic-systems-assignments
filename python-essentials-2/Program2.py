class StudentScores:
    def __init__(self, scores):
       self.scores = scores

    def highest_last_two(self):
        try:
            # Get the last two scores using negative indexing (slice)
            last_two = self.scores[-2:]
            if len(last_two) < 2:
                # Explicitly trigger the error path if fewer than two scores exist
                raise IndexError("Not enough scores")
            
            highest = max(last_two)
            print(f"Highest score among last two is: {highest}")
        except IndexError:
            print("Not enough scores to find highest value")
        except (TypeError, ValueError):
            # Handles cases where scores may contain non-numeric values
            print("Scores must be numeric to find highest value")


# ---- Example Usage ----
scores = [45, 67, 89, 72]
student = StudentScores(scores)
student.highest_last_two()  # Expected: Highest score among last two is: 89