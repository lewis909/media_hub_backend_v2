import threading
import transcode_engine
import config

tcn_1 = threading.Thread(target=transcode_engine.transcoder, args=(config.node_1_path, config.cursor_1, config.dbc1))
tcn_2 = threading.Thread(target=transcode_engine.transcoder, args=(config.node_2_path, config.cursor_2, config.dbc2))
tcn_3 = threading.Thread(target=transcode_engine.transcoder, args=(config.node_3_path, config.cursor_3, config.dbc3))
tcn_4 = threading.Thread(target=transcode_engine.transcoder, args=(config.node_4_path, config.cursor_4, config.dbc4))

tcn_1.start()
tcn_2.start()
tcn_3.start()
tcn_4.start()

tcn_1.join()
tcn_2.join()
tcn_3.join()
tcn_4.join()
