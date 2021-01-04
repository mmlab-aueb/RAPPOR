from random import normalvariate, randint
from rappor import Rappor


'''
Configuration Parameters
'''
num_providers = 10000    # Number of data providers
num_choices = 20        # Number of choices included in the question
use_normal_dist = True  # If True normal distribution is used, otherwise uniform

# Parameters that control the normal distribution
normal_mean = 9        # The mean value
nomal_dev = 1           # The deviation 

def test_rappor():
    rappor = Rappor()
    real_responses = [0] * num_choices
    noisy_responses = [0] * num_choices
    real_responses_per = [0] * num_choices
    estimated_responses_per = [0] * num_choices
    total_random = 0
    print("")
    for x in range(num_providers):
        if use_normal_dist:
            real_choice = int(round(normalvariate(normal_mean,nomal_dev),0))
            # some times ths gives values out of the range so fix that
            real_choice = min(num_choices-1, real_choice)
            real_choice = max(0, real_choice)
        else:
            real_choice = randint(0, num_choices-1)    
        real_responses[real_choice]+=1
        response = rappor.permanent_randomized_response(num_choices, real_choice)
        for y in range(num_choices):
            noisy_responses[y]+= response[y]

    estimated_responses = rappor.estimate_responses(noisy_responses,num_providers)
    print("Percentages of responses")
    print("Real\t Estimated")
    for y in range(num_choices):
        real_responses_per= (real_responses[y]/num_providers)*100
        estimated_responses_per= estimated_responses[y]*100
        print ("%.2f \t %.2f" % (real_responses_per, estimated_responses_per))

if __name__ == '__main__':
    test_rappor()