from PIL import Image
import numpy as np

def load_image_into_numpy_array(image):
	(im_width, im_height) = image.size
	return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def parse_bounding_box_line(line):
  """Parse a line in the form:

  xmin xmax ymin ymax

  where xmin, xmax, ... are floating point numbers

  into a 4-tuple of floats.

  e.g.,

  1.2 2.3 3.4 4.5
    yields
  [1.2, 2.3, 3.4, 4.5]
  """
  return [float(x) for x in line.split(' ')]

def parse_bounding_box_lines(lines):
  data = np.array(
    [parse_bounding_box_line(line) for line in lines]
  ).T

  labels = ['images/%s' % x for x in ('xmins', 'xmaxs', 'ymins', 'ymaxs')]
  print(data)
  return dict(zip(labels, data))


def create_tf_example(filename, bounding_box_file):
  image_format = b'jpg'
  raw_data = Image.open(filename)
  encoded_image_data = load_image_into_numpy_array(raw_data)

  xmins = [322.0 / 1200.0]
  xmaxs = [1062.0 / 1200.0]
  ymins = [174.0 / 1032.0]
  ymaxs = [761.0 / 1032.0]
  classes_text = ['Cat']
  classes = [1]

  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(filename),
      'image/source_id': dataset_util.bytes_feature(filename),
      'image/encoded': dataset_util.bytes_feature(encoded_image_data),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
  }))
  return tf_example

fn = '/media/sf_Sidewalks/scrapes.tar/scrapes5/scrapes5/cd/CdI636d5z2KNuF8x1qToIg_curbramp.txt'
lines = [x.strip() for x in open(fn).readlines()]
