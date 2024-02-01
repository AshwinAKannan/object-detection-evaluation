import json
import os
from xml.dom.minidom import Document
from engine.utils.enums import BBoxType
import requests


def download_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        with open(save_path, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {image_url}: {e}")
        

def coco_to_pascalvoc(coco_annotations_file, output_directory, bbox_type=BBoxType.GROUND_TRUTH):
    # Load COCO annotations
    with open(coco_annotations_file, 'r') as f:
        coco_data = json.load(f)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Iterate over images in COCO annotations
    for image_info in coco_data['images']:
        image_directory = output_directory
        image_id = image_info['id']
        image_filename = image_info['file_name']
        print(image_filename)
        image_width = image_info['width']
        image_height = image_info['height']
    
        image_url = image_info.get('coco_url') 

        # Download image if bbox_type is GROUND_TRUTH
        if bbox_type == BBoxType.GROUND_TRUTH and image_url:
            image_save_path = os.path.join(output_directory, image_filename)
            try:
                download_image(image_url, image_save_path)
            except requests.exceptions.RequestException as e:
                continue

        # Create a new XML document for this image
        doc = Document()
        
        # Create the root element
        annotation = doc.createElement('annotation')
        doc.appendChild(annotation)
        
        # Add image information to the annotation
        folder = doc.createElement('folder')
        folder.appendChild(doc.createTextNode(image_directory))
        annotation.appendChild(folder)
        
        filename = doc.createElement('filename')
        filename.appendChild(doc.createTextNode(image_filename))
        annotation.appendChild(filename)
        
        size = doc.createElement('size')
        annotation.appendChild(size)
        
        width = doc.createElement('width')
        width.appendChild(doc.createTextNode(str(image_width)))
        size.appendChild(width)
        
        height = doc.createElement('height')
        height.appendChild(doc.createTextNode(str(image_height)))
        size.appendChild(height)
        
        depth = doc.createElement('depth')
        depth.appendChild(doc.createTextNode('3'))  # Assuming RGB images
        size.appendChild(depth)
        
        # Find annotations for this image
        annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] == image_id]
        
        for ann in annotations:
            category_id = ann['category_id']
            category_info = next(cat for cat in coco_data['categories'] if cat['id'] == category_id)
            category_name = category_info['name']

            bbox = ann['bbox']
            
            xmin, ymin, width, height = map(float, bbox)
            xmax, ymax = xmin + width, ymin + height
            
            # Create object element for each annotation
            object_elem = doc.createElement('object')
            annotation.appendChild(object_elem)
            
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode(category_name))
            object_elem.appendChild(name)
            
            pose = doc.createElement('pose')
            pose.appendChild(doc.createTextNode('Unspecified'))
            object_elem.appendChild(pose)
            
            truncated = doc.createElement('truncated')
            truncated.appendChild(doc.createTextNode('0'))
            object_elem.appendChild(truncated)
            
            difficult = doc.createElement('difficult')
            difficult.appendChild(doc.createTextNode('0'))
            object_elem.appendChild(difficult)
            
            bndbox = doc.createElement('bndbox')
            object_elem.appendChild(bndbox)
            
            xmin_elem = doc.createElement('xmin')
            xmin_elem.appendChild(doc.createTextNode(str(xmin)))
            bndbox.appendChild(xmin_elem)
            
            ymin_elem = doc.createElement('ymin')
            ymin_elem.appendChild(doc.createTextNode(str(ymin)))
            bndbox.appendChild(ymin_elem)
            
            xmax_elem = doc.createElement('xmax')
            xmax_elem.appendChild(doc.createTextNode(str(xmax)))
            bndbox.appendChild(xmax_elem)
            
            ymax_elem = doc.createElement('ymax')
            ymax_elem.appendChild(doc.createTextNode(str(ymax)))
            bndbox.appendChild(ymax_elem)

            if bbox_type == BBoxType.DETECTION:
                detection_score = ann['score']
                detection_score_elem = doc.createElement('score')
                detection_score_elem.appendChild(doc.createTextNode(str(detection_score)))
                object_elem.appendChild(detection_score_elem)

        # Save the annotation XML file with proper indentation
        annotation_filename = os.path.splitext(image_filename)[0] + '.xml'
        annotation_path = os.path.join(output_directory, annotation_filename)
        with open(annotation_path, 'w') as annotation_file:
            annotation_file.write(doc.toprettyxml())


if __name__ == "__main__":
    coco_annotations_file = 'gts/sampled_gts_bbox_area.json'
    output_directory = 'gts_pascalvoc_format'
    bbox_type = BBoxType.GROUND_TRUTH
    
    coco_to_pascalvoc(coco_annotations_file, output_directory, bbox_type)

    coco_annotations_file = 'dets/sampled_bbox_results.json'
    output_directory = 'dets_pascalvoc_format'
    bbox_type = BBoxType.DETECTION
    
    coco_to_pascalvoc(coco_annotations_file, output_directory, bbox_type)
