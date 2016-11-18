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

    return segments


test = parse_xml_2(file)
f = str(test).find('seg_1_in')
x = str(test).find(']', f + 1)
z = str(test)[f:x - 1]

print(test)
print(f)
print(x)
print(z)

