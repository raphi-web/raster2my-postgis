# raster2my-postgis

A simple tool to upload geospatial raster data to your postgis-database.  
Usage:  
1. Upload raster: 'raster2my-postgis profile dir epsg schema table' (type 'cwd' instead of directory to use current working directory)
2. Create Database profile: 'raster2my-postgis -n'
3. Remove Database profile: 'raster2my-postgis -r profile name'
4. List Profiles: 'raster2my-postgis -l'

## Positional arguments:  
  **profile:**      an already stored profile with database information  
  **dir:**          the directory of tifs or the single file to upload, type 'cwd'  as the directory name to uploade all files in the current directory.  
  **epsg:**         the epsg-code of the files  
  **schema:**       the schema in which the files will be stored  
  **table:**        the table that will be created in the db  

## Optional arguments:  
  **-h, --help:**   show this help message and exit  
  **-file, -f:**    specify single file upload  
  **-new, -n:**     create a new profile  
  **-remove, -r:**  remove profile  
  **-list, -l:**    list profiles  
