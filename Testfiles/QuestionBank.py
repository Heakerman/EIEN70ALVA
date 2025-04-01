class QuestionBank:
    def __init__(self):
        self.questions = [
            {"id": 1, "question": "What is your favorite color?", "answers": ["Red", "Blue", "Green", "Yellow", "Black"]},
            {"id": 2, "question": "Which drink do you prefer?", "answers": ["Coffee", "Tea", "Soda", "Water", "Milk"]},
            {"id": 3, "question": "What is your most used mode of transportation?", "answers": ["Car", "Bicycle", "Train", "Bus", "Electric scooter"]},
            {"id": 4, "question": "What time of day do you prefer to exercise?", "answers": ["Morning", "Afternoon", "Evening", "Night", "I don't exercise"]},
            {"id": 5, "question": "Which genre of music do you like the most?", "answers": ["Pop", "Rock", "Jazz", "Classical", "Hip-hop"]},
            {"id": 6, "question": "Which type of vacation do you prefer?", "answers": ["Beach", "Mountain", "City", "Countryside", "Cruise"]},
            {"id": 7, "question": "What is your favorite season?", "answers": ["Winter", "Spring", "Summer", "Fall", "I don't have a favorite"]},
            {"id": 8, "question": "Which sport do you enjoy the most?", "answers": ["Football", "Basketball", "Tennis", "Swimming", "Running"]},
            {"id": 9, "question": "What is your favorite type of cuisine?", "answers": ["Italian", "Chinese", "Mexican", "Indian", "American"]},
            {"id": 10, "question": "How often do you travel for work?", "answers": ["Never", "Rarely", "Occasionally", "Often", "Always"]},
            {"id": 11, "question": "What is your preferred social activity?", "answers": ["Movies", "Dinner with friends", "Sports", "Reading", "Video games"]},
            {"id": 12, "question": "What is your dream job?", "answers": ["Engineer", "Doctor", "Artist", "Teacher", "Entrepreneur"]},
            {"id": 13, "question": "How many hours of sleep do you get on average?", "answers": ["Less than 4", "4-6 hours", "6-8 hours", "8-10 hours", "More than 10 hours"]},
            {"id": 14, "question": "What is your favorite type of movie?", "answers": ["Action", "Comedy", "Drama", "Horror", "Sci-fi"]},
            {"id": 15, "question": "How often do you eat out?", "answers": ["Never", "Once a week", "2-3 times a week", "4-5 times a week", "Every day"]},
            {"id": 16, "question": "Which of these do you prefer to do on weekends?", "answers": ["Relax at home", "Go hiking", "Watch TV", "Party with friends", "Work on hobbies"]},
            {"id": 17, "question": "How do you prefer to commute to work?", "answers": ["Car", "Public transport", "Bicycle", "Walk", "Work from home"]},
            {"id": 18, "question": "Which of these would you most likely invest in?", "answers": ["Stocks", "Real estate", "Cryptocurrency", "Startups", "Bonds"]},
            {"id": 19, "question": "What is your ideal weekend getaway?", "answers": ["Beach", "Mountain", "City tour", "Countryside", "Theme park"]},
            {"id": 20, "question": "What kind of books do you like to read?", "answers": ["Fiction", "Non-fiction", "Biographies", "Science fiction", "Fantasy"]}
        ]
        self.current_index = 0  # Starts at the first question (index 0, id 1)

    def get_current_question(self):
        """Returns the current question."""
        return self.questions[self.current_index]

    def next_question(self):
        """Moves to the next question if available."""
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
        else:
            self.current_index = 0  # Loop back to the first question if at the end
        return self.get_current_question()
