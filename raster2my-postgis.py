import json
import os
import sys
import subprocess
import argparse
from argparse import RawTextHelpFormatter

py_path = __file__.replace("raster2my-postgis.py", "")
hosts_path = py_path + 'hosts.txt'


def create_profile(profile_name, dbname, host, user, pw):
    with open(hosts_path) as json_file:
        profiles = json.load(json_file)

    profiles[profile_name] = {
        "dbname": dbname,
        "host": host,
        "user": user,
        "pw": pw
    }

    with open(hosts_path, 'w') as outfile:
        json.dump(profiles, outfile)


def get_profile(profile_name):
    with open(hosts_path) as json_file:
        profiles = json.load(json_file)

        return profiles[profile_name]


def get_profiles():
    with open(hosts_path) as json_file:
        profiles = json.load(json_file)

        return profiles.keys()


def delete_profile(profile_name):
    with open(hosts_path) as json_file:
        profiles = json.load(json_file)

    del profiles[profile_name]

    with open(hosts_path, 'w') as outfile:
        json.dump(profiles, outfile)


def db_upload(profile, db_schema, db_target_table, epsg, path, single=False):
    db_user = profile["user"]
    db_name = profile["dbname"]
    db_host = profile["host"]
    db_password = profile["pw"]

    if not single:
        if path == "cwd":
            path = os.getcwd() + "/"
            path += "*.tif"

        else:
            if path[-1] != "/":
                path += "/"

            path += "*.tif"

    # Set pg password environment variable - others can be included in the statement
    os.environ['PGPASSWORD'] = db_password

    # Build command string
    cmd = f'raster2pgsql -s {epsg} -C -F -t auto -l 2,4,8,16,32,64,128,256 {path} {db_schema}.{db_target_table} | ' \
          f'psql -U {db_user} -d {db_name} -h {db_host} -p 5432 '

    # Execute
    subprocess.call(cmd, shell=True)


parser = argparse.ArgumentParser(description="""
A simple tool to upload geospatial raster data to your postgis-database.
Usage:
(1) Upload multiple raster to single table: 'raster2my-postgis profile dir epsg schema table' (type 'cwd' instead of directory to use current working directory)
(2) Upload a single raster: 'raster2my-postgis profile dir epsg schema table -s ' 
(3) Bulk upload multiple raster to separate tables: 'raster2my-postgis profile dir epsg schema -b'
(4) Create Database profile: 'raster2my-postgis -n'
(5) Remove Database profile: 'raster2my-postgis -r profile name'
(6) List Profiles: 'raster2my-postgis -l'\n"""
                                 , formatter_class=RawTextHelpFormatter
                                 )

parser.add_argument("profile", type=str, nargs="?", help="an already stored profile with database information")
parser.add_argument("dir", type=str, nargs="?", help="the directory of tifs or the single file to upload, "
                                                     "type 'cwd'  as the directory name to uploade all files"
                                                     " in the current directory.")

parser.add_argument("epsg", type=int, nargs="?", help="the epsg-code of the files")
parser.add_argument("schema", type=str, nargs="?", help="the schema in which the files will be stored")
parser.add_argument("table", type=str, nargs="?", help="the table that will be created in the db")

parser.add_argument("-single", "-s", action="store_true", help="specify single file upload")
parser.add_argument("-bulk", "-b", action="store_true", help="upload every raster to seperate tabel")
parser.add_argument("-new", "-n", action="store_true", help="create a new profile")
parser.add_argument("-remove", "-r", action="store_true", help="remove profile")
parser.add_argument("-list", "-l", action="store_true", help="list profiles")

args = parser.parse_args()

if args.new:
    print("Create new profile, please submit the data.")
    profname = input("Profile name: ")

    if profname in get_profiles():
        print("Error: Profile already exists!")
        sys.exit()

    dbname = input("Name of the Database:")
    host = input("Host address: ")
    dbuser = input("DB username: ")
    pw = input("Password: ")

    create_profile(profname, dbname, host, dbuser, pw)
    print("Created profile successfully!\n")
    sys.exit()

if args.remove:

    if args.profile not in get_profiles():
        print("Error: Profile does not exist")
        sys.exit()

    delete_profile(args.profile)

    print("Deleted Profile successfully")
    sys.exit()

if args.list:
    print("Profiles:")
    for prof in get_profiles():
        print(prof)
    sys.exit()

if args.bulk:
    if args.dir == "cwd":
        cwd = os.getcwd() + "/"
        content = os.listdir(cwd)
        content = [(file[:-4], cwd + file) for file in content if file[-4:] == ".tif"]

    else:

        path = args.dir
        if path[-1] != "/":
            path += "/"

        content = os.listdir(path)

        content = [(file[:-4], path + file) for file in content if file[-4:] == ".tif"]

    for file,file_path in content:
        db_upload(get_profile(args.profile), args.schema, file, args.epsg, file_path, single=True)
    sys.exit()


if args.single:
    db_upload(get_profile(args.profile), args.schema, args.table, args.epsg, args.dir, single=True)
    sys.exit()


for name,argument in [("profile",args.profile), ("schema",args.schema), ("table", args.table),
                      ("epsg",args.epsg), ("dir", args.dir)]:

    if argument is None:
        print(f"Error: missing argument {name}")
        sys.exit()


profile = get_profile(args.profile)
db_upload(profile, args.schema, args.table, args.epsg, args.dir)
