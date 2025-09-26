#%% 
from osgeo import ogr
from os.path import join
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np


root_path = 'ENC_ROOT'

ds = ogr.Open(join(root_path, 'US1GC09M','US1GC09M.000'), 0)  # 0 = read-only
if ds is None:
    raise RuntimeError("Unable to open S-57 file. Check file path, permissions, or whether data is S-63 encrypted.")

print("Layer count:", ds.GetLayerCount())
# %% Reading layers

depare = gpd.read_file(join(root_path, 'US1GC09M','US1GC09M.000'), layer='DEPARE')

soundg = gpd.read_file(join(root_path, 'US1GC09M','US1GC09M.000'), layer='SOUNDG')

z_values = soundg['geometry'].apply(
    lambda multi: [point.z for point in multi.geoms])

z_values = (np.concat(z_values.values))

# %% Create histogram of z_values
plt.hist(z_values, bins=100)
plt.show()

# %%
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.Mercator()})
ss = soundg.plot(ax=ax, cmap='rainbow', markersize=1)
plt.colorbar(ss)
ax.coastlines()
plt.show()
# %%