from random import normalvariate, randrange
from rappor import Rappor
from attacker import Attacker
import secrets


'''
Configuration Parameters
'''
num_providers = 10000 # Number of data providers
num_choices = 20        # Number of choices included in the question
use_normal_dist = True  # If True normal distribution is used, otherwise uniform

# Parameters that control the normal distribution
normal_mean = 9        # The mean value
nomal_dev = 1          # The deviation 

def test_rappor():
    rGenerator = secrets.SystemRandom()
    rappor = Rappor()
    attacker = Attacker()
    real_responses          = [0] * num_choices
    noisy_responses         = [0] * num_choices
    real_responses_per      = [0] * num_choices
    estimated_responses_per = [0] * num_choices
    total_random = 0
    random_guesses = 0
    guesses_from_ones = 0

    for x in range(num_providers):
        '''
        Calculate the real response
        '''
        if use_normal_dist:
            real_choice = int(round(normalvariate(normal_mean,nomal_dev),0))
            # some times ths gives values out of the range so fix that
            real_choice = min(num_choices-1, real_choice)
            real_choice = max(0, real_choice)
        else:
            # real_choice = rGenerator.randrange(num_choices)
            real_choice = randrange(num_choices)     
        real_responses[real_choice]+=1
        '''
        Calculate a response use RAPPOR
        '''
        response = rappor.permanent_randomized_response(num_choices, real_choice)
        for y in range(num_choices):
            noisy_responses[y]+= response[y]
        '''
        Attack!
        '''
        guessed = attacker.select_random(response)
        if (guessed == real_choice):
            random_guesses +=1
        guessed = attacker.select_from_ones(response)
        if (guessed == real_choice):
            guesses_from_ones +=1



    estimated_responses = rappor.estimate_responses(noisy_responses,num_providers)
    print("Percentages of responses")
    print("Real\t Estimated")
    for y in range(num_choices):
        real_responses_per      = (real_responses[y]/num_providers)*100
        estimated_responses_per = estimated_responses[y]*100
        print ("%.2f \t %.2f" % (real_responses_per, estimated_responses_per))
 
    print("Guesses")
    print("Random \t From ones \t From weighted")
    print("%d \t %d \t %d" %(random_guesses, guesses_from_ones, guesses_from_weighted))
if __name__ == '__main__':
    #for x in range(20):
    test_rappor()