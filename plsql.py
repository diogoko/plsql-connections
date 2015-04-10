class Item(object):
  def __init__(self):
    self.displayName = ''
    self.isFolder = False
    self.number = 0
    self.parent = None
    self.username = ''
    self.database = ''
    self.connectAs = ''
    self.edition = ''
    self.workspace = ''
    self.password = ''
    self.identifiedExt = False
    self.color = 65535

    self.children = []

  def appendChild(self, child):
    child.parent = self
    self.children.append(child)


class Reader(object):
  def __init__(self, inputFile):
    self.inputFile = inputFile
  
  def read(self):
    rootItem = Item()
    numberToItem = {}
    
    lines = [l.rstrip() for l in self.inputFile.readlines() if l.strip()]
    while lines:
      item = self._readItem(lines)
      numberToItem[item.number] = item

      if item.parent == -1:
        rootItem.appendChild(item)
      else:
        numberToItem[item.parent].appendChild(item)

    return rootItem
  
  def _readItem(self, lines):
    item = Item()
    item.displayName = self._readField(lines, 'DisplayName')
    item.isFolder = self._readBoolField(lines, 'IsFolder')
    item.number = self._readIntField(lines, 'Number')
    item.parent = self._readIntField(lines, 'Parent')
    item.username = self._readField(lines, 'Username')
    item.database = self._readField(lines, 'Database')
    item.connectAs = self._readField(lines, 'ConnectAs')
    item.edition = self._readField(lines, 'Edition')
    item.workspace = self._readField(lines, 'Workspace')
    if self._peekField(lines, 'Password'):
      item.password = self._readField(lines, 'Password')
    if self._peekField(lines, 'IdentifiedExt'):
      item.identifiedExt = self._readBoolField(lines, 'IdentifiedExt')
    item.color = self._readIntField(lines, 'Color')
    
    return item
  
  def _readBoolField(self, lines, expectedName):
    return bool(self._readIntField(lines, expectedName))
  
  def _readIntField(self, lines, expectedName):
    return int(self._readField(lines, expectedName))
  
  def _readField(self, lines, expectedName):
    name, value = lines.pop(0).split('=', 1)
    if name != expectedName:
      raise SyntaxError('Expected field {0} but found {1}'.format(expectedName, name))
    return value

  def _peekField(self, lines, expectedName):
    name, value = lines[0].split('=', 1)
    return name == expectedName


class Writer(object):
  def __init__(self, outputFile):
    self.outputFile = outputFile
  
  def write(self, rootItem):
    rootItem.number = -1

    number = 0
    items = list(rootItem.children)
    while items:
      item = items.pop(0)
      item.number = number
      number += 1

      self._writeItem(item)
      items.extend(item.children)

  def _writeItem(self, item):
    FOLDER_TEMPLATE = '''DisplayName={}
IsFolder={}
Number={}
Parent={}
Username={}
Database={}
ConnectAs={}
Edition={}
Workspace={}
Color={}
'''
    CONNECTION_TEMPLATE = '''DisplayName={}
IsFolder={}
Number={}
Parent={}
Username={}
Database={}
ConnectAs={}
Edition={}
Workspace={}
Password={}
IdentifiedExt={}
Color={}
'''

    if item.isFolder:
      encodedItem = FOLDER_TEMPLATE.format(
        item.displayName,
        self._formatBool(item.isFolder),
        item.number,
        self._formatParent(item.parent),
        item.username,
        item.database,
        item.connectAs,
        item.edition,
        item.workspace,
        item.color
      )
    else:
      encodedItem = CONNECTION_TEMPLATE.format(
        item.displayName,
        self._formatBool(item.isFolder),
        item.number,
        self._formatParent(item.parent),
        item.username,
        item.database,
        item.connectAs,
        item.edition,
        item.workspace,
        item.password,
        self._formatBool(item.identifiedExt),
        item.color
      )
    self.outputFile.write(encodedItem)

  def _formatBool(self, value):
    return int(value)

  def _formatParent(self, value):
    if value is None:
      return -1
    else:
      return value.number
