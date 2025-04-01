import threading
from QuestionBank import QuestionBank

class Monitor:
    def __init__(self):
        self.qbank = QuestionBank()  # Initialize the question bank
        self.current_q = self.qbank.get_current_question()
        self.current_question = self.current_q['question']
        self.current_answers = self.current_q['answers']
        self.lock = threading.Lock()  # Initialize a lock to synchronize access
        self.GraphUpdated = False  # Flag to indicate if the question and answers have changed

    def nextQandA(self):
        """Updates the current question and answers to the next one."""
        with self.lock:  # Acquire the lock to ensure mutual exclusion
            # Move to the next question
            self.qbank.next_question()
            # Get the current question and answers from the QuestionBank
            self.current_q = self.qbank.get_current_question()
            self.current_question = self.current_q['question']
            self.current_answers = self.current_q['answers']
            self.GraphUpdated = True  # Set the updated flag to True

    def getQandA(self):
        """Returns the current question and answers."""
        with self.lock:  # Acquire the lock to ensure mutual exclusion
            return self.current_question, self.current_answers

    def reset_update_flag(self):
        """Resets the update flag after the Graphics thread has processed it."""
        self.GraphUpdated = False
