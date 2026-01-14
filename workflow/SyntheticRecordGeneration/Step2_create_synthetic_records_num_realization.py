import numpy as np
from random import random
import os

def generate_synthetic_records(ensemble_type, num_syn_records, LHsamples, num_realizations):
    """
    Generates synthetic streamflows using a HMM. Records are written to separate files

    :param ensemble_type:               string, baseline or ClimateChangeEnsemble (two options, "LR" and "SR")
    :param num_syn_records:             float, the number of synthetic records to generate
    """

    # load the HMM parameters
    dry_state_means = np.loadtxt('HMM_parameters/' + 'baseline' + '/dry_state_means.txt', delimiter=' ')
    wet_state_means = np.loadtxt('HMM_parameters/' + 'baseline'  + '/wet_state_means.txt', delimiter=' ')
    covariance_matrix_dry = np.loadtxt('HMM_parameters/' + 'baseline'  + '/covariance_matrix_dry.txt', delimiter=' ')
    covariance_matrix_wet = np.loadtxt('HMM_parameters/' + 'baseline'  + '/covariance_matrix_wet.txt', delimiter=' ')
    transition_matrix = np.loadtxt('HMM_parameters/' + 'baseline'  + '/transition_matrix.txt', delimiter=' ')

    # calculate stationary distribution to determine unconditional probabilities
    eigenvals, eigenvecs = np.linalg.eig(np.transpose(transition_matrix))
    one_eigval = np.argmin(np.abs(eigenvals-1))
    pi = eigenvecs[:,one_eigval] / np.sum(eigenvecs[:,one_eigval])
    unconditional_dry=pi[0]
    unconditional_wet=pi[1]

    # create empty arrays to store the new Gaussian HMM parameters for each SOW #added by Veena
    Pnew = np.empty([2,2])
    piNew = np.empty([2])
    dry_state_means_New = np.empty([5])
    wet_state_means_New = np.empty([5])
    covariance_matrix_dry_New = np.empty([5, 5])
    covariance_matrix_wet_New = np.empty([5, 5])

    #create records
    for i in range(0, num_syn_records):
        # os.mkdir('../../Synthetic_records/' + ensemble_type + '/S_' + str(i)) #change this for full run
        logAnnualQ_s=np.zeros([105, 5])

       # calculate new transition matrix and stationary distribution of SOW at last node#added by Veena until next block
        # as well as new means and standard deviations
        Pnew[0,0] = max(0.0,min(1.0,transition_matrix[0,0]+LHsamples[i,4]))
        Pnew[1,1] = max(0.0,min(1.0,transition_matrix[1,1]+LHsamples[i,5]))
        Pnew[0,1] = 1 - Pnew[0,0]
        Pnew[1,0] = 1 - Pnew[1,1]
        eigenvals, eigenvecs = np.linalg.eig(np.transpose(Pnew))
        one_eigval = np.argmin(np.abs(eigenvals-1))
        piNew = eigenvecs[:,one_eigval] / np.sum(eigenvecs[:,one_eigval])
        # piNew = np.dot(np.transpose(Pnew),eigenvecs[:,one_eigval]) / \ #ask Dave if these are same
        #     np.sum(np.dot(np.transpose(Pnew),eigenvecs[:,one_eigval]))
                
        dry_state_means_New = dry_state_means * LHsamples[i,0]
        wet_state_means_New = wet_state_means * LHsamples[i,2]
        covariance_matrix_dry_New = covariance_matrix_dry * LHsamples[i,1]
        covariance_matrix_wet_New = covariance_matrix_wet * LHsamples[i,3]
        #########################################################################
        ##############################################################
        
        for real in range(0,num_realizations):
            states = np.empty([105])
            if random() <= piNew[0]:#updated uncinditional dry
                states[0] = 0
                logAnnualQ_s[0,:]=np.random.multivariate_normal(np.reshape(dry_state_means_New,-1),covariance_matrix_dry_New)
            else:
                states[0] = 1
                logAnnualQ_s[0,:] =np.random.multivariate_normal(np.reshape(wet_state_means_New,-1),covariance_matrix_wet_New)

            # generate remaining state trajectory and log space flows
            for j in range(1,105):
                if random() <= Pnew[int(states[j-1]),int(states[j-1])]: #transition matrix is Pnew
                    states[j] = states[j-1]
                else:
                    states[j] = 1 - states[j-1]

                if states[j] == 0:
                    logAnnualQ_s[j,:] = np.random.multivariate_normal(np.reshape(dry_state_means_New,-1),covariance_matrix_dry_New)
                else:
                    logAnnualQ_s[j,:] = np.random.multivariate_normal(np.reshape(wet_state_means_New,-1),covariance_matrix_wet_New)


            AnnualQ_s = np.exp(logAnnualQ_s)

            np.savetxt('Synthetic_records/' + ensemble_type + '/S_' + str(i) + '/AnnualQ_s' + str(real) + '.txt', AnnualQ_s)

# Generate synthetic traces based off the 75 year record
LHsamples = np.loadtxt('LHsamples_1000.txt')
generate_synthetic_records("HMM_1000_r_1000", 1000, LHsamples, 1000)
#ensemble_type, num_syn_records, LHsamples, num_realizations