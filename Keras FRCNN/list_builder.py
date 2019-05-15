import glob
import os
import sys
import numpy

boxlist = []
boxlist2 = []

for jpg_file in glob.glob('/Volumes/Seagate/scrapes5/*/*.jpg')[0:2000]:
    prefix = os.path.splitext(jpg_file)[0]
    for label in ('curbramp', 'nocurbramp'):
        path = '{}_{}.txt'.format(prefix, label)
        if os.path.exists(path):
        	for line in [x.strip() for x in open(path).readlines()]:
        		xmin, xmax, ymin, ymax = [float(x) for x in line.split(' ')]
        		if not numpy.isnan(xmin) and not numpy.isnan(xmax) and not numpy.isnan(ymin) and not numpy.isnan(ymax):
        			boxline = jpg_file+','+str(int(xmin))+','+str(int(ymin))+','+str(int(xmax))+','+str(int(ymax))+','+label
        			boxlist.append(boxline)

# print(boxlist)
with open("train_data.txt", "w") as f:
	f.write("\n".join(str(x) for x in boxlist))

# for jpg_file in glob.glob('/media/sf_Sidewalks/scrapes.tar/scrapes5/scrapes5/*/*.jpg')[16080:]:
#     prefix = os.path.splitext(jpg_file)[0]
#     for label in ('curbramp', 'nocurbramp'):
#         path = '{}_{}.txt'.format(prefix, label)
#         if os.path.exists(path):
#         	for line in [x.strip() for x in open(path).readlines()]:
#         		xmin, xmax, ymin, ymax = [float(x) for x in line.split(' ')]
#         		if not numpy.isnan(xmin) and not numpy.isnan(xmax) and not numpy.isnan(ymin) and not numpy.isnan(ymax):
#         			boxline = jpg_file+','+str(int(xmin))+','+str(int(ymin))+','+str(int(xmax))+','+str(int(ymax))+','+label
#         			boxlist2.append(boxline)
#         # else:
#         #     sys.stderr.write('warning: box file {} does not exist\n'.format(path))

# # print(boxlist)
# with open("test_data.txt", "w") as f:
# 	f.write("\n".join(str(x) for x in boxlist2))