import os
from glob import glob
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
import cv2

dir = "../../DATASET/license_plate_dataset_13_sep_2019/images/train/*"
print(len(glob(dir)))


def create_label(folder_path, img_filename):
    full_img_path = os.path.join(folder_path, img_filename)
    full_txt_path = full_img_path.replace("jpg", "txt").replace("images", "labels")
    print(full_txt_path)
    img_cv = cv2.imread(full_img_path)
    h, w, d = img_cv.shape
    h, w, d = str(h), str(w), str(d)
    xml_name = img_filename.replace("jpg", "xml")
    annotation = ET.Element("annotation")
    tree = ElementTree(annotation)
    folder = ET.SubElement(annotation, "folder")
    folder.text = folder_path
    filename = ET.SubElement(annotation, "filename")
    filename.text = img_filename
    size = ET.SubElement(annotation, "size")
    width = ET.SubElement(size, "width")
    width.text = w
    height = ET.SubElement(size, "height")
    height.text = h
    depth = ET.SubElement(size, "depth")
    depth.text = d

    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = "0"
    object = ET.SubElement(annotation, "object")
    name = ET.SubElement(object, "name")
    name.text = "face"
    pose = ET.SubElement(object, "pose")
    pose.text = "Unspecified"
    truncuted = ET.SubElement(object, "truncated")
    truncuted.text = "0"
    difficult = ET.SubElement(object, "difficult")
    difficult.text = "0"
    bndbox = ET.SubElement(object, "bndbox")
    with open(full_txt_path, encoding="utf8", errors='ignore') as f_label:
        label_str = f_label.readline()
        label_str = label_str.split(",")
        label_str = label_str[:4]
        x_min, y_min, x_max, y_max, = label_str
        x_min_ET = ET.SubElement(bndbox,"xmin")

        y_min_ET = ET.SubElement(bndbox,"ymin")
        x_max_ET = ET.SubElement(bndbox,"xmax")
        y_max_ET = ET.SubElement(bndbox,"ymax")

        x_min_ET.text = x_min
        y_min_ET.text = y_min
        x_max_ET.text = x_max
        y_max_ET.text = y_max

    f = open("results/{}".format(xml_name), 'w')
    f.write(ET.tostring(annotation).decode())
    f.close()


def create_list_of_labels(image_dir):
    images = os.listdir(image_dir)
    for img in images:
        create_label(image_dir, img)


create_list_of_labels("license_plate_dataset_13_sep_2019/images/train")
create_list_of_labels("license_plate_dataset_13_sep_2019/images/val")
