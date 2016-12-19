import threading
import transcode_engine
import config



tcn_1 = threading.Thread(target=transcode_engine.transcoder, args=(config.node_1_path, config.cursor_1, config.dbc1))

tcn_1.start()
tcn_1.join()
