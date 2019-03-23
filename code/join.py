from dhs import KivaDataset, KivaMPIDataset, DHSDataset, JoinedDataset

print("Loading Kiva Datasets")
kivads = KivaMPIDataset("./data/kiva/", country="Philippines")
print("Loaded Kiva Datasets")
print(kivads.df.head())

print("Loading DHS Datasets")
dhsds = DHSDataset("./data/dhs_raw/PHIR70FL.DTA", "./data/shps/sdr_subnational_boundaries.shp")
print("Loaded DHS Datasets")
print(dhsds.df.head())

print("Joining spatially")
joined = JoinedDataset(kivads, dhsds)
print("Joined")

print(joined.df.head())
