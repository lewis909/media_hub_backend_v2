import xml.etree.ElementTree as et
file = 'F:\\Transcoder\\processing_temp\\task_00000000112\\conform\\temp\\core_metadata.xml'


def seg_element(xml_root, element_path):
    list_a = []
    for elem in xml_root.iterfind(element_path):
        a = elem.attrib
        for i in a:
            list_a.append([i + ' = ' + a[i]])
        return list_a


def parse_xml(file_input, number_of_segments):
    tree = et.parse(file_input)
    root = tree.getroot()
    path = 'file_info/segment_1'

    return seg_element(root, path)


def parse_xml_2(file_input):
    tree = et.parse(file_input)
    root = tree.getroot()
    segments_no = int(root.find('file_info/number_of_segments').text)
    segments = []

    for i in range(segments_no):
        path = 'file_info/segment_%d' % (i+1)
        segments.append(seg_element(root, path))

    ffmpeg_start_str = 'ffmpeg -i test.mp4 '
    ffmpeg_seg_cmd = 'FLAG-ss in_point -t out_point target_file.mp4 '



    ffmpeg_cmd = ffmpeg_start_str + ffmpeg_seg_cmd * segments_no

    return segments, ffmpeg_cmd


test_1, test_2 = parse_xml_2(file)
f = str(test_1).find('seg_1_in')
x = str(test_1).find(']', f)
duration_values = str(test_1)
print(duration_values)


def find_seg_in_point(dur_string, seg_number):
    seg_start_list = []
    seg_duration_list = []
    while True:
        for i in range(seg_number):
            seg = 'seg_%d_in =' % (i+1)
            seg_1_in_s = str(dur_string).find(seg)
            if seg_1_in_s > 0:
                seg_1_in_e = str(dur_string).find(']', seg_1_in_s)
                seg_1_in = str(dur_string)[seg_1_in_s:seg_1_in_e - 1]
                seg_start_list.append(str(seg_1_in).replace(seg, '-ss'))
        for i in range(seg_number):
            seg = 'seg_%d_dur =' % (i+1)
            seg_1_dur_s = str(dur_string).find(seg)
            if seg_1_dur_s > 0:
                seg_1_dur_e = str(dur_string).find(']', seg_1_dur_s)
                seg_1_dur = str(dur_string)[seg_1_dur_s:seg_1_dur_e - 1]
                seg_duration_list.append(str(seg_1_dur).replace(seg, '-t'))
        break
    print(seg_start_list)
    print(seg_duration_list)
    return seg_start_list, seg_duration_list


find_seg_in_point(duration_values, 4)

# print(test_2)
# print(f)
# print(x)
# print(z.replace('seg_1_in =', '-ss'))


