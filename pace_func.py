import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

def process_l2(path):

    prod = xr.open_dataset(path)
    obs = xr.open_dataset(path, group="geophysical_data")
    nav = xr.open_dataset(path, group="navigation_data")
    nav = (
        nav
        .set_coords(("longitude", "latitude"))
    )
    dataset = xr.merge((prod, obs, nav.coords))

    return dataset

def log_chl(dataset):
    array = np.log10(dataset["chlor_a"])
    array.attrs.update(
        {
            "units": f'log10({dataset["chlor_a"].attrs["units"]})',
        }
    )
    return array

def plot_full(array):
    fig = plt.figure(figsize=(10, 7))
    ax = plt.axes(projection=cartopy.crs.PlateCarree())
    array.plot(x="longitude", y="latitude", cmap="viridis", robust=True, ax=ax)
    ax.coastlines()
    ax.gridlines(draw_labels={"bottom": "x", "left": "y"})
    ax.set_title(dataset.attrs["product_name"], loc="center")
    plt.show()

#  Function to extract spectra for a given lat/lon
def target_spectra(dataset, target_lat, target_lon):
    
    lat_diff = np.abs(dataset["latitude"] - target_lat)
    lon_diff = np.abs(dataset["longitude"] - target_lon)
    
    distance = lat_diff + lon_diff  # Total difference in lat/lon space
    nearest_point = distance.argmin(dim=("number_of_lines", "pixels_per_line"))  # Find index of the minimum
    
    nearest_rrs = dataset["Rrs"].isel(
        number_of_lines=nearest_point["number_of_lines"], 
        pixels_per_line=nearest_point["pixels_per_line"]
    )
    
    return nearest_rrs


def subset_xr(dataset, N, S, E, W):

    sub_box = dataset.where(((dataset["latitude"] > S) & (dataset["latitude"] < N)
                             & (dataset["longitude"] > W) & (dataset["longitude"] < E)), drop=True)
    return sub_pox

