from flask import (
   # request,
   render_template,
   # Response,
)

import genericflaskwebapp as app

# Create your views here.

def webapplication (application=None, tab=None, subtab=None):
   application = str(application or '').lower()
   
   if (application not in ('webvisualizerdebugger',)):
      application = 'webvisualizerdebugger'
      capp = 'WebVisualizerDebugger'
   else:
      capp = 'WebVisualizerDebugger'
   
   cuser = ''
   
   module = '{0}{1}'.format(
      capp,
      (''
         if (not cuser)
         else (
            '.{0}'.format(cuser)
         )
      ),
   )
   
   return render_template(
      # request,
      'webapplication/WebApplication.index.html',
      **{
         'url_uapi': (
            app.backend.router.routes.endpoints.get('uapi')
            + '/'
         ),
         'module': module,
         'capp': capp,
         'user': cuser,
         'tabname': str(tab or '').lower(),
         'subtabname': str(subtab or '').lower(),
      },
   )
