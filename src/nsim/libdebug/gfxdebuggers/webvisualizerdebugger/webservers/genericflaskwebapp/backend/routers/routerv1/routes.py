import genericflaskwebapp as app

class Routes:
   endpoints = {
      'uapi' : '/uapi',
      'uapi.slash' : '/uapi/',
      'uapi.path' : '/uapi/<path:path>',
      'uapi.path.slash' : '/uapi/<path:path>/',
      
      'webapplication' : '/',
      'webapplication.application' : '/<string:application>',
      'webapplication.application.slash' : '/<string:application>/',
      'webapplication.application.tab' : (
         '/<string:application>/<string:tab>'
      ),
      'webapplication.application.tab.slash' : (
         '/<string:application>/<string:tab>/'
      ),
      'webapplication.application.tab.subtab' : (
         '/<string:application>/<string:tab>/<string:subtab>'
      ),
      'webapplication.application.tab.subtab.slash' : (
         '/<string:application>/<string:tab>/<string:subtab>/'
      ),
   }
   
   def route_webapp (webapp):
      # from . import pages
      
      @webapp.route(Routes.endpoints.get('uapi'), methods=['GET', 'POST'])
      def uapi (*args, **kwargs):
         return app.backend.functionality.uapi.views.uapi(*args, **kwargs)
      
      @webapp.route(Routes.endpoints.get('uapi.slash'),
         methods=['GET', 'POST'],
      )
      def uapi_slash (*args, **kwargs):
         return app.backend.functionality.uapi.views.uapi(*args, **kwargs)
      
      @webapp.route(
         Routes.endpoints.get('uapi.path'),
         methods=['GET', 'POST'],
      )
      def uapi_path (*args, **kwargs):
         return app.backend.functionality.uapi.views.uapi(*args, **kwargs)
      
      @webapp.route(
         Routes.endpoints.get('uapi.path.slash'),
         methods=['GET', 'POST'],
      )
      def uapi_path_slash (*args, **kwargs):
         return app.backend.functionality.uapi.views.uapi(*args, **kwargs)
      
      @webapp.route(Routes.endpoints.get('webapplication'))
      def webapplication (*args, **kwargs):
         return app.backend.functionality.webapplication.views.webapplication(
            *args,
            **kwargs,
         )
      
      @webapp.route(Routes.endpoints.get('webapplication.application'))
      def webapplication_application (*args, **kwargs):
         return app.backend.functionality.webapplication.views.webapplication(
            *args,
            **kwargs,
         )
      
      @webapp.route(Routes.endpoints.get('webapplication.application.slash'))
      def webapplication_application_slash (*args, **kwargs):
         return app.backend.functionality.webapplication.views.webapplication(
            *args,
            **kwargs,
         )
      
      @webapp.route(Routes.endpoints.get('webapplication.application.tab'))
      def webapplication_application_tab (*args, **kwargs):
         return app.backend.functionality.webapplication.views.webapplication(
            *args,
            **kwargs,
         )
      
      @webapp.route(
         Routes.endpoints.get('webapplication.application.tab.slash')
      )
      def webapplication_application_tab_slash (*args, **kwargs):
         return app.backend.functionality.webapplication.views.webapplication(
            *args,
            **kwargs,
         )
      
      @webapp.route(
         Routes.endpoints.get('webapplication.application.tab.subtab')
      )
      def webapplication_application_tab_subtab (*args, **kwargs):
         return app.backend.functionality.webapplication.views.webapplication(
            *args,
            **kwargs,
         )
      
      @webapp.route(
         Routes.endpoints.get('webapplication.application.tab.subtab.slash')
      )
      def webapplication_application_tab_subtab_slash (*args, **kwargs):
         return app.backend.functionality.webapplication.views.webapplication(
            *args,
            **kwargs,
         )
