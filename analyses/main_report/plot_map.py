import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt

from shapely.geometry import Point
from src.data_cleaning.processing import processing_result_for_map

ukr = gpd.read_file("data/raw/ADMIN_1.shp") # EPSG:4326 format
# Select administrative regions of interest
warzone = ukr[ukr["NAME_LAT"].isin(["Khersonska", "Avtonomna Respublika Krym", "Zaporizka", "Donetska", "Luhanska", "Sevastopol"])]
loc_data = pd.read_csv("data/derived/loc_data.csv", index_col=0)
loc_data = processing_result_for_map(loc_data)
# Use latitude and longitude to create a Point object for each location
geometry = [Point(lon, lat) for lon, lat in zip(loc_data["longitude"], loc_data["latitude"])]
geo_data = gpd.GeoDataFrame(loc_data, geometry=geometry)
geo_data.set_crs(epsg=4326, inplace=True) # Match the downloaded map's EPSG
# Same location may appear under different names --> group by latitude and longitude and count occurrences
grouped = geo_data.groupby(["latitude", "longitude"]).count().reset_index()
# Create auxiliary dataframe for count data for scatterplot
new_geometry = [Point(lon, lat) for lon, lat in zip(grouped["longitude"], grouped["latitude"])]
new_geo_data = gpd.GeoDataFrame(grouped, geometry=new_geometry)
new_geo_data.set_crs(epsg=4326, inplace=True)
# Project everything onto correct EPSG for plotting
warzone = warzone.to_crs(epsg=3857)
new_geo_data = new_geo_data.to_crs(epsg=3857)
# Select cities of interest to point out in the plot
bk = geo_data[geo_data["name"] == "Bakhmut"].to_crs(epsg=3857)
x_bk, y_bk = bk.iloc[0, -1].x, bk.iloc[0, -1].y
ro = geo_data[geo_data["name"] == "Rostov"].to_crs(epsg=3857)
x_ro, y_ro = ro.iloc[0, -1].x, ro.iloc[0, -1].y

plt.rc("text", usetex=True)
plt.rc("font", family="cm")

fig, ax = plt.subplots(1, 1, figsize=(8, 5))
warzone.plot(ax=ax, alpha=0.5, edgecolor="#758D99", lw=0.25, color="#D1B07C")
new_geo_data.plot(ax=ax, color="#DB444B", markersize=2*new_geo_data["name"], alpha=0.5)
ax.set_axis_off()
ax.set_xlim((3.5e6, 4.5e6))
ax.set_ylim((5.5e6, 6.5e6))
# Fictitious points for the legend
ax.scatter(0, 0, s=2, color="#DB444B", alpha=0.5, label="1")
ax.scatter(0, 0, s=10, color="#DB444B", alpha=0.5, label="5")
ax.scatter(0, 0, s=40, color="#DB444B", alpha=0.5, label="20")
# Lines for the cities of interest
ax.vlines(x_bk, ymin=y_bk, ymax=y_bk + 1.7e5, color="#0C0C0C", lw=0.5, alpha=0.8)
ax.text(0.74, 0.86, "Bakhmut", fontsize=8, color="#3F5661", transform=ax.transAxes)
ax.vlines(x_ro, ymin=y_ro, ymax=y_ro - 1e5, color="#0C0C0C", lw=0.5, alpha=0.8)
ax.text(0.875, 0.35, "Rostov", fontsize=8, color="#3F5661", transform=ax.transAxes)
# Add basemap in correct EPSG
ctx.add_basemap(ax=ax, crs=warzone.crs, attribution=False, source=ctx.providers.CartoDB.VoyagerNoLabels, zoom=7)
legend = ax.legend(fontsize=8, loc="upper left", ncols=3, edgecolor="#758D99", labelspacing=0.75)
legend.set_title(title="Total mentions of cities, towns and villages", prop={"size":9})
legend.get_title().set_color("#3F5661")
legend.get_frame().set_linewidth(0.25)
for text in legend.get_texts():
    text.set_color("#3F5661")
fig.savefig("outputs/main_report/figures/map.pdf", dpi=300, bbox_inches="tight")

