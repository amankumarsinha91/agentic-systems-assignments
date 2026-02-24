class StudentMarks:
    def __init__(self, marks):
        self.marks = marks
    def last_three_avg(self):
        try:
            # Use negative indexing to get the last three marks
            last_three = self.marks[-3:]  # still safe to slice even if length<3, but we'll validate next
            if len(last_three) < 3:
                # Explicitly raise an exception to handle the "not enough marks" case
                raise IndexError("Not enough elements for last three average")
            avg = sum(last_three) / 3
            print(f"Average of last 3 marks is: {avg}")
        except (TypeError, ValueError):
            # In case marks contain non-numeric values
            print("Marks must be numeric to calculate average")
        except IndexError:
            print("Not enough marks to calculate average")


marks = [50, 60]
student = StudentMarks(marks)
student.last_three_avg()