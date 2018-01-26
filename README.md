# Forecasting-HIV-Infections

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
##### Figure 1: Removal of the Scott County, IN outlier data

5. The total number of MSM-12months and MSM-5years in counties were transformed into percentages of the adult male population for each county.
6. The percentages for the 20-24 population, the 25-34 population, and the 35-44 population were combined into a percentage for the 20-44 population.
7. Household income data was log transformed.

## Exploratory Data Analysis
