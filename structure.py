#Mount Kenya file structure#
#M:\pay-data\data\pay\Kenya\MKN\incoming

# import
import os
import shutil
import datetime
from datetime import datetime
import re #regex
import yaml
import csv
from csv import DictReader
import sys


config = '/home/sdanioth/Documents/git/file_directory/file_directory/config.yaml'

with open(os.path.abspath(config), "r") as f:
    config = yaml.safe_load(f)
    f.close()

if sys.argv[1] == "MKN":
    source = os.path.expanduser(config['sourceMKN'])
    general_dir = config['generalPathMKN']

elif sys.argv[1] == "NRB":
    source = os.path.expanduser(config['sourceNRB'])
    general_dir = config['generalPathNRB']



with open(source, "r") as read_obj:

    csv_reader = DictReader(read_obj)

    for row in csv_reader:
        # all files in directory
        files = os.listdir(general_dir+row["file_path"])

        for file in files:

            if file.startswith(row["file_start"]) and file.endswith(row["file_end"]):
                # extract date from filename
                date_string = re.search(r"\d{4}\d{2}\d{2}", file)[0]
                date = datetime.strptime(date_string, "%Y%m%d")

                year = str(date.year)
                month = str(date.month)
                day = str(date.day)

                dir = general_dir+row["file_path"]
                dir_yearly = dir+year
                dir_monthly = dir_yearly+"/"+month
                dir_daily = dir_monthly+"/"+day


                if row["division"] == "daily":
                    if not os.path.exists(dir_daily):
                        os.makedirs(dir_daily)

                    shutil.move(dir+file,dir_daily+"/"+file)

                elif row["division"] == "monthly":
                    if not os.path.exists(dir_monthly):
                        os.makedirs(dir_monthly)

                    shutil.move(dir+file, dir_monthly+"/"+file)

                elif row["division"] == "yearly":
                    if not os.path.exists(dir_yearly):
                        os.makedirs(dir_yearly)

                    shutil.move(dir+file, dir_yearly+"/"+file)