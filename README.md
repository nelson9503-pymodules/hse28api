# hse28api

28 House API. User can query the data on 28 House via this package.


---

## Methods Discovery

Users should execute the methods below orderly to get essential information for next step.

**func |** ScanID ( propertyType: `str`, numOfThread: `int` ) **->** listOfID: `list`

**func |** ExtractID ( ids: `list`,  propertyType: `str`, numOfThread: `int`) **->** propertiesDetails: `dict`

**func |** DownloadPhoto ( results: `dict`, saveFolderPath: `str`, numOfThread: `int`)