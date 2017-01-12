from metadata_profiles import amazon, xbox, itunes, sky, google, virgin

# dictionary of metadata profiles
metadata_profiles = {

    'amazon': amazon.create_xml,
    'itunes': itunes.create_xml,
    'sky': sky.create_xml,
    'google': google.create_xml,
    'virgin': virgin.create_xml,
    'xbox': xbox.create_xml,

}
