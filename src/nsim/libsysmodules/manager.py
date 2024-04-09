import sys

class Manager:
   """Manager for system modules.
   
   Responsible for overriding or restoration of system modules so as to better
   integrate with existing applications.
   
   Attributes
   ----------
   modules : dict
      Collection of original modules (with object), which are overridden.
   _overridden : bool
      System modules' state - overridden by manager or not.
   
   Methods
   -------
   is_overridden ()
      Returns system modules' overridden state.
   module_original ()
      Fetches original module, irrespective of overridden state.
   override ()
      Overrides system modules with custom ones.
   restore ()
      Restores overridden modules with originals.
   """
   
   modules = dict()
   _overridden = False
   
   def is_overridden ():
      """Returns system modules' overridden state.
      
      Checks the _overridden flag for state and returns same.
      
      Returns
      -------
      bool
         Returns whether system modules are overridden by manager or not.
      """
      
      return (Manager._overridden)
   
   def module_original (module):
      """Fetches original module, irrespective of overridden state.
      
      Searces for module in modules attribute, failing which it tries
      importing them and returns the result.
      
      Parameters
      ----------
      module : str
         Module to be fetched.
      
      Raises
      ------
      ModuleNotFoundError
         Error is raised if module is neither overridden nor exists.
      
      Returns
      -------
      NoneType
         Returns None if invalid parameters.
      object
         Returns module object on success.
      """
      
      if (not module):
         return None
      
      module_o = None
      
      if (Manager._overridden):
         module_o = Manager.modules.get(module, None)
      
      if (module_o is None):
         module_o = __import__(module)
      
      return module_o
   
   def override ():
      """Overrides system modules with custom ones.
      
      Overrides system modules with custom ones located in modules package
      in same directory.
      
      Returns
      -------
      bool
         Returns True on success.
      """
      
      if (Manager._overridden):
         return True
      
      import socket
      
      Manager.modules['socket'] = sys.modules['socket']
      
      from .modules import o_socket
      
      sys.modules['socket'] = o_socket
      
      Manager._overridden = True
      
      return True
   
   def restore ():
      """Restores overridden modules with originals.
      
      Restores overriden modules by restoring from modules attribute, which
      was used to store original ones during override.
      
      Returns
      -------
      bool
         Returns True on success.
      """
      
      if (not Manager._overridden):
         return True
      
      for module_name, module in Manager.modules.items():
         sys.modules[module_name] = module
      
      Manager._overridden = False
      
      return True
