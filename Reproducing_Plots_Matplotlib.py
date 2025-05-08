import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import streamlit as st

# input datasets
gdp_data = pd.read_csv("gdp_clean.csv")
life_exp_data = pd.read_csv("life_exp_clean.csv")
pop_data = pd.read_csv("pop_clean.csv")
countrycodes_data = pd.read_csv("countrycodes.csv")

# choose years
years = [1850, 1900, 1950, 2000]   
 
# preprocess the data to merge different data sets correctly
## reshape each dataset from wide to long format
gdp_long = gdp_data.melt(id_vars=['Country'], var_name='Year', value_name='GDP_per_capita')
life_exp_long = life_exp_data.melt(id_vars=['Country'], var_name='Year', value_name='Life_Expectancy')
pop_long = pop_data.melt(id_vars=['Country'], var_name='Year', value_name='Population')

## merge the datasets on 'Country' and 'Year'
merged_data = pd.merge(gdp_long, life_exp_long, on=['Country', 'Year']) 
merged_data = pd.merge(merged_data, pop_long, on=['Country', 'Year'])

## add continent information by merging with country_codes
merged_data = pd.merge(merged_data,
                       countrycodes_data[['country', 'continent']],
                       left_on='Country', right_on='country',
                       how='left')

## drop the redundant 'country' column
merged_data.drop(columns=['country'], inplace=True)   

#check all data types if I need to convert some data
print(merged_data.dtypes)

# convert object to int
merged_data['Year'] = merged_data['Year'].astype(int)
# use years to plot
filter_data = merged_data[merged_data['Year'].isin(years)]

# Define a color scheme for continents      
continent_color_map = {
    "Asia": "red",          
    "Europe": "green",    
    "Africa": "blue",     
    "Oceania": "yellow",    
    "Americas": "orange"     
}

# create plots
st.title("My Chart")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Life Expectancy vs Income: 1850-2000", fontsize=16)

# iterate through each year and its corresponding subplot
for i, (ax, year) in enumerate(zip(axes.flatten(), years)):
    subset = filter_data[filter_data["Year"] == year].dropna()

    
    for continent in continent_color_map:
        cont_data = subset[subset["continent"] == continent]

        ax.scatter(
            cont_data["GDP_per_capita"],
            cont_data["Life_Expectancy"],
            s=cont_data["Population"] / 1e5,  
            color=continent_color_map[continent],
            alpha=0.6,
            edgecolors="black",
            linewidth=0.5
        )

    
    ax.set_xscale("log")
    ax.set_xlim(100, 100000)
    ax.set_ylim(0, 100)

    
    ax.text(0.5, 0.9, str(year), transform=ax.transAxes, fontsize=16)

    
    if i % 2 == 0:
        ax.set_ylabel("Life Expectancy in years")
    if i >= 2:
        ax.set_xlabel("GDP/Capita $")

    
    ax.set_xticks([100, 1000, 10000, 100000])
    ax.set_xticklabels([r"$10^2$", r"$10^3$", r"$10^4$", r"$10^5$"])


legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w',
               markerfacecolor=continent_color_map[continent],
               markeredgecolor='black', markersize=10,
               label=continent)
    for continent in continent_color_map
]
axes[1, 1].legend(handles=legend_elements, title="Continent", loc="lower right")


plt.tight_layout(rect=[0, 0, 1, 0.96])
st.pyplot(fig)




 