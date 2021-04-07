import secrets

class Attacker:

    def __init__(self):
        self.rGenerator = secrets.SystemRandom()

    
    def select_random(self, noisy_responses):
        num_choices = len (noisy_responses)
        guess = self.rGenerator.randrange(num_choices) 
        return guess

    def select_from_ones(self, noisy_responses):
        choices = []
        index = 0
        for response in noisy_responses:
            if response == 1:
                choices.append(index)
            index+=1
        if len(choices) == 0:
            return self.select_random(noisy_responses)
        else:
            return self.rGenerator.choice(choices) 
   


    