from FactTableStagingP1 import data_staging_phase_one
from FactTableStagingP2 import data_staging_phase_two
from OttawaAccidentHourTableUnbucketize import unbucketizeHourTable
from OttawaAccidentLocationUnbucketize import unbucketizeLocationTable
from PrefilteringWeatherData import prefilteringWeatherData

prefilteringWeatherData()

unbucketizeHourTable()

unbucketizeLocationTable()

data_staging_phase_one("LOOKUP_TABLE_2014.csv", "2014ProcessedCollisionHourList.csv", "Staging_1_Main",
                       "Staging_1_Hour")

data_staging_phase_two("Staging_1_Main.csv", "2014ProcessedCollisionLocationList.csv", "Staging_2_Main",
                       "Staging_2_Location")
