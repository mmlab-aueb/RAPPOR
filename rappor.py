import secrets

class Rappor:

    def __init__(self, rappor_f = 0.5):
        self.rappor_f = rappor_f
        self.rGenerator = secrets.SystemRandom()
    
    def permanent_randomized_response(self,number_of_choices, correct_choice):
        '''
        It executes the basic one-time RAPPOR
        '''
        responses = [0] * number_of_choices  
        for x in range(number_of_choices):
            r = self.rGenerator.random()
            if (r < 0.5 * self.rappor_f):
                responses[x] = 1 # anwer randomly one
            elif (r < self.rappor_f):
                responses[x] = 0 # answer randomly zelo
            else :               # asnwer honestly
                if x == correct_choice:
                    responses[x] = 1
                else:
                    responses[x] = 0

        return responses

    def estimate_responses(self, noisy_responses, total_responders):
        '''
        It calculates the propability of each choice
        based on the noisy repsonses
        '''
        estimations = [0] * len(noisy_responses)
        for x in range(len(noisy_responses)):
            #propability = max(0, 2*(noisy_responses[x]/total_responders - 0.25))
            propability = max(0, (noisy_responses[x]/total_responders - self.rappor_f*0.5)/(1-self.rappor_f))
            estimations[x] = propability
        return estimations

    