# Overview

This is a DL Reproducibility Project for UIUC CS598 DL4H in Spring 2022.

## Citation to the original work

> Paper: 
Completing Missing Prevalence Rates for Multiple Chronic Diseases by Jointly Leveraging Both Intra- and Inter-Disease Population Health Data Correlations published by Yujie, et al in 2021
> 
> CPH model: https://github.com/WoodScene/Compressive-Population-Health

## Scope of reproducibility

I will evaluate whether CPH has better performance than baseline as stated, and whether using inter- and intra-disease correlation is truly reasonable.

Three claims to be addressed from the original paper:

1. The authors compared their CPH methods to 10 baseline models and achieved a higher inference accuracy. The average accuracy delta ranged from 14.8% to 9.1%. 

2. The authors made a conclusion that spatial correlation of morbidity must exist when the distance between two wards is not exceeding a certain threshold.

3. The authors presented that there is a strong correlation among these three chronic diseases (obesity, diabetes, and hypertension).

# Setup

## Requirements

Install python(3.6+), TensorFlow(2.x).

## Data download instruction 

The Chronic Diseases Prevalence Dataset is open according to [here](https://digital.nhs.uk/data-and-information/publications/statistical/quality-and-outcomes-framework-achievement-prevalence-and-exceptions-data)

## Run

All the code related to this reproducibility project is available in the CPH-Reproducibility-Project directory.

1. Verify Claim 1

    - CPH model
        - Change disease to a target disease (obesity, diabetes, and hypertension), then run ./CPH-Reproducibility-Project/main.py. 
        - Note: Default parameters (learning_rate, epoch, etc.) are optimized for obesity as target disease using grid search (search logs in ./CPH-Reproducibility-Project/result/). To reproduce two other diseases, I suggest learning_rate = 2.746196517822815e-05, epoch = 20 for hypertension and learning_rate = 2.156862745098039e-05, epoch = 20 for diabetes.
    - CPH1 model (baseline no.1)
        - Change disease to a target disease (obesity, diabetes, and hypertension) and ***hint_rate = 0***, then run ./CPH-Reproducibility-Project/main.py. 
    - GAIN model (baseline no.2)
        - Change disease to a target disease (obesity, diabetes, and hypertension), then run ./GAIN/main.py. 

2. Verify Claim 2

    - Run ./CPH-Reproducibility-Project/statistics.py. Two files will be generatged inside ./CPH-Reproducibility-Project/result/ directory.

        - correlation-distance.csv: correlation of one disease (e.g. obesity) against ward distance in km.
    
        - correlation-distance2.csv: Pearson correlation of three diseases (obesity, diabetes, and hypertension) against ward distance in km.

    - Plot correlation vs distance from .csv file.

3. Verify Claim 3

    - Fetch Prevalence_2017 data of three diseases (obesity, diabetes, and hypertension) from ./CPH-Reproducibility-Project/data/Chronic_Diseases_Prevalence_Dataset.csv.

    - Plot Pearson correlation of any two pairs of diseases.

# Reproducibility Results
 
1.  Claim 1

I reproduced comparable inference quality metrics as the original paper: RMSE for obesity, hypertension and diabetes were 0.0409, 0.0151, 0.0218 (+13.6%, -9.0%, +20.4% compared with original paper); MAE for obesity, hypertension and diabetes were 0.0329, 0.0106, 0.0161 (+17.1%, -17.8%, +28.8% compared with original paper).

![claim1](https://i.ibb.co/kH1tpDh/20220509113127.png)

Table1 has summarized the final results for three diseases using the optimized configurations. Compared with two top-performing baseline models, CPH1 (CPH model without hinting mechanism) and GAIN (GAN model using intra-disease data only), the average accuracy improvement across three diseases is 9.8% and 51.4%. The percentage improvement from CPH1 model is very close to the value in original paper (10.5%). Percentage improvement from GAIN is slightly higher than original paper (51.4% vs 31.1%), which is also acceptable because I honestly did not spend as much time tuning baseline models thus GAIN model performs slightly worse than what presented in the original paper. Regardless of the small difference, this result supports the overall reproducibility of the CPH model proposed in the original work. It also upholds the paper’s conclusion that CPH model can achieve significant improvements in recovering public health dataset with missing entries by leveraging the power of both intra- and inter-disease correlation.

2.  Claim 2

![claim2](https://i.ibb.co/t4bYf48/20220509113125.png)

The spatial correlation within a certain geographical scale can be easily seen from the Figure 2. This finding justifies the rationale of using intra-disease data from nearby wards to predict a specific location.

3.  Claim 3

![claim3](https://i.ibb.co/cvWsf6b/20220509113118.png)

The high Pearson coefficients (0.75 ~ 0.84) between any of the three disease pair do support the Claim 3. So, positive correlation exists among these three chronic diseases, and using inter-disease prevalence data is reasonable for missing data recovery.

# Demo video

https://mediaspace.illinois.edu/media/t/1_rtem1gmh