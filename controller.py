import transcode_engine
import config

# TODO - Create job log.
while True:
    transcode_engine.transcoder(config.node_1_path, config.cursor_1, config.dbc1)
