import pandas as pd
import numpy as np
import plotly
import geopandas as gpd
import plotly.express as px
from shapely.geometry import shape

def create_county_barchart(df, county, variable_col):
    df = df[df["county_name"]==county]
    
    fig = px.bar(
    df,
    x="census_tract",
    y=variable_col,
    title=f"Population by {county} for {variable_col}",
    labels={county: county.replace('_', ' ').title(), variable_col: variable_col.replace('_', ' ').title()},
    height=500,
    width=800
    )
    fig.update_layout(
        xaxis_title=county.replace('_', ' ').title(),
        yaxis_title=variable_col.replace('_', ' ').title(),
        showlegend=False,
        bargap=0.1
        )
    fig.show()

def create_tract_barchart(df, census_tract, variable_cols):
    df = df[df["census_tract"]==census_tract]
    df_long = df.melt(id_vars=["census_tract"], value_vars=variable_cols, 
                      var_name="Variable", value_name="Value")
    fig = px.bar(
        df_long,
        x="census_tract",
        y="Value",
        color="Variable",  # Group by the 'Variable' column to create clusters
        title=f"Population in {census_tract}",
        height=500,
        width=800
    )
    fig.update_layout(
        title={
            'x': 0.5,  # Center the title
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Census Tract",
        yaxis_title="Percentage",
        showlegend=True,  # Show the legend
        bargap=0.1,
        barmode="group"
    )
    fig.show()

def calculate_geojson_center(geojson):
    geometries = [shape(feature['geometry']) for feature in geojson['features']]
    
    # Combine all geometries into a single object (MultiPolygon) and calculate the centroid
    combined_shape = geometries[0]
    for geom in geometries[1:]:
        combined_shape = combined_shape.union(geom)

    centroid = combined_shape.centroid
    return {"lat": centroid.y, "lon": centroid.x}

def create_heatmap(df_geo, geojson, variable, county_geojson):
    
    # Create the base choropleth map for census tracts using Plotly with Mapbox
    fig = px.choropleth_mapbox(
        df_geo,
        geojson=geojson,  # Use the census tract GeoJSON
        locations="geoid",  # Link to the 'geoid' column
        featureidkey="properties.geoid",  # Make sure this matches the GeoJSON field
        color=variable,
        color_continuous_scale='Viridis',
        labels={f"{variable}"},
        mapbox_style="white-bg", 
        center=calculate_geojson_center(geojson),
        zoom=6, 
        hover_data=['county_name'] #additional tooltips
    )

    # Add county boundaries as a Mapbox layer
    fig.update_layout(
        mapbox_layers=[
            {
                "source": county_geojson,  # Use the county GeoJSON
                "sourcetype": "geojson",  # Specify GeoJSON source type
                "type": "line",  # Display only the borders as lines
                "color": "black",  # Set border color
                "line": {"width": 1},  # Set line width
                "below": "traces",  # Ensure county borders are below choropleth
            }
        ]
    )

    # Show the figure
    fig.show()

def create_county_income_race_dotplot(df, county_name, il_value):
    income_limit = df.loc[df["county_name"] == county_name, il_value].values[0]
    df_county = df[df["county_name"] == county_name]
    plot_cols = [col for col in df.columns if 'Median Household Income' in col and "By Race" in col]
    
    df_long = df_county.melt(id_vars=["census_tract"], value_vars=plot_cols, var_name = "Income Type", value_name = "Income")
    df_long = df_long[df_long["Income"] != -666666666]
    df_long['Income Type'] = df_long['Income Type'].apply(lambda x: x.split(' - ')[3] if len(x.split(' - ')) > 3 else x)
    
    fig = px.scatter(
            df_long,
            x='Income',  # Income values on the x-axis
            y='census_tract',  # County names on the y-axis
            color='Income Type',  # Each 'Median Household Income' column as a separate color trace
            title=f"Median Household Income by Race in {county_name}",
            labels={'Income': 'Income ($)', 'census_tract': 'Census Tract'},
        )

    fig.update_layout(
            yaxis_title='Census Tract',
            xaxis_title='Income ($)',
            legend_title='Income Type',
            height=500,
            width = 800,
            showlegend=True,
            
            shapes=[
                dict(
                    type='line',
                    x0=income_limit,  # Position of the vertical line
                    x1=income_limit,
                    y0=0,
                    y1=1,
                    xref='x',
                    yref='paper',  # 'paper' means it spans the entire y-axis range
                    line=dict(color='red', width=2, dash='dash')
                )
            ]
        )

    # Add annotation to display income limit value
    fig.add_annotation(
        x=income_limit,  # Position of the annotation
        y=1,  # Position near the top
        xref="x",
        yref="paper",
        text=f"${income_limit:,.0f}",  # Format the value as currency
        showarrow=False,
        font=dict(size=12, color="black"),
        align='center',
        yshift=10  # Adjust the shift upwards to position text above the line
    )
    fig.show()
    
def create_tract_income_race_dotplot(df, county_name, census_tracts, il_value):
    income_limit = df.loc[df["county_name"] == county_name, il_value].values[0]
    df_county = df[df["county_name"] == county_name]
    df_tracts = df_county[df_county["census_tract"].isin(census_tracts)]
    plot_cols = [col for col in df_tracts.columns if 'Median Household Income' in col and "By Race" in col]
    
    df_long = df_tracts.melt(id_vars=["census_tract"], value_vars=plot_cols, var_name = "Income Type", value_name = "Income")
    df_long = df_long[df_long["Income"] != -666666666]
    df_long['Income Type'] = df_long['Income Type'].apply(lambda x: x.split(' - ')[3] if len(x.split(' - ')) > 3 else x)
    
    fig = px.scatter(
            df_long,
            x='Income',  # Income values on the x-axis
            y='census_tract',  # County names on the y-axis
            color='Income Type',  # Each 'Median Household Income' column as a separate color trace
            title=f"Median Household Income by Race in {county_name}",
            labels={'Income': 'Income ($)', 'census_tract': 'Census Tract'},
        )

    fig.update_layout(
            yaxis_title='Census Tract',
            xaxis_title='Income ($)',
            legend_title='Income Type',
            height=500,
            width = 800,
            showlegend=True,
            
            shapes=[
                dict(
                    type='line',
                    x0=income_limit,  # Position of the vertical line
                    x1=income_limit,
                    y0=0,
                    y1=1,
                    xref='x',
                    yref='paper',  # 'paper' means it spans the entire y-axis range
                    line=dict(color='red', width=2, dash='dash')
                )
            ]
        )

    # Add annotation to display income limit value
    fig.add_annotation(
        x=income_limit,  # Position of the annotation
        y=1,  # Position near the top
        xref="x",
        yref="paper",
        text=f"${income_limit:,.0f}",  # Format the value as currency
        showarrow=False,
        font=dict(size=12, color="black"),
        align='center',
        yshift=10  # Adjust the shift upwards to position text above the line
    )
    fig.show()
    
def create_county_income_age_dotplot(df, county_name, il_value):
    income_limit = df.loc[df["county_name"] == county_name, il_value].values[0]
    df_county = df[df["county_name"] == county_name]
    plot_cols = [col for col in df.columns if 'Median Household Income' in col and "By Age" in col]
    
    df_long = df_county.melt(id_vars=["census_tract"], value_vars=plot_cols, var_name = "Income Type", value_name = "Income")
    df_long = df_long[df_long["Income"] != -666666666]
    df_long['Income Type'] = df_long['Income Type'].apply(lambda x: x.split(' - ')[3] if len(x.split(' - ')) > 3 else x)
    
    fig = px.scatter(
            df_long,
            x='Income',  # Income values on the x-axis
            y='census_tract',  # County names on the y-axis
            color='Income Type',  # Each 'Median Household Income' column as a separate color trace
            title=f"Median Household Income by Age in {county_name}",
            labels={'Income': 'Income ($)', 'census_tract': 'Census Tract'},
        )

    fig.update_layout(
            yaxis_title='Census Tract',
            xaxis_title='Income ($)',
            legend_title='Income Type',
            height=500,
            width = 800,
            showlegend=True,
            
            shapes=[
                dict(
                    type='line',
                    x0=income_limit,  # Position of the vertical line
                    x1=income_limit,
                    y0=0,
                    y1=1,
                    xref='x',
                    yref='paper',  # 'paper' means it spans the entire y-axis range
                    line=dict(color='red', width=2, dash='dash')
                )
            ]
        )

    # Add annotation to display income limit value
    fig.add_annotation(
        x=income_limit,  # Position of the annotation
        y=1,  # Position near the top
        xref="x",
        yref="paper",
        text=f"${income_limit:,.0f}",  # Format the value as currency
        showarrow=False,
        font=dict(size=12, color="black"),
        align='center',
        yshift=10  # Adjust the shift upwards to position text above the line
    )
    fig.show()
    
def create_tract_income_age_dotplot(df, county_name, census_tracts, il_value):
    income_limit = df.loc[df["county_name"] == county_name, il_value].values[0]
    df_county = df[df["county_name"] == county_name]
    df_tracts = df_county[df_county["census_tract"].isin(census_tracts)]
    plot_cols = [col for col in df_tracts.columns if 'Median Household Income' in col and "By Age" in col]
    
    df_long = df_tracts.melt(id_vars=["census_tract"], value_vars=plot_cols, var_name = "Income Type", value_name = "Income")
    df_long = df_long[df_long["Income"] != -666666666]
    df_long['Income Type'] = df_long['Income Type'].apply(lambda x: x.split(' - ')[3] if len(x.split(' - ')) > 3 else x)
    
    fig = px.scatter(
            df_long,
            x='Income',  # Income values on the x-axis
            y='census_tract',  # County names on the y-axis
            color='Income Type',  # Each 'Median Household Income' column as a separate color trace
            title=f"Median Household Income by Age in {county_name}",
            labels={'Income': 'Income ($)', 'census_tract': 'Census Tract'},
        )

    fig.update_layout(
            yaxis_title='Census Tract',
            xaxis_title='Income ($)',
            legend_title='Income Type',
            height=500,
            width = 800,
            showlegend=True,
            
            shapes=[
                dict(
                    type='line',
                    x0=income_limit,  # Position of the vertical line
                    x1=income_limit,
                    y0=0,
                    y1=1,
                    xref='x',
                    yref='paper',  # 'paper' means it spans the entire y-axis range
                    line=dict(color='red', width=2, dash='dash')
                )
            ]
        )

    # Add annotation to display income limit value
    fig.add_annotation(
        x=income_limit,  # Position of the annotation
        y=1,  # Position near the top
        xref="x",
        yref="paper",
        text=f"${income_limit:,.0f}",  # Format the value as currency
        showarrow=False,
        font=dict(size=12, color="black"),
        align='center',
        yshift=10  # Adjust the shift upwards to position text above the line
    )
    fig.show()
    