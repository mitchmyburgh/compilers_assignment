
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = 'B5F7ECDA580C27B43E82306D4727905F'
    
_lr_action_items = {'$end':([2,3,5,6,7,8,10,11,17,18,19,20,21,],[0,-1,-2,-6,-12,-3,-11,-9,-8,-7,-4,-5,-10,]),'$':([6,7,8,10,11,16,17,18,19,20,21,],[-6,-12,15,-11,-9,15,-8,-7,-4,-5,-10,]),'(':([4,9,12,13,14,15,],[9,9,9,9,9,9,]),'@':([6,7,8,10,11,16,17,18,19,20,21,],[-6,-12,14,-11,-9,14,-8,-7,-4,-5,-10,]),'FLOAT_LITERAL':([4,9,12,13,14,15,],[10,10,10,10,10,10,]),'ID':([0,3,4,5,6,7,8,9,10,11,12,13,14,15,17,18,19,20,21,],[1,1,7,1,-6,-12,-3,7,-11,-9,7,7,7,7,-8,-7,-4,-5,-10,]),'=':([1,],[4,]),'&':([6,7,10,11,17,18,21,],[12,-12,-11,-9,-8,-7,-10,]),'#':([6,7,10,11,17,18,21,],[13,-12,-11,-9,-8,-7,-10,]),')':([6,7,10,11,16,17,18,19,20,21,],[-6,-12,-11,-9,21,-8,-7,-4,-5,-10,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'factor':([4,9,12,13,14,15,],[11,11,17,18,11,11,]),'program':([0,],[2,]),'expression':([4,9,14,15,],[8,16,19,20,]),'term':([4,9,14,15,],[6,6,6,6,]),'statement':([0,3,5,],[3,5,5,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement','program',1,'p_program','parse_ula.py',21),
  ('statement -> statement statement','statement',2,'p_statement_clos','parse_ula.py',26),
  ('statement -> ID = expression','statement',3,'p_statement_assign','parse_ula.py',31),
  ('expression -> expression @ expression','expression',3,'p_expression_sum','parse_ula.py',36),
  ('expression -> expression $ expression','expression',3,'p_expression_sub','parse_ula.py',41),
  ('expression -> term','expression',1,'p_expression_term','parse_ula.py',46),
  ('term -> term # factor','term',3,'p_term_product','parse_ula.py',51),
  ('term -> term & factor','term',3,'p_term_div','parse_ula.py',57),
  ('term -> factor','term',1,'p_term_factor','parse_ula.py',62),
  ('factor -> ( expression )','factor',3,'p_factor_pare','parse_ula.py',67),
  ('factor -> FLOAT_LITERAL','factor',1,'p_factor_float','parse_ula.py',72),
  ('factor -> ID','factor',1,'p_factor_ID','parse_ula.py',77),
]
