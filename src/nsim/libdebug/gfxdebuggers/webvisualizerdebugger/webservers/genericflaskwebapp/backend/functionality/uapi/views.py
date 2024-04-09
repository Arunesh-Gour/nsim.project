import re
import json

from flask import (
   request,
   # render_template,
   Response,
)

from .uapiManager import UAPIManager

from .apis import APIs

APIs.start()

def uapi (path=None,):
   apicode = None
   
   if (path):
      path = [
         (
            int(ipath)
            if (str(ipath).isdigit())
            else (
               True
               if (str(ipath) in (
                  'True',
                  'true',
               ))
               else (
                  False
                  if (str(ipath) in (
                     'False',
                     'false',
                  ))
                  else (
                     None
                     if (str(ipath) in (
                        'None',
                        'NULL',
                        'Null',
                        'null',
                     ))
                     else
                     str(ipath)
                  )
               )
               # str(ipath)
            )
         )
         for ipath in [
            re.sub('[\ ]+', ' ', apath.strip())
            for apath in re.split('[^a-zA-Z0-9\-\.\ ]+', path)
            if (apath)
         ]
         if (ipath)
      ]
      
      if (len(path) > 0):
         apicode = str(path[0]).strip().replace(' ', '') or None
         path = path[1:]
   else:
      path = []
   
   requestdata = None
   try:
      requestdata = request.json # json.loads(request.json) # request.body
   except:
      requestdata = None
   
   if (requestdata):
      if (not apicode):
         apicode = requestdata.get('apicode')
      
      requestdata = requestdata.get('data')
   else:
      requestdata = dict()
      for key, value in request.args.items():
         requestdata[key] = value
      
      for key, value in request.form.items():
         requestdata[key] = value
      
      if (not apicode):
         apicode = requestdata.get('apicode')
      
      try:
         requestdata.pop('apicode')
      except:
         pass
   
   if (apicode):
      apicode = apicode.replace('-', '.')
   
   requestdata = requestdata or dict()
   
   data = UAPIManager.fetch(request,
      apicode=apicode, data=requestdata, path=path,
   )
   
   return Response (
      json.dumps(data),
      content_type='application/json',
   )
