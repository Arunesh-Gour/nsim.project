from browser import document, window, timer

from .datamanager import DataManager

import WebApplication as App

jquery = window.jQuery

class Debug:
   retries = 0
   retryTimer = None
   
   updateinterval_data = 300 # ms
   updateinterval_display = 200 # ms
   
   updateIntervalLoop = None
   
   dataFetches = 0
   dataFetch_LayerInterval = 10
   dataFetchIntervalLoop = None
   
   class Flags:
      FUNCTION_NONE   = 1
      FUNCTION_TOGGLE = 2
      FUNCTION_OFF    = 4
      FUNCTION_ON     = 8
   
   functionality_index_active = 1
   functionality_mappings     = {
      0 : [
             1, # primary   : Flags.FUNCTION_NONE
             2, # secondary : Flags.FUNCTION_TOGGLE
          ],
      1 : [
             2, # primary   : Flags.FUNCTION_TOGGLE
             2, # secondary : Flags.FUNCTION_TOGGLE
             # dblclick.BUG: 1, # secondary : Flags.FUNCTION_NONE
          ],
      2 : [
             4, # primary   : Flags.FUNCTION_OFF
             8, # secondary : Flags.FUNCTION_ON
          ],
      3 : [
             8, # primary   : Flags.FUNCTION_ON
             4, # secondary : Flags.FUNCTION_OFF
          ],
   }
   
   cardStripIdentifier = None
   cardMetaItemIdentifier = None
   
   noSocketMessage = (
      'No sockets found !'
      + '<BR /><BR />Create some socket(s) first, to debug (and visualize).'
   )
   debugRetrieveErrorMessage = (
      'Error retrieving debug information.'
      + '<BR /><BR />Please check your internet connection.'
   )
   
   def entry (event=None):
      layout_cardstrip = App.webInterface.TemplateManager.getTemplate(
         'layout.content.card.strip',
      )
      layout_carditem = App.webInterface.TemplateManager.getTemplate(
         'layout.content.card.item',
      )
      
      content_header = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.header',
      )
      content_footer = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.footer',
      )
      content_footer_item_meta = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.footer.item.meta',
      )
      content_body_layer = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.body.slab.layer',
      )
      content_body_queues = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.body.slab.queues',
      )
      
      if (None in (
            layout_cardstrip, layout_carditem,
            content_header, content_footer,
            content_footer_item_meta,
            content_body_layer, content_body_queues,
         )):
         return False
      
      data = DataManager.state_socket_retrieve(
         index = 0,
         queue = False,
      )
      
      if (not (
         data
         or DataManager.state_sockets
      )):
         return False
      
      if (DataManager.state_sockets):
         Debug.showconfiguration()
      else:
         jquery(
            App.webPages.PageStructure.contentBlockIdentifier
         ).html(Debug.noSocketMessage)
      
      return True
   
   def exit (event=None):
      try:
         timer.clear_timeout(Debug.retryTimer)
         Debug.retryTimer = None
      except:
         Debug.retryTimer = None
      
      try:
         timer.clear_interval(Debug.updateIntervalLoop)
         Debug.updateIntervalLoop = None
      except:
         Debug.updateIntervalLoop = None
      
      try:
         timer.clear_interval(Debug.dataFetchIntervalLoop)
         Debug.dataFetchIntervalLoop = None
      except:
         Debug.dataFetchIntervalLoop = None
      
      DataManager.index_sockets_visible.clear()
      
      return True
   
   def showconfiguration (event=None):
      layout_cardstrip = App.webInterface.TemplateManager.getTemplate(
         'layout.content.card.strip',
      )
      layout_carditem = App.webInterface.TemplateManager.getTemplate(
         'layout.content.card.item',
      )
      
      content_header = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.header',
      )
      content_footer = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.footer',
      )
      content_footer_item_meta = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.footer.item.meta',
      )
      content_body_layer = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.body.slab.layer',
      )
      content_body_queues = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.body.slab.queues',
      )
      
      try:
         timer.clear_timeout(Debug.retryTimer)
         Debug.retryTimer = None
      except:
         Debug.retryTimer = None
      
      if (None in (
            layout_cardstrip, layout_carditem,
            content_header, content_footer,
            content_footer_item_meta,
            content_body_layer, content_body_queues,
         )):
         if (Debug.retries < App.Configuration.failureMaxRetries):
            Debug.retries += 1
            
            Debug.retryTimer = timer.set_timeout(
               Debug.showconfiguration,
               App.Configuration.failureRefreshInterval,
            )
            
            return None
         else:
            Debug.retries = 0
            jquery(
               App.webPages.PageStructure.contentBlockIdentifier
            ).html(Debug.debugRetrieveErrorMessage)
            
            Debug.showConnectionError(Debug.showconfiguration)
            return None
         
         return None
      else:
         pass
      
      data = DataManager.state_socket_retrieve(
         index = 0,
         queue = False,
      )
      
      if (not data):
         if (data is None):
            if (Debug.retries < App.Configuration.failureMaxRetries):
               Debug.retries += 1
               
               Debug.retryTimer = timer.set_timeout(
                  Debug.showconfiguration,
                  App.Configuration.failureRefreshInterval,
               )
               
               return None
            else:
               Debug.retries = 0
               jquery(
                  App.webPages.PageStructure.contentBlockIdentifier
               ).html(DataManager.dataRetrieveErrorMessage)
               
               Debug.showConnectionError(Debug.showconfiguration)
               return None
         else:
            Debug.retries = 0
            jquery(
               App.webPages.PageStructure.contentBlockIdentifier
            ).html(DataManager.dataRetrieveErrorMessage)
            return False
      else:
         Debug.retries = 0
      
      if (not DataManager.state_sockets):
         jquery(
            App.webPages.PageStructure.contentBlockIdentifier
         ).html(Debug.noSocketMessage)
         
         return None
      
      Debug.cardStripIdentifier = (
         '.content-card-strip.debug-card-strip'
      )
      
      Debug.cardMetaItemIdentifier = (
         Debug.cardStripIdentifier
         + ' .debug-card-meta-item.debug-card-meta-item-index-0'
      )
      
      carditem_meta_content = App.webInterface.TemplateManager.render(
         layout_carditem,
         itemaddonclasses='{0}'.format(
            'debug-card-meta-item debug-card-meta-item-index-0',
         ),
         
         headeraddonclasses='',
         headerbody=(
            'INFO | META CONTROL'
         ),
         
         bodyaddonclasses='',
         mainbody=(
              'click.single: perform function.primary'
            + '<BR /><BR />'
            + 'click.double: perform function.secondary'
            + '<BR /><BR />'
            + 'meta.click.single: cards.all (perform function.primary)'
            + '<BR /><BR />'
            + 'meta.click.double: alter functions (primary, secondary)'
         ),
         
         footeraddonclasses='',
         footerbody=App.webInterface.TemplateManager.render(
            content_footer_item_meta,
            primaryaddonclasses='',
            primarybody=Debug.resolve_meta_info_str(secondary=False),
            
            secondaryaddonclasses='',
            secondarybody=Debug.resolve_meta_info_str(secondary=True),
         ),
      )
      
      jquery(
         App.webPages.PageStructure.contentBlockIdentifier
      ).html(
         App.webInterface.TemplateManager.render(
            layout_cardstrip,
            columnshortlimit=1,
            columnlimit=3,
            addonclasses='debug-card-strip',
            content=carditem_meta_content, # load with card meta item in place
         )
      )
      
      jquery(
         Debug.cardMetaItemIdentifier
      ).on(
         'click',
         (lambda event=None, *args, alternate=False, index=int(
               '0'
            ), **kwargs: (
            Debug.card_debug_functionality_alter(
               event=event,
               alternate=alternate,
               index=index,
            )
         )),
      )
      jquery(
         Debug.cardMetaItemIdentifier
      ).on(
         'dblclick',
         (lambda event=None, *args, alternate=True, index=int(
            '0'
         ), **kwargs: (
            Debug.card_debug_functionality_alter(
               event=event,
               alternate=alternate,
               index=index,
            )
         )),
      )
      
      DataManager.index_sockets_visible.clear()
      
      # R-Click = (btn.onmousedown -> [ event.which == 3 ]) | btn.oncontextmenu
      
      # complementaries: (primary -> secondary) | (click -> dblclick)
      # on indie card::
      # [0] None -> Toggle
      # [1] Toggle -> Toggle (originally None, but changed due to dblclick bug)
      # [2] On -> Off
      # [3] Off -> On
      # on 0 card::
      # click = function(activeindex[0|1|2|3])
      # dblclick: activeindex = ((activeindex + 1) % 4)
      
      for socket_index in DataManager.state_sockets.keys():
         Debug._insert_socket_card(index=socket_index)
      
      Debug.updateIntervalLoop = timer.set_interval(
         Debug._update_socket_cards,
         Debug.updateinterval_display,
      )
      Debug.dataFetchIntervalLoop = timer.set_interval(
         Debug._data_fetch_socket_cards,
         Debug.updateinterval_data,
      )
      
      return True
   
   def card_debug_functionality_alter (
      event     = None,
      alternate = False,
      index     = 0,
   ):
      if (event is not None):
         event.preventDefault()
      
      try:
         index = int(index)
      except:
         index = 0
      
      if (
             (index)
         and (index not in DataManager.state_sockets.keys())
      ):
         return None
      
      if (
             (not index)
         and (alternate)
      ):
         Debug.functionality_index_active = (
              (Debug.functionality_index_active + 1)
            % (len(Debug.functionality_mappings.keys()))
         )
         
         return None
      
      functionality = Debug.functionality_mappings.get(
         Debug.functionality_index_active,
      )
      
      if (functionality is None):
         return None
      
      functionality = functionality[(
         0
         if (not alternate)
         else
         1
      )]
      
      if (functionality & Debug.Flags.FUNCTION_NONE):
         return None
      elif (functionality & Debug.Flags.FUNCTION_TOGGLE):
         activate = (
            None
            if (not index)
            else (
               False
               if (DataManager.state_sockets.get(index).get('state'))
               else
               True
            )
         )
         
         DataManager.state_socket_alter(
            index    = index,
            activate = activate,
         )
      elif (functionality & Debug.Flags.FUNCTION_OFF):
         DataManager.state_socket_alter(
            index    = index,
            activate = False,
         )
      elif (functionality & Debug.Flags.FUNCTION_ON):
         DataManager.state_socket_alter(
            index    = index,
            activate = True,
         )
      else:
         return None
      
      return None
   
   def _insert_socket_card (
      event = None,
      index = 0,
   ):
      if (
            (index not in DataManager.state_sockets.keys())
         or (index in DataManager.index_sockets_visible)
      ):
         return None
      
      layout_carditem = App.webInterface.TemplateManager.getTemplate(
         'layout.content.card.item',
      )
      
      content_header = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.header',
      )
      content_footer = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.footer',
      )
      content_body_layer = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.body.slab.layer',
      )
      content_body_queues = App.webInterface.TemplateManager.getTemplate(
         'content.debug.card.body.slab.queues',
      )
      
      state_socket = DataManager.state_sockets.get(index)
      
      if (None in (
            layout_carditem,
            content_header, content_footer,
            content_body_layer, content_body_queues,
            state_socket,
      )):
         return None
      
      
      if (state_socket.get('layers') is None):
         '''
         DataManager.state_socket_retrieve(
            index = index,
            queue = False,
         )
         '''
         return None
      
      carditem_mainbody = list()
      
      for layer in (state_socket.get('layers') or []):
         carditem_mainbody.extend([
            App.webInterface.TemplateManager.render(
               content_body_layer,
               addonclasses='',
               layerindex='{0}'.format(layer[0]),
               layername='{0}'.format(layer[1]),
            ),
            App.webInterface.TemplateManager.render(
               content_body_queues,
               slabaddonclasses='',
               queueindex='{0}'.format(layer[0]),
            ),
         ])
      
      try:
         carditem_mainbody.pop()
      except:
         pass
      
      carditem_mainbody = ''.join(carditem_mainbody)
      
      jquery(
         Debug.cardStripIdentifier
      ).append(
         App.webInterface.TemplateManager.render(
            layout_carditem,
            itemaddonclasses='{0}{1}'.format(
               'debug-card-item debug-card-item-index-{0}'.format(
                  state_socket.get('index'),
               ),
               (
                  ' debug-default-index'
                  if (state_socket.get('index') == DataManager.default_index)
                  else
                  ''
               ),
            ),
            
            headeraddonclasses='',
            headerbody=App.webInterface.TemplateManager.render(
               content_header,
               addonclasses=(
                  'debug-index-active'
                  if (state_socket.get('state'))
                  else
                  ''
               ),
               indexbody='{0:02}'.format(
                  state_socket.get('index'),
               ),
            ),
            
            bodyaddonclasses='',
            mainbody=carditem_mainbody,
            
            footeraddonclasses='',
            footerbody=App.webInterface.TemplateManager.render(
               content_footer,
               modeaddonclasses='',
               modebody=(
                  state_socket.get('mode')
                  or 'mode.unknown'
               ),
               
               stateaddonclasses='',
               statebody=DataManager.resolve_status_str(
                  status=(state_socket.get('status') or 0),
               ),
            ),
         )
      )
      
      DataManager.index_sockets_visible.append(state_socket.get('index'))
      
      jquery((
         Debug.cardStripIdentifier
         + ' .debug-card-item.debug-card-item-index-{0}'.format(
            state_socket.get('index'),
         )
      )).on(
         'click',
         (lambda event=None, *args, alternate=False, index=(
               int('{0}'.format(state_socket.get('index')))
            ), **kwargs: (
               Debug.card_debug_functionality_alter(
                  event=event,
                  alternate=alternate,
                  index=index,
               )
         )),
      )
      jquery((
         Debug.cardStripIdentifier
         + ' .debug-card-item.debug-card-item-index-{0}'.format(
            state_socket.get('index'),
         )
      )).on(
         'dblclick',
         (lambda event=None, *args, alternate=True, index=(
               int('{0}'.format(state_socket.get('index')))
            ), **kwargs: (
               Debug.card_debug_functionality_alter(
                  event=event,
                  alternate=alternate,
                  index=index,
               )
         )),
      )
      
      return None
   
   def _update_socket_cards (event=None):
      if (not DataManager.state_sockets):
         return None
      
      for index in list(
           set(DataManager.state_sockets.keys())
         - set(DataManager.index_sockets_visible)
      ):
         Debug._insert_socket_card(index=index)
      
      # Meta Info Card : UPDATE
      jquery((
         Debug.cardMetaItemIdentifier
         + ' .debug-meta-function-primary'
      )).text(
         '{0}'.format(
            Debug.resolve_meta_info_str(secondary=False),
         )
      )
      jquery((
         Debug.cardMetaItemIdentifier
         + ' .debug-meta-function-secondary'
      )).text(
         '{0}'.format(
            Debug.resolve_meta_info_str(secondary=True),
         )
      )
      
      # Remove
      # debug-default-index
      jquery((
         Debug.cardStripIdentifier
         + ' .debug-card-item.debug-default-index'
      )).removeClass(
         'debug-default-index'
      )
      
      # debug-index-active
      jquery((
         Debug.cardStripIdentifier
         + ' .debug-card-item'
         + ' .debug-index.debug-index-active'
      )).removeClass(
         'debug-index-active'
      )
      
      # debug-queue-slot-active
      jquery((
         Debug.cardStripIdentifier
         + ' .debug-card-item'
         + ' .debug-queues-slab'
         + ' .debug-queue-slot.debug-queue-slot-active'
      )).removeClass(
         'debug-queue-slot-active'
      )
      
      # Update
      
      for index in DataManager.index_sockets_visible:
         state_socket = DataManager.state_sockets.get(index)
         
         if (not state_socket):
            continue
         
         # debug-index text
         jquery((
            Debug.cardStripIdentifier
            + ' .debug-card-item.debug-card-item-index-{0}'.format(
                  state_socket.get('index'),
               )
            + ' .debug-index'
         )).text(
            '{0:02}'.format(
               state_socket.get('index'),
            )
         )
         
         # debug-mode text
         jquery((
            Debug.cardStripIdentifier
            + ' .debug-card-item.debug-card-item-index-{0}'.format(
                  state_socket.get('index'),
               )
            + ' .debug-mode'
         )).text(
            '{0}'.format((
               state_socket.get('mode')
               or 'mode.unknown'
            ))
         )
         
         # debug-state text
         jquery((
            Debug.cardStripIdentifier
            + ' .debug-card-item.debug-card-item-index-{0}'.format(
                  state_socket.get('index'),
               )
            + ' .debug-state'
         )).text(
            '{0}'.format(
               DataManager.resolve_status_str(
                  status=(state_socket.get('status') or 0),
               ),
            )
         )
         
         if (state_socket.get('index') == DataManager.default_index):
            # debug-default-index
            jquery((
               Debug.cardStripIdentifier
               + ' .debug-card-item.debug-card-item-index-{0}'.format(
                     state_socket.get('index'),
                  )
            )).addClass(
               'debug-default-index'
            )
         
         if (state_socket.get('state')):
            # debug-index-active
            jquery((
               Debug.cardStripIdentifier
               + ' .debug-card-item.debug-card-item-index-{0}'.format(
                     state_socket.get('index'),
                  )
               + ' .debug-index'
            )).addClass(
               'debug-index-active'
            )
         
         if (state_socket.get('queues') is not None):
            # debug-queue-slot-active
            for queue_index, queue_content in enumerate(
               state_socket.get('queues')
            ):
               length_queue_row_1 = (int(queue_content[0]) or 0)
               length_queue_row_2 = (int(queue_content[1]) or 0)
               
               if (length_queue_row_1 < 1):
                  length_queue_row_1 = 0
               
               if (length_queue_row_1 > 7):
                  length_queue_row_1 = 8
               
               if (length_queue_row_2 < 1):
                  length_queue_row_2 = 0
               
               if (length_queue_row_2 > 7):
                  length_queue_row_2 = 8
               
               # row 1
               for slot_index in range(length_queue_row_1):
                  jquery((
                     Debug.cardStripIdentifier
                     + ' .debug-card-item.debug-card-item-index-{0}'.format(
                           state_socket.get('index'),
                        )
                     + ' .debug-queues-slab'
                     + '.debug-queues-slab-index-{0}'.format(
                           (queue_index + 1),
                        )
                     + ' .debug-queue-row.debug-queue-row-1'
                     + ' .debug-queue-slot.debug-queue-slot-{0}'.format(
                           (slot_index + 1),
                        )
                  )).addClass(
                     'debug-queue-slot-active'
                  )
               
               # row 2
               for slot_index in range(length_queue_row_2):
                  jquery((
                     Debug.cardStripIdentifier
                     + ' .debug-card-item.debug-card-item-index-{0}'.format(
                           state_socket.get('index'),
                        )
                     + ' .debug-queues-slab'
                     + '.debug-queues-slab-index-{0}'.format(
                           (queue_index + 1),
                        )
                     + ' .debug-queue-row.debug-queue-row-2'
                     + ' .debug-queue-slot.debug-queue-slot-{0}'.format(
                           (slot_index + 1),
                        )
                  )).addClass(
                     'debug-queue-slot-active'
                  )
      
      return None
   
   def _data_fetch_socket_cards (event=None):
      Debug.dataFetches += 1
      
      if (Debug.dataFetches >= Debug.dataFetch_LayerInterval):
         Debug.dataFetches = 0
      
      if (not Debug.dataFetches):
         DataManager.state_socket_retrieve(
            index = 0,
            queue = False,
         )
      else:
         DataManager.state_socket_retrieve(
            index = 0,
            queue = True,
         )
      
      return None
   
   def resolve_meta_info_str (
      event     = None,
      secondary = False,
   ):
      try:
         seconday = bool(secondary)
      except:
         seconday = False
      
      functionality = Debug.functionality_mappings.get(
         Debug.functionality_index_active
      )
      
      if (not functionality):
         return 'invalid configuration'
      
      functionality = functionality[(
         0
         if (not secondary)
         else
         1
      )]
      
      if (functionality & Debug.Flags.FUNCTION_NONE):
         return 'NONE'
      elif (functionality & Debug.Flags.FUNCTION_TOGGLE):
         return 'TOGGLE'
      elif (functionality & Debug.Flags.FUNCTION_OFF):
         return 'OFF'
      elif (functionality & Debug.Flags.FUNCTION_ON):
         return 'ON'
      else:
         return 'invalid configuration'
      
      return 'invalid configuration'
   
   def showConnectionError (reloadFunction=None):
      App.webPages.PageStructure.showConnectionError(
         body=DataManager.dataRetrieveErrorMessage,
         reloadFunction=reloadFunction,
      )
