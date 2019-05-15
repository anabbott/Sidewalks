import numpy as np
import tensorflow as tf
import os
import sys
import pprint
import scipy.misc

from object_detection.utils import dataset_util

class BoundingBoxSet(object):
    def __init__(self):
        self.data = {
            'image/object/bbox/xmin': [],
            'image/object/bbox/xmax': [],
            'image/object/bbox/ymin': [],
            'image/object/bbox/ymax': [],
            'image/object/class/text': [],
            'image/object/class/label': [],
        }

    def add_line(self, line, class_name, class_label):
        # Note: this will throw if the line contains bad data (e.g., NaN)
        # Rearrange if the coords are actually in some other order.
        xmin, xmax, ymin, ymax = [float(x) for x in line.split(' ')]
        self.data['image/object/bbox/xmin'].append(xmin)
        self.data['image/object/bbox/xmax'].append(xmax)
        self.data['image/object/bbox/ymin'].append(ymin)
        self.data['image/object/bbox/ymax'].append(ymax)
        self.data['image/object/class/text'].append(class_name)
        self.data['image/object/class/label'].append(class_label)

    def get_feature_dict(self):
        features = {}
        for x in ('xmin', 'xmax', 'ymin', 'ymax'):
            key = 'image/object/bbox/{}'.format(x)
            features[key] = dataset_util.float_list_feature(self.data[key])
        features['image/object/class/text'] = dataset_util.bytes_list_feature(
            self.data['image/object/class/text'])
        features['image/object/class/label'] = dataset_util.int64_list_feature(
            self.data['image/object/class/label'])
        return features

    def __repr__(self):
        return repr(self.data)


class SidewalkExample(object):
    labels_to_ids = {
        'curbramp': 1,
        'nocurbramp': 2
    }

    def __init__(self, prefix, image_type='jpg'):
        self.prefix = prefix
        self.image_file = '.'.join((prefix, image_type))
        self.image_type = image_type
        self.boxes = BoundingBoxSet()

        for label, id in self.labels_to_ids.iteritems():
            path = '{}_{}.txt'.format(prefix, label)
            if os.path.exists(path):
                self._load_bounding_boxes(path, label)
            else:
                sys.stderr.write(
                    'warning: box file {} does not exist\n'.format(path))

    def _load_bounding_boxes(self, path, class_name):
        class_id = self.labels_to_ids[class_name]
        for line in [x.strip() for x in open(path).readlines()]:
            self.boxes.add_line(line, class_name, class_id)

    def get_feature_dict(self):
        image_data = scipy.misc.imread(self.image_file)
        width, height, depth = image_data.shape

        feature_dict = {
            'image/height' : dataset_util.int64_feature(height),
            'image/width' : dataset_util.int64_feature(width),
            'image/filename' : dataset_util.bytes_feature(self.image_file),
            'image/source_id' : dataset_util.bytes_feature(self.image_file),
# NOTE: uncomment the next line to actually load the image data.
# It is commented out so that when we print it we don't flood the screen with
# the raw bytes of the image.
            #'image/encoded' : dataset_util.bytes_feature(image_data.tobytes()),
            'image/format' : dataset_util.bytes_feature(self.image_type),
            }

        feature_dict.update(self.boxes.get_feature_dict())
        return feature_dict

    def make_tf_example(self):
        return tf.train.Example(features=tf.train.Features(
            feature=self.get_feature_dict()))



def main(argv):
    print(argv)
    if len(argv) != 2:
        print('Usage: {} <image_data_prefix>'.format(argv[0]))
        sys.exit(1)
    prefix = sys.argv[1]
    example = SidewalkExample(prefix)
    pp = pprint.PrettyPrinter()
    print('Feature dict:')
    pp.pprint(example.get_feature_dict())
    print('tf.Example proto:')
    pp.pprint(example.make_tf_example())

if __name__ == '__main__':
    main(sys.argv)
