from browser import document, window, timer

import WebApplication as App

jquery = window.jQuery

class Developers:
   def entry (event=None):
      jquery(
         App.webPages.PageStructure.contentBlockIdentifier
      ).html(
           '<h3>&lt; developer & designer /&gt;</h3><BR />'
         + '<h4>Arunesh Gour</h4>'
         + '<BR /><BR /><BR />'
         + '<h3>[ software ]</h3><BR />'
         + '<h5>Edition: Concept Prototype</h5><BR />'
         + '<h5>License: MIT</h5><BR />'
         + '<h5>Source : Free &amp; Open Source [ Github ]</h5><BR /><BR />'
         + '<h5>Get it on github @ <a href="'
         + 'https://github.com/Arunesh-Gour/nsim.project/'
         + '">github.com/Arunesh-Gour/nsim.project/'
         + '</a> !</h5><BR />'
      )
      return True
   
   def exit (event=None):
      return True
