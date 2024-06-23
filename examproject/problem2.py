import numpy as np 
import matplotlib.pyplot as plt

####Question 1

# Function to calculate the expected utility
def calculate_utility(par):
    # Generate epsilon for all career tracks
    epsilon = np.random.normal(0, par.sigma, (par.K, par.J))
    
    # Initialize array to store expected utilities
    expected_utilities = np.zeros(par.J)
    realised_utilities = np.zeros(par.J)
    
    # Iterate over each career track
    for j in range(par.J):
        v_j = par.v[j]  # Value associated with career track j
        
        # Calculate expected utility using simulation
        expected_utility = v_j + np.mean(epsilon[:, j])
        expected_utilities[j] = expected_utility
        
        # Calculate average realised utility
        realised_utility = np.mean(v_j + epsilon[:, j])
        realised_utilities[j] = realised_utility

    return expected_utilities, realised_utilities


####Question 2

# Function to simulate the scenario and calculate required metrics
def simulate_and_visualize(par):
    np.random.seed(2021)
    
    # Initialize arrays to store results
    chosen_careers = np.zeros((par.N, par.K), dtype=int)
    prior_expectations = np.zeros((par.N, par.K))
    realized_utilities = np.zeros((par.N, par.K))
    
    for k in range(par.K):
        for i in range(par.N):
            F_i = par.F[i]
            
            # Draw noise terms for friends and self
            epsilon_friends = np.random.normal(0, par.sigma, (par.J, F_i)) 
            epsilon_self = np.random.normal(0, par.sigma, par.J)
            #print(epsilon_friends)
            
            # Calculate prior expected utility for each career
            prior_expected_utility = par.v + np.mean(epsilon_friends, axis=1) #axis=0
            #print(prior_expected_utility)   
            
            # Choose the career with the highest prior expected utility
            chosen_career = np.argmax(prior_expected_utility)
            
            # Store chosen career, prior expectation, and realized utility
            chosen_careers[i, k] = chosen_career
            prior_expectations[i, k] = prior_expected_utility[chosen_career]
            realized_utilities[i, k] = par.v[chosen_career] + epsilon_self[chosen_career]
    
    # Calculate average share of graduates choosing each career
    career_shares = np.zeros((par.N, par.J))
    for i in range(par.N):
        for j in range(par.J):
            career_shares[i, j] = np.mean(chosen_careers[i, :] == j)
    
    # Calculate average subjective expected utility and average realized utility
    avg_prior_expectations = np.mean(prior_expectations, axis=1)
    avg_realized_utilities = np.mean(realized_utilities, axis=1)
    
    # Visualize the results
    for i in range(par.N):
        plt.figure(figsize=(12, 4))
        
        # Share of graduates choosing each career
        plt.subplot(1, 3, 1)
        plt.bar(range(1, par.J + 1), career_shares[i, :])
        plt.xlabel('Career Track')
        plt.ylabel('Share of Graduates')
        plt.title(f'Graduate {i+1} - Career Choices')
        plt.xticks(range(1, par.J + 1), range(1, par.J + 1))  # Set x-tick labels to 1, 2, 3
        
        # Average subjective expected utility
        plt.subplot(1, 3, 2)
        plt.bar([i + 1], avg_prior_expectations[i])
        plt.xlabel('Graduate')
        plt.ylabel('Avg Subjective Expected Utility')
        plt.title(f'Graduate {i+1} - Avg Subjective Expected Utility')
        plt.xticks([i + 1], [i + 1])  # Set x-tick label to the graduate number
        
        # Average realized utility
        plt.subplot(1, 3, 3)
        plt.bar([i + 1], avg_realized_utilities[i])
        plt.xlabel('Graduate')
        plt.ylabel('Avg Realized Utility')
        plt.title(f'Graduate {i+1} - Avg Realized Utility')
        plt.xticks([i + 1], [i + 1])  # Set x-tick label to the graduate number
        
        plt.tight_layout()
        plt.show()

####Question3        

# Function to simulate the scenario and calculate required metrics
def simulate_and_visualize2(par):
    np.random.seed(2021)
    
    # Initialize arrays to store results
    chosen_careers = np.zeros((par.N, par.K), dtype=int)
    prior_expectations = np.zeros((par.N, par.K))
    realized_utilities = np.zeros((par.N, par.K))
    new_prior_expectations = np.zeros((par.N, par.K))
    new_realized_utilities = np.zeros((par.N, par.K))
    switched_careers = np.zeros((par.N, par.K), dtype=bool)
    
    for k in range(par.K):
        for i in range(par.N):
            F_i = par.F[i]
            
            # Draw noise terms for friends and self
            epsilon_friends = np.random.normal(0, par.sigma, (F_i, par.J))
            epsilon_self = np.random.normal(0, par.sigma, par.J)
            
            # Calculate prior expected utility for each career
            prior_expected_utility = par.v + np.mean(epsilon_friends, axis=0)
            
            # Choose the career with the highest prior expected utility
            chosen_career = np.argmax(prior_expected_utility)
            
            # Store chosen career, prior expectation, and realized utility
            chosen_careers[i, k] = chosen_career
            prior_expectations[i, k] = prior_expected_utility[chosen_career]
            realized_utilities[i, k] = par.v[chosen_career] + epsilon_self[chosen_career]
            
            # After one year, update priors considering the switching cost
            updated_prior = np.copy(prior_expected_utility)
            updated_prior[chosen_career] = realized_utilities[i, k]
            for j in range(par.J):
                if j != chosen_career:
                    updated_prior[j] -= par.c
            
            # Choose the new optimal career
            new_chosen_career = np.argmax(updated_prior)
            new_prior_expectations[i, k] = updated_prior[new_chosen_career]
            new_realized_utilities[i, k] = (
                realized_utilities[i, k] if new_chosen_career == chosen_career else par.v[new_chosen_career] + np.random.normal(0, par.sigma) - par.c
            )
            
            # Check if the career was switched
            switched_careers[i, k] = (new_chosen_career != chosen_career)
    
    # Calculate average share of graduates choosing each career
    career_shares = np.zeros((par.N, par.J))
    for i in range(par.N):
        for j in range(par.J):
            career_shares[i, j] = np.mean(chosen_careers[i, :] == j)
    
    # Calculate average subjective expected utility and average realized utility
    avg_prior_expectations = np.mean(new_prior_expectations, axis=1)
    avg_realized_utilities = np.mean(new_realized_utilities, axis=1)
    
    # Calculate the share of graduates who switched careers
    switch_shares = np.mean(switched_careers, axis=1)
    
    # Visualize the results
    for i in range(par.N):
        plt.figure(figsize=(16, 4))
        
        # Share of graduates choosing each career
        plt.subplot(1, 4, 1)
        plt.bar(range(1, par.J + 1), career_shares[i, :])
        plt.xlabel('Career Track')
        plt.ylabel('Share of Graduates')
        plt.title(f'Graduate {i+1} - Career Choices')
        plt.xticks(range(1, par.J + 1), range(1, par.J + 1))  # Set x-tick labels to 1, 2, 3
        
        # Average subjective expected utility
        plt.subplot(1, 4, 2)
        plt.bar([i + 1], avg_prior_expectations[i])
        plt.xlabel('Graduate')
        plt.ylabel('Avg Subjective Expected Utility')
        plt.title(f'Graduate {i+1} - Avg Subjective Expected Utility')
        plt.xticks([i + 1], [i + 1])  # Set x-tick label to the graduate number
        
        # Average realized utility
        plt.subplot(1, 4, 3)
        plt.bar([i + 1], avg_realized_utilities[i])
        plt.xlabel('Graduate')
        plt.ylabel('Avg Realized Utility')
        plt.title(f'Graduate {i+1} - Avg Realized Utility')
        plt.xticks([i + 1], [i + 1])  # Set x-tick label to the graduate number
        
        # Share of graduates who switched careers
        plt.subplot(1, 4, 4)
        plt.bar([i + 1], switch_shares[i])
        plt.xlabel('Graduate')
        plt.ylabel('Share Switching Careers')
        plt.title(f'Graduate {i+1} - Share Switching Careers')
        plt.xticks([i + 1], [i + 1])  # Set x-tick label to the graduate number
        
        plt.tight_layout()
        plt.show()
