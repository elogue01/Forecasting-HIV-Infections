# Forecasting-HIV-Infections

## Background
Due to the development of anti-retroviral therapies the HIV/AIDS epidemic is generally considered to be under control in the US.  However, as of 2015 there were 971,524 people living with diagnosed HIV in the US with an estimation of 37,600 new HIV diagnoses in 2014.  HIV infection rates continue to be particularly problematic in communities of color, among men who have sex with men (MSM), the transgender community, and other vulnerable populations in the US. Socioeconomic factors are a significant risk factor for HIV infection and likely contribute to HIV infection risk in these communities.  The current US opioid crisis has further complicated the efforts to combat HIV with HIV infection outbreaks now hitting regions that weren’t previously thought to be vulnerable to such outbreaks.  

A model that can accurately forecast regional HIV infection rates would be beneficial to local public health officials.  Provided with this information, these officials will be able to better marshal the resources necessary to combat HIV and prevent outbreaks from occurring.  Accurate modeling will also identify risk factors for communities with high HIV infection rates and provide clues as to how officials may better combat HIV in their respective communities.

## Project Goal
1)	To accurately forecast the HIV infection rates in US counties by building a multilevel model that utilizes HIV infection data, census data, data on the opioid crisis, and data on sexual orientation.

2)	Identify features that are the most significant drivers of HIV infection rates and learn how these drivers differ between rural, suburban and urban counties

## About the Data

### Sources
Data was obtained from four sources for this project.  
1. The largest collection of HIV and opioid data was obtained from the [opioid database](http://opioid.amfar.org/) maintained by the American Foundation for AIDS Research (amfAR).  
2. Additional HIV data was gathered from the datasets maintained by the [AIDSVu](https://aidsvu.org/resources/downloadable-maps-and-resources/).  
3. Demographic and economic data were obtained from the 5yr - American Community Survey which are available at the [US census bureau website](https://factfinder.census.gov/faces/nav/jsf/pages/searchresults.xhtml?refresh=t).
4. Estimates for the [MSM population](http://emorycamp.org/item.php?i=48) in each county were obtained from the Emory Coalition for Applied Modeling for Prevention (CAMP).

### Methods
