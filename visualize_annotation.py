"""
Visualize annotations to image file
"""

import sys
import argparse
import cv2
import xml.etree.ElementTree as ET
from pathlib import Path

from annotate import face_parts

def process_file(image_annotation, img_dir, output_dir):
    src_img_path = img_dir / image_annotation.attrib["file"]
    dst_img_path = output_dir / Path(image_annotation.attrib["file"]).name
    if dst_img_path.exists():
        sys.stderr.write(f"File {dst_img_path} already exists. Skipping.\n")
        return
    exist = False
    img = cv2.imread(str(src_img_path))
    for box in image_annotation.findall("box"):
        exist = True
        part_poses = {}
        for part in box.findall("part"):
            attrib = part.attrib
            part_poses[int(attrib["name"])] = (int(attrib["x"]), int(attrib["y"]))
        for _, (bottom, top) in face_parts.items():
            for i in range(bottom-1, top):
                cv2.circle(img, part_poses[i], 3, (0, 255, 255), -1)
                if i >= bottom:
                    cv2.line(img, part_poses[i-1], part_poses[i], (0, 255, 255), 1)
    if exist:
        cv2.imwrite(str(dst_img_path), img)

def main():
    parser = argparse.ArgumentParser(description='Visualize annotations')
    parser.add_argument("xml", help="Path to the anntation xml file")
    parser.add_argument("img", help="Path to the image file directory")
    parser.add_argument("output", help="Path to the output directory")
    args = parser.parse_args()

    annotation_tree = ET.parse(args.xml)

    img_dir = Path(args.img)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    for image_annotation in annotation_tree.findall(".//image"):
        try:
            process_file(image_annotation, img_dir, output_dir)
        except:
            sys.stderr.write(f"Failed to process {image_annotation.attrib['file']}\n")

if __name__ == "__main__":
    main()
