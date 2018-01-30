# Forecasting-HIV-Infections
This project was originally used as my capstone project for the data science intensive program at [Galvanize Inc.](https://www.galvanize.com/denver-platte/data-science) Prior to participating in this program I spent about a decade in the HIV research field.  My work had largely focused on the molecular host-pathogen  interactions involved in HIV infection and on the impacts HIV has on the immune system.  Although I have always been interested in the epidemiology of HIV, this had never been a focus of my research projects. I ultimately decided to use my capstone project as an opportunity try my hand at HIV epidemiology and learn something new about the HIV epidemic in the US.  Although my time in this data science program has ended, I intend to continue work on this project whenever I can find the time.  So if this is something that you find interesting, I would suggest checking this repo from time to time to see how my analysis has been extended. For those with critiques and suggestions for improving this analysis I encourage you to get in contact with me (elogue01@gmail.com).

If you are only looking for a brief summary of this project, I would suggest looking at the [poster](https://github.com/elogue01/Forecasting-HIV-Infections/blob/master/Eric_Logue_poster.pdf) that I presented at the Galvanize Data Science Capstone Showcase.  However, for those of you that you are interested in a more detailed dive into this project, then I encourage you to read on.
## Background
Due to the development of anti-retroviral therapies the HIV/AIDS epidemic is generally considered to be under control in the US.  However, as of 2015 there were 971,524 people living with diagnosed HIV in the US with an estimation of 37,600 new HIV diagnoses in 2014.  HIV infection rates continue to be particularly problematic in communities of color, among men who have sex with men (MSM), the transgender community, and other vulnerable populations in the US. Socioeconomic factors are a significant risk factor for HIV infection and likely contribute to HIV infection risk in these communities.  The current US opioid crisis has further complicated the efforts to combat HIV with HIV infection outbreaks now hitting regions that weren’t previously thought to be vulnerable to such outbreaks.  

A model that can accurately forecast regional HIV infection rates would be beneficial to local public health officials.  Provided with this information, these officials will be able to better marshal the resources necessary to combat HIV and prevent outbreaks from occurring.  Accurate modeling will also identify risk factors for communities with high HIV infection rates and provide clues as to how officials may better combat HIV in their respective communities.

## Project Goal
1)	To accurately model HIV incidences (new infections per 100,000) in US counties by building a linear regression model that utilizes HIV infection data, census data, data on the opioid crisis, and data on sexual orientation.

2)	Identify features that are the most significant drivers of HIV infection rates and learn how these drivers differ between different regions.

## About the Data

### Sources
Data were obtained from four sources for this project:  
1. The largest collection of HIV and opioid data was obtained from the [opioid database](http://opioid.amfar.org/) maintained by the American Foundation for AIDS Research (amfAR).  
2. Additional HIV data was gathered from the datasets maintained by the [AIDSVu](https://aidsvu.org/resources/downloadable-maps-and-resources/).  
3. Demographic and economic data were obtained from the 5yr - American Community Survey which are available at the [US census bureau website](https://factfinder.census.gov/faces/nav/jsf/pages/searchresults.xhtml?refresh=t).
4. Estimates for the [MSM population](http://emorycamp.org/item.php?i=48) in each county were obtained from the Emory Coalition for Applied Modeling for Prevention (CAMP).

### Methods

Data were manipulated prior to analysis in the following ways:
1. State and county codes were merged in datasets were they were separated so they could be used later to merge dataframes together.
2. To simplify the intitial analysis, data was restricted to the year 2015.
3. Counties in which HIV incidence data were suppressed (counties with 0-4 new HIV diagnoses) in 2015 were removed from the dataset.  This resulted in a dataset containing 747 counties.
4. Data from Scott County, Indiana was removed from the dataset.  This small rural county experienced an HIV outbreak in 2014-2015 due to IV drug use.  This county was an obvious outlier in the data and made it difficult to image all data in a plot.
![alt text](https://github.com/elogue01/Forecasting-HIV-Infections/blob/master/images/outlier_removal_plot.png)
#### Figure 1: HIV incidence vs HIV prevalence data with and without the removal of suppressed counties and the Scott County, IN outlier data

5. The total number of MSM-12months and MSM-5years in counties were transformed into percentages of the adult male population for each county.
6. The percentages for the 20-24 population, the 25-34 population, and the 35-44 population were combined into a percentage for the 20-44 population.
7. Household income data was log transformed.

## Exploratory Data Analysis
Exploratory data analysis was performed on the dataset to identify the features were most promising for use in a multiple linear regression model. This analysis also identified features that would benefit from a transformation of their data.  The following text summarizes the data analysis that was perform. The reader can find a fuller picture of the exploratory data analysis in the [EDA-presentation.ipynb](https://github.com/elogue01/Forecasting-HIV-Infections/blob/master/EDA-presentation.ipynb) jupyter notebook.

### Identifying features with linear relationship to HIV incidence.
After cleaning and merging our different data sources there were 42 features to be explored in our dataframe.  Initial analysis focused on finding features that appeared to have a linear relationship with HIV incidence.  Pair plots and joint plots were used to identified five features (HIV prevalence, % African American, % White, % of Population Uninsured, and Poverty Rate) where a linear relationship to HIV incidence looked likely. Furthermore, spearman correlations for each of these features indicated moderate positive or negative correlation with HIV incidence.  It is not surprising that  HIV prevalence, which measures the number of HIV+ individuals per 100,000 in the population, shows the highest correlation with HIV incidence levels.  The fact that the other features in this group relate to demographics and economics is also to be expected since there is ample evidence indicating that race and socioeconomic status impact an individuals risk for HIV infection.
![alt text](https://github.com/elogue01/Forecasting-HIV-Infections/blob/master/images/high_corr_features)
#### Figure 2: Five features associated with HIV demographicsshowed moderate correlation with HIV incidence.

In addition to these features with a stronger correlation to HIV incidence, we also identified four features (Household Income (log transformed), % Unmet Drug Treatment Need, % Drug Dependent, % of Nonmedical Pain Reliever Use) that show significant though low level correlation with HIV incidence. It was somewhat surprising that the household income levels were not more highly correlated with HIV incidence like some of our other socioeconomic indicators.  It is clear that even with a log transformation, this feature may not have a straight forward linear relationship to HIV incidence. In addition, this group of features also include three features associated with opioid use. A closer look at this figure indicates that while these features may not be linearly related to HIV incidence for all US counties, it is possible that there will be a linear relationship in a subset of counties.  The opioid epidemic has had a particularly strong impact in white rural communities and the impact of the opioid crisis on HIV incidence may only be apparent in state with a number of such counties.  

![alt text](https://github.com/elogue01/Forecasting-HIV-Infections/blob/master/images/lower_corr_features)
#### Figure 3: Features associated with opioid use and household income showed significant though low level correlation with HIV incidence.

One major assumption when building a linear model is that the features used in that model are not correlated with one another.  After having identified several features with low to moderate correlation with HIV incidence levels, I wanted to check if these different features correlation with one another.  A high degree of correlation between features would suggest that the one feature should be excluded from the model.  Looking at the nine features identified above we only see the % African American and % White features have a correlation coefficient with an absolute value greater than 0.8.  We see a lower level of correlation between the two features dealing with race and HIV prevalence.  This is to be expected since HIV has had an outsized impact on the African American community in the US.  Having correlation coefficients with an absolute value just above 0.7, a feature dealing with race may still be useful in a model with HIV prevalence.  Ultimately we will see how these features play with each other once we begin the feature selection process.
![alt text](https://github.com/elogue01/Forecasting-HIV-Infections/blob/master/images/feature_corr_heatmap.png)
#### Figure 3: A heatmap displays the correlation matrix for nine features with low to moderate correlation to HIV incidence.
