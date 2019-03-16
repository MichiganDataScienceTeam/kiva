import pandas as pd
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
        self.df = geopandas.sjoin(self._dhs_dataset.df, self._kiva_dataset.df, how="inner")


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
            self.loan_reg = self.loan_reg[self.loan_reg.country == self.country].dropna(subset=["geocode"])
        self.loan_reg = self.loan_reg.dropna(subset=["geocode"])
        self.loan_reg["geocode"] = self.loan_reg.geocode.apply(pd.eval).apply(lambda x: Point(*x[0]))
        self.loan_reg = geopandas.GeoDataFrame(self.loan_reg, crs=crs, geometry="geocode")
        self.df = pd.merge(left=self.df, right=self.loan_themes_by_id, on="id")
        self.df = pd.merge(left=self.loan_reg, right=self.df, on="Loan Theme ID")


class DHSDataset(object):

    """Docstring for DHSDataset. """

    def __init__(self, filename, shapefile, adm2=False):
        """TODO: to be defined.

        :filename: TODO

        """
        self._filename = filename
        self._shapefile = shapefile
        self.df = pd.read_stata(filename, convert_categoricals=False)
        self.boundaries = geopandas.read_file(shapefile)

        self.preprocess()
        self.join_to_map()

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
