"""Utilities to help visualise gpd DataFrames."""

from typing import Union

import folium
import geopandas as gpd

def viz_revised_coordinates(
    gdf: gpd.GeoDataFrame,
    zoom:Union[int, float] = 9,
    snapped_geom="snapped_geometry",
    line_geom="lines") -> folium.Map:
    """Visualise coordinate revisions."""
    # layer 1
    imap = gdf.explore(
        marker_type="marker",
        marker_kwds={
            "icon": folium.map.Icon(color="red", icon="ban", prefix="fa"),
        },
        map_kwds={
            "center": {"lat": 51.583, "lng": -0.018}
        },
        zoom_start=zoom,
    )
    # layer 2
    imap = gdf.set_geometry(snapped_geom).explore(
        m=imap,
        marker_type="marker",
        marker_kwds={
            "icon": folium.map.Icon(
                color="green", icon="person-walking", prefix="fa"),
        }
    )
    # layer 3
    imap = gdf.set_geometry(line_geom).explore(
        m=imap,
    )
    return imap
