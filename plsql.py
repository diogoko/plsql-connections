class Item(object):
	displayName = ''
	isFolder = 0
	number = 0
	parent = -1
	username = ''
	database = ''
	connectAs = ''
	edition = ''
	workspace = ''
	color = 65535
	
	children = []


class Reader(object):
	def __init(self, inputFile):
		self.inputFile = inputFile
	
	def read(self):
		rootItem = Item()
		numberToItem = {}
		
		lines = self.inputFile.readlines()
		while lines:
			item = self._readItem(lines))
			numberToItem[item.number] = item
			
			if item.parent == -1:
				rootItem.children.append(item)
			else:
				numberToItem[item.parent].children.append(item)
		
		return rootItem
	
	def _readItem(self, lines):
		item = Item()
		# TODO


class Writer(object):
	def __init(self, outputFile):
		self.outputFile = outputFile
	
	def write(self, rootItem, _number = 0):
		rootItem.number = _number
		self._writeItem(rootItem)
		_number += 1
		
		for child in rootItem.children:
			self.write(child, _number)
			_number += 1
	
	def _writeItem(self, item):
		ITEM_TEMPLATE = '''DisplayName={}
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
		encodedItem = ITEM_TEMPLATE.format(
			item.displayName,
			item.isFolder,
			item.number,
			item.parent,
			item.username,
			item.database,
			item.connectAs,
			item.edition,
			item.workspace,
			item.color
		)
		self.outputFile.write(encodedItem)
