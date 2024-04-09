import os
from pathlib import Path

from flask import (
   Flask,
   request,
)

from urllib.request import urlopen

import genericflaskwebapp as app

class Executor:
   instances = 0
   
   def __init__ (
      self,
      host=None, port=None,
      database=None, dbpath=None,
      templatespath=None,
      staticpath=None,
      model=None, router=None,
      debug=None,
   ):
      self.ready = False
      
      self.host = (
         str(host)
         if (host)
         else
         '0.0.0.0'
      )
      
      self.port = (
         int(port)
         if (port)
         else
         5000
      )
      
      self.debug = (
         bool(debug)
         if (debug is not None)
         else
         True
      )
      
      database = (
         database
         if (database is not None)
         else
         app.database.api.DataBase.SQLite3
      )
      
      dbpath = os.path.abspath(
         dbpath
         if (dbpath)
         else
         (
            Path(__file__).parent.parent.parent / 'storage' / 'database' / (
               'sqlite3database.sqlite3'
            )
         ).resolve()
      )
      
      templatespath = os.path.abspath(
         templatespath
         if (templatespath)
         else
         (
            Path(__file__).parent.parent.parent / 'frontend' / 'templates'
         ).resolve()
      )
      staticpath = os.path.abspath(
         staticpath
         if (staticpath)
         else
         (
            Path(__file__).parent.parent.parent / 'frontend' / 'static'
         ).resolve()
      )
      
      model = (
         model
         if (model is not None)
         else
         app.database.api.Model.ModelsV1
      )
      
      router = (
         router
         if (router is not None)
         else
         app.backend.api.Router.RouterV1
      )
      
      # Database not required !
      '''
      if (not app.database.api.database_start(database, dbpath)):
         raise Exception(
            'operations.webserver.executor:Executor.__init__:: '
            + 'Error starting database !'
         )
      
      if (not app.database.api.model_start(model)):
         raise Exception(
            'operations.webserver.executor:Executor.__init__:: '
            + 'Error loading models !'
         )
      '''
      
      if (not app.backend.api.router_start(router)):
         raise Exception(
            'operations.webserver.executor:Executor.__init__:: '
            + 'Error starting backend router !'
         )
      
      self.instance = Executor.instances + 1
      Executor.instances += 1
      
      self.webapp = Flask(
         __name__,
         template_folder=templatespath,
         static_folder=staticpath,
      )
      self.webapp.config.from_mapping(
         SECRET_KEY=app.backend.security.basickeygen.key_general_generate(
            length=32,
         ),
      )
      
      app.backend.router.routes.route_webapp(self.webapp)
      
      self._shutdown_url = (
         app.backend.security.basickeygen.key_general_generate(
            length=16,
      ))
      
      @self.webapp.route('/{0}'.format(self._shutdown_url), methods=['GET',])
      def close (*args, **kwargs):
         shutdown_function = request.environ.get('werkzeug.server.shutdown')
         
         if (shutdown_function is None):
            raise RuntimeError('genericflaskwebapp.close')
         
         shutdown_function()
         
         return 'Shutdown'
      
      self._close = close
      
      self.ready = True
   
   def start (self):
      if (not self.ready):
         return None
      
      result = None
      
      try:
         result = self.webapp.run(
            host=self.host,
            port=self.port,
            debug=self.debug,
         )
      except:
         raise
      finally:
         app.database.api.close()
      
      return result
   
   def stop (self):
      try:
         urlopen(
            'http://127.0.0.1:{0}/{1}'.format(
               # self.host,
               self.port,
               self._shutdown_url,
         ))
      except:
         pass
      
      return None
