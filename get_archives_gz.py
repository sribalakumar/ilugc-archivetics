#One time script to get all legacy archives.
import urllib
import os.path

month_list = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
base_url = "http://www.ae.iitm.ac.in/pipermail/ilugc/"
archive_dir = os.path.dirname(os.path.abspath(__file__)) + "/gz_archives/"

for year in range (2000, 2016):
  for month in month_list:
    file_name = str(year)+ "-" + month + ".txt"
    archive_url = base_url + file_name + ".gz"
    dest_file_name = archive_dir + file_name + ".gz"
    try:
      urllib.urlretrieve(archive_url, dest_file_name)
    except:
      print "ERROR: while fetching " + file_name


