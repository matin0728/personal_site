import os
import webapp2

debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

SITE_CONFIG = {
  'is_debug': False,
  'static_file_version': '1211011629413760'
}