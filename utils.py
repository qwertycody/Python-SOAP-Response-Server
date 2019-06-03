import os as os
import glob as glob
import traceback
import time

def getDirectories():
	files = [f for f in os.listdir('.') if os.path.isdir(f)]
	return files

def getDirectories_Match(parameter_path):
	for id_substring, path  in enumerate(getDirectories()): 
		if path == parameter_path:
			return True
	return False

def getTimestamp():
    return time.strftime("%Y%m%d-%H%M%S")

def getFiles_LatestModified(parameter_directory):
	list_of_files = glob.glob(parameter_directory) # * means all if need specific format then *.csv
	latest_file = max(list_of_files, key=os.path.getmtime)
	return latest_file

def printStackTrace(e):
    print(e)
    traceback.print_tb(e.__traceback__)