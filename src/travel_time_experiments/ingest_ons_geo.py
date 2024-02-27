import geopandas as gpd
import pandas as pd
import requests


def get_ons_geo_data(endpoint:str, params:dict) -> gpd.GeoDataFrame:
    "Get first response - no pagination. Cast json response to gdf"
    resp = requests.get(endpoint, params=params)
    if resp.ok:
        content = resp.json()
    else:
        raise requests.RequestException(
            f"HTTP {resp.status_code} : {resp.reason}")
    gdf = gpd.GeoDataFrame.from_features(
        content["features"], crs=content["crs"]["properties"]["name"])
    return content, gdf


def get_ons_geo_paginated(endpoint:str, params:dict) -> gpd.GeoDataFrame:
    """Get data from endpoint with pagination."""
    content, gdf = get_ons_geo_data(endpoint, params)
    more_pages = content["properties"]["exceededTransferLimit"]
    offset = len(gdf) # number of records to offset by
    all_gdfs = gdf # append gdfs here
    while more_pages:
        params["resultOffset"] += offset # increment the records
        content, gdf = get_ons_geo_data(endpoint, params)
        all_gdfs = pd.concat([all_gdfs, gdf])
        try:
            more_pages = content["properties"]["exceededTransferLimit"]
        except KeyError:
            # rather than exceededTransferLimit = False, it disappears...
            more_pages = False
    all_gdfs = all_gdfs.reset_index(drop=True)
    return all_gdfs

