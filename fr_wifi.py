import geopandas as gpd
import contextily as ctx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load freiburg shapes
fr_base = gpd.read_file('data/stadtbezirke.shp')
# littenweiler is too far away so we dont care
drop_list = ["Waldsee", "Kappel", "Littenweiler"]
fr_base = fr_base[~(fr_base.name.isin(drop_list))]
fr_base = fr_base.to_crs(epsg=4326)

# load building shape file masked on central freiburg
fr_pois = gpd.read_file('data/freiburg-regbez-latest-free.shp/gis_osm_buildings_a_free_1.shp', mask=fr_base)
fr_pois = fr_pois.to_crs(epsg=3857)
fr_pois = fr_pois.dropna(subset=["name"])

# filter buildings by university, hospital and fraunhofer as those offer eduroam
fr_uni = fr_pois[fr_pois["type"]== "university"]
fr_hospital = fr_pois[fr_pois["type"]== "hospital"]
fr_FHG = fr_pois[fr_pois["name"].str.contains("Fraunhofer")]
fr_FHG = fr_FHG.dropna(subset=["type"])
fr_FHG["type"] = ["fraunhofer"]*3

# merge the different buildings into one dataframe
fr_eduroam = fr_uni.append(fr_hospital)
fr_eduroam = fr_eduroam.append(fr_FHG)


#plot it
fig, ax = plt.subplots(figsize=(8,8))
fr_eduroam.plot(ax=ax, column="type", alpha=1, legend=True)

# add basemap background
ctx.add_basemap(ax, zoom=15)
ax.set_axis_off()
plt.title("Buildings offering eduroam in central Freiburg")
plt.show()
