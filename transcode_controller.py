import transcode_engine_postgres
import config

while True:
    transcode_engine_postgres.transcoder(config.node_1_path, config.p_cursor, config.p_con)
