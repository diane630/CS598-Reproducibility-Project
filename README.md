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


# Demo video

https://mediaspace.illinois.edu/media/t/1_rtem1gmh