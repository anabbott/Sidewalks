README
Since the total file size is around 125GB and Box max a maximum file upload size of 15GB we have split the file into 10 GB sized chunks using the linux split command 


split -b 10G scrapes5.tar.gz “scrapes5.tar.gz”


This generates files of 10 GB each with the prefix scrapes5.tar.gz. In order to recover the original file run the following in the directory where the chunks are stored:


cat scrapes5.tar.gz* > scrapes.tar.gz 


Now extract the scrapes.tar.gz file. 
________________


We currently have files grouped into folders corresponding to the first two characters of the panorama ID they are associated with. Some of the metadata for the panoramas and accessibility labels can be parsed from the filenames. The metadata currently present in the data included are:
1. Google Street View Panorama ID <panoid>
2. The type of label <label_type>
3. The latitude and longitude of the panorama <lat> and <lng>: This can be used as a proxy for the coordinates of the labels. 
4. Pixel coordinates (x1,x2,y1,y2) on the panorama image of the bounding boxes associated with each label.
The (lat,lng) of individual labels and label severity need to be added in the future.


Each panorama is associated with at least 3 types of files. The filenames of these begin with the panorama id (panoid). 
1. <panoid>.jpg: The panorama image file.
2. <panoid>.xml: This contains metadata related to the panorama. The attributes of the data_properties_elevation element include <lat> and <lng>. Optional: The street information is also available as a descendent of this element. 
3. <panoid>.depth.txt: which is just the depth data extracted from the xml and converted into a matrix form that can be more easily read.
4. <panoid>_<label_type>.txt: If there are Curbramp or Missing Curbramp labels on the panorama, the bounding boxes for those labels will be in <panoid>_curbramp.txt and <panoid>_nocubramp.txt respectively. Each line these files has tab-seperated pixel coordinates (x1,x2,y1,y2) for a single label’s bounding box (See figure 1). (x1,y1) represents the top left corner of the bounding box. The center of the bounding box ((x1+x2)/2,(y1+y2)/2) can be used as a proxy for the location of the label. Some points that need to be mentioned:
   1. The crop coordinates are estimates and some percentage of these crops may not recover the pixels associated with the issue.
   2. The coordinates may include negative values due to the proximity of the bounding box to the image boundary.
   3. Note: importantly, in the future, we will also include the exact label position (x,y) instead of or in addition to the crop position. The crop positions are inferences based on point positions of the labels. We will also include: severity information and all label types (currently, the label types are restricted to curb ramps and missing curb ramps).




 pano_crop_example.jpg 

Figure 1. Example of how to visualize the coordinates associated with a label on a panorama image