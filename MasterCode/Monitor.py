import threading
from QuestionBank import QuestionBank

class Monitor:
    def __init__(self,condition):
        self.qbank = QuestionBank()  # Initialize the question bank
        self.current_q = self.qbank.get_current_question()
        self.current_question = self.current_q['question']
        self.current_answers = self.current_q['answers']
        self.lock = threading.Lock()  # Initialize a lock to synchronize access
        self.GraphUpdated = False  # Flag to indicate if the question and answers have changed
        self.robotBusy = False  # Flag to indicate if the robot is busy
        self.robotInteger = -1  # Integer of the robot, -1 indicates idle
        self.robotIntegerHasBeenSet = False  # Flag to indicate if the robot Integer has been set
        self.condition = condition
        self.bucketSensor = False  # Flag to indicate if the bucket sensor is triggered

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

    def getA(self):
        """Returns the current answers."""
        with self.lock:
            return self.current_answers

    def try_send_to_robot(self, x):
        """Attempts to send an integer to the robot."""
        if not self.robotBusy:
            with self.lock:
                self.robotInteger = x
                self.robotIntegerHasBeenSet = True
                self.robotBusy = True
                
            with self.condition:
                self.condition.notify()
        else:
            print("Busy")

    def get_robot_Integer(self):
        """Returns the robot Integer to the robot"""
        if(self.robotIntegerHasBeenSet):
            with self.lock:
                return self.robotInteger
        else:
            return -1
        
    def robot_acknowledge(self):
        """Resets the robot Integer."""
        with self.lock:
            self.robotInteger = -1
            self.robotIntegerHasBeenSet = False
            self.robotBusy = False
        
    def set_bucketSensor(self, value):
        """Sets the bucket sensor flag."""
        with self.lock:
            self.bucketSensor = value

    def get_bucketSensor(self):
        """Returns the bucket sensor flag."""
        with self.lock:
            return self.bucketSensor
