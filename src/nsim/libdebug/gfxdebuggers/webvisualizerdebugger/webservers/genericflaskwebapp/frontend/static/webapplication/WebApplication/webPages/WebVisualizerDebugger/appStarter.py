import WebApplication as App

class AppStarter:
   def start ():
      App.Configuration.applicationName = 'WebVisualizerDebugger'
      App.Configuration.subApplicationName = None
      # App.Configuration.loggedIn = None
      
      App.Configuration.pageStructureType = 'topbar'
      
      App.webInterface.Activator.tabs = {
         # 'default' : 'default-tabname',
         # 'tabname' : exec_function(event),
         # 'tabname' : [exit_function(event), enter_function(event),],
         # 'tabname' : {
         #    'default' : 'default-subtabname',
         #    'subtabname' : exec_function(event),
         #    'subtabname' : [exit_function(event), enter_function(event),],
         # },
         'default' : 'home',
         'home' : [
            App.webPages.WebVisualizerDebugger.Home.exit,
            App.webPages.WebVisualizerDebugger.Home.entry,
         ],
         'developers' : [
            App.webPages.WebVisualizerDebugger.Developers.exit,
            App.webPages.WebVisualizerDebugger.Developers.entry,
         ],
         'debug' : [
            App.webPages.WebVisualizerDebugger.debug.Debug.exit,
            App.webPages.WebVisualizerDebugger.debug.Debug.entry,
         ],
      }
      App.webInterface.Activator.hiddenTabs = {
         # 'tabname' : None,
         # 'tabname' : {
         #    'subtabname' : None,
         # },
      }
