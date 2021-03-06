# raster2my-postgis


A simple tool to upload geospatial raster data to your postgis-database. Requires raster2pgsql!
It allows you to store database information and automates pyramid layers as well as bulk uploads.
Usage:  
1. Upload multiple raster to single table: `raster2my-postgis profile dir epsg schema table` (type 'cwd' instead of directory to use current working directory)
2. Upload a single raster: `raster2my-postgis profile dir epsg schema table -s` 
3. Bulk upload multiple raster to separate tables: `raster2my-postgis profile dir epsg schema -b`
4. Create database profile: `raster2my-postgis -n`
5. Remove database profile: `raster2my-postgis -r profilename`
6. List profiles: `raster2my-postgis -l`

## Positional arguments:  
  **profile:**      an already stored profile with database information  
  **dir:**          the directory of tifs or the single file to upload, type 'cwd'  as the directory name to uploade all files in the current directory.  
  **epsg:**         the epsg-code of the files  
  **schema:**       the schema in which the files will be stored  
  **table:**        the table that will be created in the db  

## Optional arguments:
  **-h, --help:**   show this help message and exit  
  **-single, -s:**  specify single file upload  
  **-bulk, -b:**    upload every raster to seperate tabel, name of the table is the filename of the tif  
  **-new, -n:**     create a new profile  
  **-remove, -r:**  remove profile  
  **-list, -l:**    list profiles  

