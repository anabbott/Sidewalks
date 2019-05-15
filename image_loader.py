from PIL import Image
import numpy as np
import scipy.misc


def _parse_bounding_box_line(line):
  return [float(x) for x in line.split(' ')]

def _parse_bounding_box_lines(lines):
  data = np.array(
    [_parse_bounding_box_line(line) for line in lines]
  ).T

  labels = ['images/%s' % x for x in ('xmins', 'xmaxs', 'ymins', 'ymaxs')]
  return dict(zip(labels, data))

def _maybe_parse_coordinate_file(path, label_text, label_id):
  try:
    data = _parse_bounding_box_lines(
      [x.strip() for x in open(path).readlines()]
    )

    return _parse_bounding_box_lines(lines)
  except IOError as ex:
    print(ex) 
    return None
 
class ImageLoader(object):
  def __init__(self, prefix, image_type='jpg'):
    self.image_file = '.'.join((prefix, image_type))
    self.curbramp_file = '{}_curbramp.txt'.format(prefix)
    self.nocurbramp_file = '{}_nocurbramp.txt'.format(prefix)

    self.image_data = scipy.misc.imread(self.image_file)
    self.curbramp_boxes = _maybe_parse_coordinate_file(self.curbramp_file)
    self.nocurbramp_boxes = _maybe_parse_coordinate_file(self.nocurbramp_file)

   

    print(self.curbramp_boxes)

    
#def create_tf_example(filename, bounding_box_file):
#  image_format = b'jpg'
#
#  xmins = [322.0 / 1200.0]
#  xmaxs = [1062.0 / 1200.0]
#  ymins = [174.0 / 1032.0]
#  ymaxs = [761.0 / 1032.0]
#  classes_text = ['Cat']
#  classes = [1]
#
#  tf_example = tf.train.Example(features=tf.train.Features(feature={
#      'image/height': dataset_util.int64_feature(height),
#      'image/width': dataset_util.int64_feature(width),
#      'image/filename': dataset_util.bytes_feature(filename),
#      'image/source_id': dataset_util.bytes_feature(filename),
#      'image/encoded': dataset_util.bytes_feature(encoded_image_data),
#      'image/format': dataset_util.bytes_feature(image_format),
#      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
#      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
#      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
#      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
#      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
#      'image/object/class/label': dataset_util.int64_list_feature(classes),
#  }))
#  return tf_example

prefix = '/media/sf_Sidewalks/scrapes.tar/scrapes5/scrapes5/cd/CdI636d5z2KNuF8x1qToIg'
loader = ImageLoader(prefix)

