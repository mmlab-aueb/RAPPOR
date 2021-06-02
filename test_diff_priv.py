from random import normalvariate, randrange
from rappor import Rappor
from attacker import Attacker
import secrets


'''
Configuration Parameters
'''
num_providers = 1000     # Number of data providers
num_choices = 20         # Number of choices included in the question
use_normal_dist = False  # If True normal distribution is used, otherwise uniform

# Parameters that control the normal distribution
normal_mean = 9        # The mean value
nomal_dev = 1          # The deviation 

def test_rappor():
    rGenerator = secrets.SystemRandom()
    rappor = Rappor()
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

    estimated_responses = rappor.estimate_responses(noisy_responses,num_providers)
    print("Percentages of responses")
    print("Real\t Estimated")
    for y in range(num_choices):
        real_responses_per      = (real_responses[y]/num_providers)*100
        estimated_responses_per = estimated_responses[y]*100
        print ("%.2f \t %.2f" % (real_responses_per, estimated_responses_per))
 
    print("Averages:")
    real_responses_sum  = 0
    noisy_responses_sum = 0
    noisy_num_providers = 0
    noisy_responses_new = [0] * num_choices
    for y in range(num_choices):
        noisy_num_providers += estimated_responses[y]*num_providers

    for y in range(num_choices):
        real_responses_sum  += real_responses[y]* y
        noisy_responses_sum += (estimated_responses[y]*num_providers)* y
        
    
    print ("All \t %.6f \t %.6f" % (real_responses_sum/num_providers, noisy_responses_sum/noisy_num_providers))
    # Adding a new provider
    # We will perform num_choices experiements
    # The selected choice of the new provider increases with each new experiment
    num_providers_new       = num_providers +1
    real_responses_sum_new  = 0
    noisy_responses_sum_new = 0
    noisy_num_providers_new = 0
    noisy_responses_new     = [0] * num_choices
    for real_choice in range(num_choices): 
        real_responses_sum_new  = real_responses_sum  + real_choice
        noisy_num_providers_new = 0
        noisy_responses_sum_new = 0
        # Create a new noisy response
        response = rappor.permanent_randomized_response(num_choices, real_choice)
        # Add the new response to the existing ones
        for x in range(num_choices):
            noisy_responses_new[x] = noisy_responses[x]+response[x]
        # Make a new estumation of the noisy responses
        estimated_responses_new = rappor.estimate_responses(noisy_responses_new, num_providers_new)
        # Calculate the new number of noisy responders
        for x in range(num_choices):
            noisy_num_providers_new += estimated_responses_new[x]*num_providers_new        
            noisy_responses_sum_new += (estimated_responses_new[x]* num_providers_new)*x 
        print ("All+%d \t %.6f \t %.6f" % (real_choice, real_responses_sum_new/num_providers_new, noisy_responses_sum_new/noisy_num_providers_new))

if __name__ == '__main__':
    #for x in range(20):
    test_rappor()