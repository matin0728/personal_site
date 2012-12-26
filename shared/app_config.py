import os
import webapp2

debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

SITE_CONFIG = {
  'is_debug': debug,
  'static_file_version': '1212261630625932'
}