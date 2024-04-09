from browser import document, window, timer

import WebApplication as App

jquery = window.jQuery

class Home:
   retries = 0
   retryTimer = None
   
   offlineMessage = (
        '<h1>!# Welcome to Web Visualizer Debugger (NSIM) #!</h1>'
      + '</BR><BR/>'
      + 'Looks like you\'re offline !'
      + '</BR>'
      + 'Try checking server status !'
   )
   onlineMessage = (
        '<BR />'
      + '<h1> &lt; NSIM: Web Visualizer Debugger /&gt; </h1>'
   )
   connectionErrorMessage = (
        'Error connecting to server.'
      + '<BR /><BR />Please check your internet connection (or server status).'
   )
   
   def entry (event=None):
      jquery(
         App.webPages.PageStructure.contentBlockIdentifier
      ).html(Home.offlineMessage)
      
      try:
         Home.graphics_display()
      except:
         pass
      
      return True
   
   def exit (event=None):
      return True
   
   def graphics_display (event=None):
      layout_graphic_item = App.webInterface.TemplateManager.getTemplate(
         'layout.graphic.item',
      )
      
      try:
         timer.clear_timeout(Home.retryTimer)
         Home.retryTimer = None
      except:
         Home.retryTimer = None
      
      if (None in (
            layout_graphic_item,
         )):
         if (Home.retries < App.Configuration.failureMaxRetries):
            Home.retries += 1
            
            Home.retryTimer = timer.set_timeout(
               Home.graphics_display,
               App.Configuration.failureRefreshInterval,
            )
            
            return None
         else:
            Home.retries = 0
            jquery(
               App.webPages.PageStructure.contentBlockIdentifier
            ).html(Home.offlineMessage)
            
            Home.showConnectionError(Home.graphics_display)
            return None
         
         return None
      else:
         pass
      
      graphics = [
         'icon.dark.dark',
         'icon.dark.transparent',
         'icon.light.light',
         'icon.light.transparent',
         
         'logo.dark.dark',
         'logo.dark.transparent',
         'logo.light.light',
         'logo.light.transparent',
      ]
      
      graphics = ' '.join([
         App.webInterface.TemplateManager.render(
            layout_graphic_item,
            imageurl='{0}Images/{1}.png'.format(
               App.Configuration.staticUrl,
               graphic,
            ),
            alt='{0}'.format(
               graphic,
            ),
            description='{0}'.format(
               graphic,
            ),
         )
         for graphic in graphics
      ])
      
      jquery(
         App.webPages.PageStructure.contentBlockIdentifier
      ).html(
         '{0}{1}'.format(
            Home.onlineMessage,
            (
               '{0}{1}{0}{2}'.format(
                  '<BR/><BR/>',
                  'Icons &amp; Logos:<BR/>',
                  graphics,
               )
               if (graphics)
               else
               ''
            ),
         )
      )
      
      return None
   
   def showConnectionError (reloadFunction=None):
      App.webPages.PageStructure.showConnectionError(
         body=Home.connectionErrorMessage,
         reloadFunction=reloadFunction,
      )
