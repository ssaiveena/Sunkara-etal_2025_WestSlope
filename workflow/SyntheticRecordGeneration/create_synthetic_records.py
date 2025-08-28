import numpy as np
from random import random

def generate_synthetic_records(ensemble_type, num_syn_records):
    """
    Generates synthetic streamflows using a HMM. Records are written to separate files

    :param ensemble_type:               string, baseline or ClimateChangeEnsemble (two options, "LR" and "SR")
    :param num_syn_records:             float, the number of synthetic records to generate
    """

    # load the HMM parameters
    dry_state_means = np.loadtxt('HMM_parameters/' + ensemble_type + '/dry_state_means.txt', delimiter=' ')
    wet_state_means = np.loadtxt('HMM_parameters/' + ensemble_type + '/wet_state_means.txt', delimiter=' ')
    covariance_matrix_dry = np.loadtxt('HMM_parameters/' + ensemble_type + '/covariance_matrix_dry.txt', delimiter=' ')
    covariance_matrix_wet = np.loadtxt('HMM_parameters/' + ensemble_type + '/covariance_matrix_wet.txt', delimiter=' ')
    transition_matrix = np.loadtxt('HMM_parameters/' + ensemble_type + '/transition_matrix.txt', delimiter=' ')

    # calculate stationary distribution to determine unconditional probabilities
    eigenvals, eigenvecs = np.linalg.eig(np.transpose(transition_matrix))
    one_eigval = np.argmin(np.abs(eigenvals-1))
    pi = eigenvecs[:,one_eigval] / np.sum(eigenvecs[:,one_eigval])
    unconditional_dry=pi[0]
    unconditional_wet=pi[1]

    #create records
    for i in range(0, num_syn_records):
        logAnnualQ_s=np.zeros([105, 5])

        states = np.empty([105])

        if random() <= unconditional_dry:
            states[0] = 0
            logAnnualQ_s[0,:]=np.random.multivariate_normal(np.reshape(dry_state_means,-1),covariance_matrix_dry)
        else:
            states[0] = 1
            logAnnualQ_s[0,:] =np.random.multivariate_normal(np.reshape(wet_state_means,-1),covariance_matrix_wet)

        # generate remaining state trajectory and log space flows
        for j in range(1,105):
            if random() <= transition_matrix[int(states[j-1]),int(states[j-1])]:
                states[j] = states[j-1]
            else:
                states[j] = 1 - states[j-1]

            if states[j] == 0:
                logAnnualQ_s[j,:] = np.random.multivariate_normal(np.reshape(dry_state_means,-1),covariance_matrix_dry)
            else:
                logAnnualQ_s[j,:] = np.random.multivariate_normal(np.reshape(wet_state_means,-1),covariance_matrix_wet)


        AnnualQ_s = np.exp(logAnnualQ_s)

        np.savetxt('Synthetic_records/' + ensemble_type + '/AnnualQ_s' + str(i) + '.txt', AnnualQ_s)

# Generate synthetic traces based off the 75 year record
generate_synthetic_records("baseline", 1000)
