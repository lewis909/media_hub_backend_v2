import xml.etree.cElementTree as ET
from xml.dom import minidom


def create_xml(task_id, mat_id, series_title, season_title, season_number, episode_title,
               episode_number, start_date, end_date, rating, synopsis, vid_file_name, vid_file_size,
               vid_md5_checksum, image_file_name, image_file_size, image_md5_checksum, target_path, profile,
               video_file_naming_convention, image_file_naming_convention, package_naming_convention):

    root = ET.Element('package')
    asset_metadata = ET.SubElement(root, 'asset_metadata')
    video_metadata = ET.SubElement(root, 'video_metadata')
    image_1 = ET.SubElement(root, 'image_1')

    # package/asset_metadata
    ET.SubElement(asset_metadata, 'task_id', ).text = task_id
    ET.SubElement(asset_metadata, 'mat_id', ).text = mat_id
    ET.SubElement(asset_metadata, 'series_title', ).text = series_title
    ET.SubElement(asset_metadata, 'season_title', ).text = season_title
    ET.SubElement(asset_metadata, 'season_number', ).text = season_number
    ET.SubElement(asset_metadata, 'episode_title', ).text = episode_title
    ET.SubElement(asset_metadata, 'episode_number', ).text = episode_number
    ET.SubElement(asset_metadata, 'start_date', ).text = start_date
    ET.SubElement(asset_metadata, 'end_date', ).text = end_date
    ET.SubElement(asset_metadata, 'rating', ).text = rating
    ET.SubElement(asset_metadata, 'synopsis', ).text = synopsis

    # package/video_metadata
    ET.SubElement(video_metadata, 'file_name', ).text = vid_file_name
    ET.SubElement(video_metadata, 'file_size', ).text = vid_file_size
    ET.SubElement(video_metadata, 'md5_checksum', ).text = vid_md5_checksum

    # package/image_1
    ET.SubElement(image_1, 'file_name', ).text = image_file_name
    ET.SubElement(image_1, 'file_size', ).text = image_file_size
    ET.SubElement(image_1, 'md5_checksum', ).text = image_md5_checksum

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open(target_path, "w") as f:
        f.write(xmlstr)
        f.close()
