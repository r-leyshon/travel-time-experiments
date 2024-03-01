"""Utilities for engineering GeoDataFrames."""
import geopandas as gpd
from haversine import haversine, Unit
from shapely.geometry import LineString

def add_linestring_col(
    gdf: gpd.GeoDataFrame,
    new_colnm: str = "lines",
    geom_col: str = "geometry",
    snapped_col:str = "snapped_geometry",
    calc_haversine: bool = True,
    haversine_colnm: str = "snap_dist_m"
    ) -> gpd.GeoDataFrame:
    """Add a new column to gdf, a line between original & snapped geometry."""
    out_gdf = gdf.copy(deep=True)
    # create the LineString geometry
    out_gdf[new_colnm] = out_gdf.apply(
    lambda row: LineString([row[geom_col], row[snapped_col]]),
    axis=1
    )
    if calc_haversine:
        # reverse the lonlat to latlon
        out_gdf[haversine_colnm] = out_gdf.apply(
            lambda row:haversine(
                (row[geom_col].y, row[geom_col].x),
                (row[snapped_col].y, row[snapped_col].x),
                unit=Unit.METERS), axis=1)

    return out_gdf
