#One time script to extract the gz archives
import gzip
import glob
import os.path
source_dir = os.path.dirname(os.path.abspath(__file__)) + "/gz_archives/"
dest_dir = os.path.dirname(os.path.abspath(__file__)) + "/archives/"

for src_name in glob.glob(os.path.join(source_dir, '*.gz')):
  base = os.path.basename(src_name)
  dest_name = os.path.join(dest_dir, base[:-3])
  try:
    with gzip.open(src_name, 'rb') as infile:
      with open(dest_name, 'w') as outfile:
        for line in infile:
          outfile.write(line)
  except:
    print "ERROR: with " + src_name