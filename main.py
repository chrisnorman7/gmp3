"""The main entry."""

if __name__ == '__main__':
 from default_argparse import parser
 parser.add_argument('--server-host', default = '0.0.0.0', help = 'The host to run the HTTP server on')
 parser.add_argument('--server_port', default = 4673, help = 'The port to run the HTTP server on')
 args = parser.parse_args()
 import logging
 logging.basicConfig(stream = args.log_file, level = args.log_level)
 try:
  import application
  logging.info('Starting %s, version %s.', application.name, application.__version__)
  import db, config, os, os.path
  dir = config.config.storage['media_dir']
  if os.path.isdir(dir):
   application.library_size = sum([os.path.getsize(os.path.join(dir, x)) for x in os.listdir(dir) if os.path.isfile(os.path.join(dir, x))])
  else:
   application.library_size = 0
  logging.info('Library size is %s b (%.2f mb).', application.library_size, application.library_size / (1024 ** 2))
  logging.info('Working out of directory: %s.', config.config_dir)
  db.Base.metadata.create_all()
  from gui.main_frame import MainFrame
  application.frame = MainFrame(None)
  application.frame.Show(True)
  application.frame.Maximize(True)
  from server.base import app
  from threading import Thread
  Thread(target = app.run, args = [args.server_host, args.server_port, args.log_file]).start()
  application.app.MainLoop()
  from twisted.internet import reactor
  reactor.callFromThread(reactor.stop)
  logging.info('Done.')
 except Exception as e:
  logging.exception(e)
