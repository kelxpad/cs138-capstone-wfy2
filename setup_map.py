import geopandas as gpd
import numpy as np
import numpy.typing as npt
from shapely.geometry import Point
from dataclasses import dataclass

@dataclass
class Location:
    name: str
    latitude: float
    longitude: float

def main():
    SPACING = 50

    ## Load map
    boundary = gpd.read_file(                       ## Coordinates are in (lat, long)
        "assets/ph.national-capital-region.metropolitan-manila.quezon-city.any.geo.json"
    )

    ## Convert to UTM Zone 51N
    boundary = boundary.to_crs(epsg=32651)          ## Coordinates are in (x [meters], y [meters]) 
    xmin, ymin, xmax, ymax = boundary.total_bounds 

    ## Generate valid x and y coordinates
    xs: npt.NDArray[np.float64] = np.arange(
        xmin + SPACING / 2, xmax, SPACING, dtype=np.float64
    )

    ys: npt.NDArray[np.float64] = np.arange(
        ymin + SPACING / 2, ymax, SPACING, dtype=np.float64
    )

    ## Generate points
    points: list[Point] = [
        Point(x, y)
        for x in xs
        for y in ys
    ]

    ## Reject points that go out of bounds
    area = boundary.geometry.union_all()
    points = [
        point for point in points
        if area.covers(point)
    ]

    grid = gpd.GeoDataFrame(
        geometry=points,
        crs="EPSG:32651"
    )

    print(points)
    print(grid)
    # grid.to_file("grid.geojson", driver="GeoJSON")

def convert_latlong_to_projected(p: Point):
    pass

if __name__ == "__main__":
    main()