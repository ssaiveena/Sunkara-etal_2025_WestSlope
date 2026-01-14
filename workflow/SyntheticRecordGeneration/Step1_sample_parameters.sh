#this code generates parameter samples using Latin Hypercube Sampling (LHS) method combinations of HMM parameters and demand 
NSAMPLES=1000
METHOD=Latin
JAVA_ARGS="-cp MOEAFramework-3.11-Demo.jar"

# Generate the parameter samples
echo -n "Generating parameter samples..."
java ${JAVA_ARGS} \
    org.moeaframework.analysis.sensitivity.SampleGenerator \
    --method ${METHOD} --n ${NSAMPLES} --p uncertain_param_demand.txt \
    --o LHsamples_1000.txt
#download MOEA framework from https://moeaframework.org/

