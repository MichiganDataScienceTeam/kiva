import pandas as pd
import pickle as pkl
import geopandas
from shapely.geometry import Point
from pathlib import Path


class JoinedDataset(object):

    """Docstring for JoinedDataset. """

    def __init__(self, kiva_dataset, dhs_dataset):
        """TODO: to be defined1.

        :kiva_dataset: TODO
        :dhs_dataset: TODO

        """
        self._kiva_dataset = kiva_dataset
        self._dhs_dataset = dhs_dataset
        self.df = geopandas.sjoin(self._kiva_dataset.df, self._dhs_dataset.df, how="right", op="intersects")


class KivaMPIDataset(object):
    def __init__(self, datadir, country=None):
        self.cache_path = "./cache/kiva_mpi_dataset.pkl"
        try:
            print("Trying cache")
            self.df = pkl.load(open(self.cache_path))
        except:
            print("Not using cache")
            self._mpi_path = Path(datadir) / "kiva_mpi_region_locations.csv"
            self.country = country
            self.df = pd.read_csv(self._mpi_path)
            self.make_geographic()
            pkl.dump(self.df, open(self.cache_path, 'wb'))

    def make_geographic(self):
        if self.country:
            self.df = self.df[self.df.country == self.country]
        self.df.dropna(subset=["geo"])
        self.df["geocode"] = self.df.geo.apply(pd.eval).apply(lambda x: Point(*x))
        self.df = geopandas.GeoDataFrame(self.df, geometry="geocode")

class KivaDataset(object):

    """Docstring for KivaDataset. """

    def __init__(self, datadir, country=None):
        """
        datadir is the directory with all the kiva dataset files
        """
        self._kiva_loan_region = Path(datadir) / "loan_themes_by_region.csv"
        self._kiva_loan_theme_id = Path(datadir) / "loan_theme_ids.csv"
        self._filename = Path(datadir) / "kiva_loans.csv"
        self.country = country
        self.df = pd.read_csv(self._filename)
        self.loan_reg = pd.read_csv(self._kiva_loan_region)
        self.loan_themes_by_id = pd.read_csv(self._kiva_loan_theme_id)
        self.make_geographic()

    def make_geographic(self):
        # http://www.spatialreference.org/ref/epsg/2263/
        crs = {'init': 'epsg:2263'}  # I don't think this is actually necessary, but see link above
        if self.country:
            self.loan_reg = self.loan_reg[self.loan_reg.country == self.country]
        self.loan_reg = self.loan_reg.dropna(subset=["geocode"])
        self.loan_reg["geocode"] = self.loan_reg.geocode.apply(pd.eval).apply(lambda x: Point(*x[0]))
        self.loan_reg = geopandas.GeoDataFrame(self.loan_reg, crs=crs, geometry="geocode")
        self.df = pd.merge(left=self.df, right=self.loan_themes_by_id, on="id")
        self.df = pd.merge(left=self.loan_reg, right=self.df, on="Loan Theme ID")


class DHSDataset(object):

    """Docstring for DHSDataset. """

    def __init__(self, filename, shapefile, adm2=False, bust_cache=False):
        """TODO: to be defined.

        :filename: TODO

        """
        self.cache_path = "./cache/dhs_dataset.pkl"
        try:
            self.df = pkl.load(open(self.cache_path))
        except:
            self._filename = filename
            self._shapefile = shapefile
            print("Reading Stata File")
            self.df = pd.read_stata(filename, convert_categoricals=False)
            print("Done reading Stata File")
            print("Reading Shapefile")
            self.boundaries = geopandas.read_file(shapefile)
            print("Done reading Shapefile")

            print("Preprocessing")
            self.preprocess()
            print("Finished preprocessing")
            print("Joining Data and Shape")
            self.join_to_map()
            print("Joined Data and Shape")
            pkl.dump(self.df, open(self.cache_path, "wb"))

    def preprocess(self):
        """Keep and rename relevant columns
        """
        fields = {
                "v024": "region",
                "v116": "toilet",
                "v127": "floor_type",
                "v133": "education"
                }

        for key, item in fields.items():
            self.df[item] = self.df[key]
        self.df = self.df[fields.values()]

    def join_to_map(self):
        self.df = pd.merge(left=self.boundaries, right=self.df, left_on="REGCODE", right_on="region")
