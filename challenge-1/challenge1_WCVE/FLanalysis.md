# Affordable Housing Crisis in the State of Florida

As part of the [DataKind](https://www.datakind.org/) challenge, I conducted a comprehensive analysis of the affordable housing crisis in the state of Florida for the year 2020. The goal of this research was to uncover insights that could contribute to addressing the pressing issues surrounding housing accessibility and affordability.

In reviewing relevant data and existing research, I encountered several studies that align with the issue, including a study led by the University of Arizona. This study confirms that Black, Hispanic, and low-income populations are disproportionately located in areas at high risk of flooding compared to their white and Asian counterparts. The research, which analyzed over 50,000 property sales in South Florida, explores how ethnicity and income influence homebuyers' decisions regarding high-risk flood zones (Mittan, 2020; Backenssen & Ma, 2020). While DataKind's analysis uses U.S. Census data to explore similar demographic trends, this research underscores the complex intersection of housing affordability and environmental risk.

Motivated by these findings, I sought to explore the data further, creating specific subsets to identify trends within different populations and uncover how these trends intersect with the housing crisis. To facilitate a comprehensive examination of this complex issue, I organized the data into five distinct datasets. Each dataset focuses on specific features and inquiries related to housing accessibility, affordability, and environmental risks. The fifth dataset integrates all the individual datasets, allowing for a broader perspective that combines the insights from each, and providing a more holistic view of the housing crisis. 

![Data Organization chart]( https://github.com/wvelebanks/datakit-housing-fall-2024/blob/2f111923ede05ee716084b79e1354a4db312d500/challenge-1/challenge1_WCVE/data_organization.png "Data Organization Chart")

By examining these factors individually, we can gain a clearer understanding of the specific demographics facing significant barriers to housing. This analysis helps identify at-risk populations and highlights areas where increased state investment may be needed to improve housing stability. Additionally, it provides insight into how certain conditions may make housing unaffordable in areas that are already considered high-risk (Backenssen & Ma, 2020). Ultimately, this approach aims to deliver actionable insights that can inform policy decisions and contribute to a more equitable housing landscape in Florida.

Finally, by analyzing the combined data, we can develop a more comprehensive understanding of the barriers to housing that affect residents across different demographics. This holistic analysis uncovers key trends that illustrate how factors such as income levels, environmental risks, and housing affordability intersect to create systemic challenges in accessing stable housing.
It also highlights how environmental risks, such as flooding, and financial constraints are not isolated to specific groups, but instead affect a broader segment of the population—particularly in regions where flood-prone areas overlap with economically disadvantaged neighborhoods.

### Population Demographics:
Let’s first examine the demographic composition of Florida as of 2020 and how it has evolved over the past few years. Florida's diversity has grown significantly in recent years. In 2020, the state's population was composed of 36.8% Caucasian/White, 28.3% African American/Black, 5.2% Asian, 1.8% Native American/Indigenous, and 2.0% Pacific Islander/Hawaiian. Additionally, a combined 26% of the population identified with multiple races or other groups, including Hispanics and Middle Eastern/North African individuals.

![population chart](https://github.com/wvelebanks/datakit-housing-fall-2024/blob/b214398adadba8726c093460379338bb0ccb5bed/challenge-1/challenge1_WCVE/popgraph.png))

Though USA Facts (2024) states that the non-Hispanic White population increased to 52.3% in 2022, compared to 2020, the Hispanic/Latino population experienced the largest growth, rising by 4.5 percentage points to 27.1%. The stacked bar chart illustrates the population distribution by sex (male/female) across all age groups in each county throughout the state of Florida (Census Reporter, n.d.).

![population by gender chartt](https://github.com/wvelebanks/datakit-housing-fall-2024/blob/c46806cebe28eefa1586a266064fc27bbb91f976/challenge-1/challenge1_WCVE/popdist.png)

### Housing Situation:
Florida has become one of the most expensive places to live, with rising housing costs affecting working families, people of color, older adults, and those with disabilities. The state’s appeal has drawn many high-income professionals from places like New York, which has made the housing shortage worse. Between 2020 and 2022, rent prices went up by over 30%, and many low-income Floridians now spend more than 30% of their income on housing, leaving them with less money for other important needs like food or medicine (Florida’s Affordable Housing Crisis, n.d.).

The Florida Policy Institute (FPI), with help from the Charles & Margery Barancik Foundation, is working to solve this problem by focusing on affordable housing policies in Southwest Florida. They want to create solutions that reduce inequality and meet the need for affordable homes. After Hurricane Ian, addressing housing costs is even more urgent for the health and well-being of Florida’s residents (Florida’s Affordable Housing Crisis, n.d.).

In Florida, the homeownership rate is around 64-65%, slightly below the national average. Homeownership is more common in suburban and rural areas, while urban areas tend to have higher percentages of renters due to rising housing costs. As housing prices increase, more residents are opting to rent, especially in larger cities. Many renters are spending a significant portion of their income on housing, driving up the demand for more affordable options. The following graph illustrates the distribution of homeownership versus renting in key counties.

![rent - owner chartt](https://github.com/wvelebanks/datakit-housing-fall-2024/blob/f8ba5123923f7c429deed85217e0d684cac057e1/challenge-1/challenge1_WCVE/rent_owner.png)

The next graph illustrates the distribution of homeowners by race, highlighting the major groups: White/Caucasian, African American/Black, and a combined category of biracial and other racial groups.

![rent - owner by race chartt](https://github.com/wvelebanks/datakit-housing-fall-2024/blob/1811202e27c5c5d1d6241f5ea84a51a071f5f397/challenge-1/challenge1_WCVE/rntownerbyrace.png)

### Financial Situation (Banking):
Mortgage payments in Florida are among the highest in the nation relative to income, with the state's Purchase Applications Payment Index (PAPI) score of 228 in April indicating that homeownership is expensive for residents. This is due to rising home prices and high mortgage rates, which have been above 7%. The median mortgage payment in April was about $2,600, a 7% increase from the previous year. Florida's home prices also increased, with the median price for single-family homes at $415,000. These factors are making it difficult for first-time buyers, and experts stress the need for lower mortgage rates and more housing inventory to improve affordability (Mohammed, 2024).

Florida's commercial real estate market is facing challenges, including rising vacancy rates, more loan delinquencies, and tighter lending rules. Vacancy rates are up in office, industrial, and multifamily sectors, especially due to remote work. Loan delinquencies are increasing as higher interest rates make refinancing harder. Banks are tightening lending standards, and demand for new loans is weakening (Florida Commercial Real Estate Loans: Tightened Lending and Increased Delinquencies, 2024).

The graph below shows a comparison between the number of mortgage applications submitted and the number of denials across 27 counties in Florida. This highlights the constraints faced by potential homebuyers, such as stricter lending standards, high debt-to-income ratios, and other factors that contribute to mortgage denials. By examining these numbers, we can better understand the challenges residents in different counties face when trying to secure a mortgage.

![motgages  chartt](https://github.com/wvelebanks/datakit-housing-fall-2024/blob/8ccb666bc1721cf7cc8f4cc997cd013735fe33b7/challenge-1/challenge1_WCVE/mortgagebycounty.png)

The next graph further explores this by showing which counties are most likely to request a mortgage and how feasible it is for applicants in each county to get approved. This provides insight into the likelihood of obtaining a mortgage based on local economic conditions, housing demand, and other factors that vary from one county to another. It highlights the disparities in mortgage accessibility, showing which areas may face more difficulties or have higher approval rates for loan applications.

![mortgages 2 chartt](https://github.com/wvelebanks/datakit-housing-fall-2024/blob/8ccb666bc1721cf7cc8f4cc997cd013735fe33b7/challenge-1/challenge1_WCVE/mortgagebycounty2.png)

### Environmental Situation:

Newborn (2017) found that environmental concerns varied across Florida, with South Floridians focused on sea level rise, northern Florida worried about land loss from development, and Tampa Bay concerned about invasive species. Many residents also expressed frustration with lawmakers for not funding land preservation. Florida faces major environmental challenges, including pollution from plastics, phosphate mining, pesticides, and excess fertilizers, which cause algae blooms. Aging infrastructure leads to sewage spills, while hazardous industrial waste and mercury from power plants threaten human and wildlife health (Zero, 2023). Solutions require stronger laws and reduced pollution at its source.

The graph below highlights the most prevalent pollutants reported across 27 counties in Florida, supporting the concerns previously mentioned. Key pollutants include wastewater, which can contaminate local water sources and harm aquatic ecosystems. Air toxics, such as those linked to industrial and traffic emissions, pose significant health risks, with some even being carcinogenic. Proximity to traffic is another major issue, contributing not only to noise pollution but also to increased exposure to harmful vehicle emissions. Lead paint remains a concern, particularly in buildings and houses constructed before the 1960s, as it can lead to serious health problems, especially in children. Additionally, the graph shows the percentage of areas with high diesel pollution, which is a significant contributor to air quality issues and respiratory problems in urban and industrial regions. These data points underline the urgency of addressing these pollutants to improve public health and environmental quality in Florida.

![polutants by county chartt](https://github.com/wvelebanks/datakit-housing-fall-2024/blob/8ccb666bc1721cf7cc8f4cc997cd013735fe33b7/challenge-1/challenge1_WCVE/pollutionbycounty.png)

The counties with the highest pollution levels (numbers 20-27) are often rural or have larger minority populations. These areas, typically lower income, face higher exposure to pollutants like wastewater, air toxics, and diesel emissions due to limited resources and infrastructure. This disproportionate environmental burden highlights the need for targeted policies to protect these vulnerable communities.

![individual pollutants chartt](https://github.com/wvelebanks/datakit-housing-fall-2024/blob/8ccb666bc1721cf7cc8f4cc997cd013735fe33b7/challenge-1/challenge1_WCVE/individualpollutantsbycounty.png)

Despite the environmental challenges Florida faces, including pollution and the loss of natural lands, there is a growing awareness and call for action. Communities across the state, from South Florida to the Tampa Bay area, are advocating stronger environmental protections and sustainable practices. However, these environmental issues are closely intertwined with housing problems, economic inequality, and financial challenges. Many areas, especially rural and minority communities, are grappling with older housing stock that poses health risks, and the economic pressures of development often overshadow environmental concerns. Yet, as more Floridians recognize the value of preserving natural resources and addressing housing and economic disparities, there is hope for a more equitable future. By pushing for comprehensive policies that tackle both environmental and economic challenges, Florida can move toward a sustainable future where both people and the planet can thrive.

### Bibliography

* Mittan, K. (2020, October 5). Black and Hispanic People More Likely to Live in High-Risk Flood Zones, Study Finds | University of Arizona News. Home | University of Arizona News; Arizona State University Communications. https://news.arizona.edu/news/black-and-hispanic-people-more-likely-live-high-risk-flood-zones-study-finds

* Backenssen, L., & Ma, L. (2020, August 25). Sorting over flood risk and implications for policy reform - ScienceDirect. ScienceDirect.Com | Science, Health and Medical Journals, Full Text Articles and Books.; Elsevier: Journal of Environmental Economics and Management. https://www.sciencedirect.com/science/article/abs/pii/S0095069620300851

* USAFacts. (2024, November 25). Florida  population by year, county, race, & more. USAFacts. https://usafacts.org/data/topics/people-society/population-and-demographics/our-changing-population/state/florida/

* Census Reporter. (n.d.). Census profile: Florida. https://censusreporter.org/profiles/04000US12-florida/

* Florida’s affordable housing crisis. (n.d.). https://www.floridapolicy.org/posts/floridas-affordable-housing-crisis
Mohammed, O. (2024, May 30). Florida mortgages are more expensive than most. Newsweek. https://www.newsweek.com/florida-mortgages-are-more-expensive-most-1906305#:~:text=Mortgage%20payments%20in%20Florida%20are%20some%20of,facing%20less%20affordable%20prospects%20in%20acquiring%20property

* Florida Commercial Real Estate Loans: Tightened lending and increased delinquencies. (2024, November 15). JD Supra. https://www.jdsupra.com/legalnews/florida-commercial-real-estate-loans-5192636/#:~:text=The%20commercial%20real%20estate%20(CRE)%20market%20in,difficult%20environment%20for%20both%20borrowers%20and%20lenders

* Newborn, S. (2017, October 23). Environment one of Floridians’ top 5 concerns. WUSF. https://www.wusf.org/environment/2017-10-23/environment-one-of-floridians-top-5-concerns 

* Zero, F. F. (2023, June 25). Florida’s top 10 toxic pollution problems. The Advocates Voice. https://www.advocatesvoice.com/2020/04/floridas-top-10-toxic-pollution-problems.html



