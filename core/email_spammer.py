import pickle


class EmailSpammner:
    
    def __init__(self, message):
        self.message = [message]
        self.model_cls = "/home/antares/Documents/anka/Job/Hidup/MachineLearning/dataset/World/Email-filtering/Model_1/email_spam.pkl"
        self.vectorizer = "/home/antares/Documents/anka/Job/Hidup/MachineLearning/dataset/World/Email-filtering/Model_1/vectorizer.pkl"


    def vectorizerMessage(self):
        with open(self.vectorizer, 'rb') as file:
            model = pickle.load(file)

        # Change the message into numeric features (2D-Array)
        message = model.transform(self.message).toarray()
        return message
    
    def predictor(self):
        with open(self.model_cls, 'rb') as file:
            model = pickle.load(file)

        # Getting the final message
        email = self.vectorizerMessage()
        # Predict the email
        pred = model.predict(email)

        # Check if 1 is a spam and 0 is not a spam
        if pred == 1:
            print("The message is a spam!")
        elif pred == 0:
            print("The message not a spam!")

    def run(self):
        self.predictor()
