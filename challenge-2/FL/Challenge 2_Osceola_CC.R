#########################
## Author: Chloe Confino
## Date: 9/22/2024
## Description: Challenge #2 exploration - Osceola County
#########################

library(data.table)
library(bit64)
library(tigris)
library(dplyr)
library(ggplot2)
options(tigris_use_cache = TRUE)

setwd('C:/Users/cmars/Documents/DataKind - Affordable Housing')


##### Read in Data #####
dt <- fread('housing-data/FL/Osceola Data/data.csv')
dt_dict <- fread('housing-data/FL/Osceola Data/data_dictionary.csv')

##### Clean Data #####
#Med HH Income field. -666666666 appears to be for null fields
dt[,med_hh_inc_est:=ifelse(med_hh_inc_est==-666666666,NA,med_hh_inc_est)]
summary(dt$med_hh_inc_est) #only 1 NA, let's drop the record
dt<- dt[!is.na(med_hh_inc_est)]

#annualize rental cost
dt[,housecost_rent_est_annual:=housecost_rent_est*12]
summary(dt$housecost_rent_est_annual)

#2 records with negative rent.. drop
dt <- dt[housecost_rent_est_annual>0]

summary(dt$pop_pct_60plus_est) #looks good


##### Calculate Needed Fields #####

#Calculate % of AMI
dt[,Pct_AMI:=med_hh_inc_est/90400]

#Calculate cost burden of rent
dt[,Cost_Burden_Rent:=housecost_rent_est_annual/med_hh_inc_est]


##### Plot % of AMI and Cost Burden of Rent #####
tracts <- tracts(state = "FL", county = '097')
dt[,GEOID:=as.character(geoid)]

map_dt <- tracts %>% 
  left_join(dt[,.(GEOID,Pct_AMI,Cost_Burden_Rent,pop_pct_60plus_est)], by = c("GEOID" = "GEOID")) 


# Start PDF generation
pdf(file = "housing-data/FL/Osceola Data/Osceola County Plots.pdf", 
    width = 6,
    height = 6) 

ggplot(data = map_dt, aes(fill = Pct_AMI)) + 
  geom_sf() + 
  scale_fill_distiller(palette = "YlGnBu", 
                       direction = 1) + 
  labs(title = "Percent of AMI - Osceola County",
       fill = "% of AMI") + 
  theme_void()


ggplot(data = map_dt, aes(fill = Cost_Burden_Rent)) + 
  geom_sf() + 
  scale_fill_distiller(palette = "YlOrRd", 
                       direction = 1) + 
  labs(title = "Cost Burden of Rent - Osceola County",
       fill = "Cost Burden of Rent") + 
  theme_void()

ggplot(data = map_dt, aes(fill = pop_pct_60plus_est)) + 
  geom_sf() + 
  scale_fill_distiller(palette = "YlGnBu", 
                       direction = 1) + 
  labs(title = "% of Population 60+ - Osceola County",
       fill = "% of Population 60+") + 
  theme_void()

##Identify areas that assistance should be most targeted
##(highest cost burden, highest senior population, lowest % of AMI)

#rank tracts by each of the fields
dt[,pop_pct_60plus_est_rank:=frank(pop_pct_60plus_est)]
dt[,Cost_Burden_Rent_rank:=frank(Cost_Burden_Rent)]
dt[,Pct_AMI_rank:=frank(-Pct_AMI)]

#Calculate Combined Rank for each tract
dt[,Combined_Rank:=frank(pop_pct_60plus_est+Cost_Burden_Rent_rank+Pct_AMI_rank)]

map_dt <- tracts %>% 
  left_join(dt[,.(GEOID,Pct_AMI,Cost_Burden_Rent,pop_pct_60plus_est,Combined_Rank)], 
            by = c("GEOID" = "GEOID")) 

ggplot(data = map_dt, aes(fill = Combined_Rank)) + 
  geom_sf() + 
  scale_fill_distiller(palette = "YlOrRd", 
                       direction = 1) + 
  labs(title = "Target Areas for Assistance - Osceola County",
       fill = "Rank",
       caption = "Areas with higher rank (darker fill) would be the best areas to target assistance.") + 
  theme_void()

dev.off()


#save dataset
fwrite(dt,'housing-data/FL/Osceola Data/Osceola County Data - Calculated.csv')
