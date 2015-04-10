import unittest
from StringIO import StringIO
import plsql


ROOT_FOLDER_0 = '''DisplayName=Imported Fixed Users
IsFolder=1
Number=0
Parent=-1
Username=
Database=
ConnectAs=
Edition=
Workspace=
Color=65535
'''

ROOT_FOLDER_3 = '''DisplayName=Imported History
IsFolder=1
Number=3
Parent=-1
Username=
Database=
ConnectAs=
Edition=
Workspace=
Color=255
'''

ROOT_FOLDER_0_CHILD_1 = '''DisplayName=child 1
IsFolder=0
Number=1
Parent=0
Username=foo
Database=mydb
ConnectAs=Normal
Edition=
Workspace=
Password=bar
IdentifiedExt=0
Color=65535
'''

ROOT_FOLDER_0_CHILD_2 = '''DisplayName=child 2
IsFolder=0
Number=2
Parent=0
Username=foo2
Database=mydb2
ConnectAs=Normal
Edition=edition
Workspace=workspace 1
Password=bar2
IdentifiedExt=1
Color=255
'''


class TestReader(unittest.TestCase):
  def _check_root_folder_0(self, item):
    self.assertEqual(item.displayName, 'Imported Fixed Users')
    self.assertEqual(True, item.isFolder)
    self.assertEqual('', item.username)
    self.assertEqual('', item.database)
    self.assertEqual('', item.connectAs)
    self.assertEqual('', item.edition)
    self.assertEqual('', item.workspace)
    self.assertEqual(65535, item.color)

  def _check_root_folder_1(self, item):
    self.assertEqual('Imported History', item.displayName)
    self.assertEqual(True, item.isFolder)
    self.assertEqual('', item.username)
    self.assertEqual('', item.database)
    self.assertEqual('', item.connectAs)
    self.assertEqual('', item.edition)
    self.assertEqual('', item.workspace)
    self.assertEqual(255, item.color)

  def _check_child_2(self, item):
    self.assertEqual('child 1', item.displayName)
    self.assertEqual(False, item.isFolder)
    self.assertEqual('foo', item.username)
    self.assertEqual('mydb', item.database)
    self.assertEqual('Normal', item.connectAs)
    self.assertEqual('', item.edition)
    self.assertEqual('', item.workspace)
    self.assertEqual('bar', item.password)
    self.assertEqual(False, item.identifiedExt)
    self.assertEqual(65535, item.color)

  def test_single_folder(self):
    reader = plsql.Reader(StringIO(ROOT_FOLDER_0))
    root = reader.read()
    
    self.assertEqual(1, len(root.children))

    self._check_root_folder_0(root.children[0])
    self.assertEqual(0, len(root.children[0].children))

  def test_many_root_folders(self):
    reader = plsql.Reader(StringIO(ROOT_FOLDER_0 + ROOT_FOLDER_3))
    root = reader.read()
    
    self.assertEqual(2, len(root.children))

    self._check_root_folder_0(root.children[0])
    self.assertEqual(0, len(root.children[0].children))

    self._check_root_folder_1(root.children[1])
    self.assertEqual(0, len(root.children[1].children))

  def test_tree(self):
    reader = plsql.Reader(StringIO(ROOT_FOLDER_0 + ROOT_FOLDER_3 + ROOT_FOLDER_0_CHILD_1))
    root = reader.read()

    self.assertEqual(2, len(root.children))

    self._check_root_folder_0(root.children[0])
    self.assertEqual(1, len(root.children[0].children))

    self._check_child_2(root.children[0].children[0])
    self.assertEqual(0, len(root.children[0].children[0].children))
    self.assertEqual(root.children[0], root.children[0].children[0].parent)

    self._check_root_folder_1(root.children[1])
    self.assertEqual(0, len(root.children[1].children))


class TestWriter(unittest.TestCase):
  def _build_root_folder_0(self):
    item = plsql.Folder('Imported Fixed Users')
    item.username = ''
    item.database = ''
    item.connectAs = ''
    item.edition = ''
    item.workspace = ''
    item.color = 65535

    return item

  def _build_root_folder_3(self):
    item = plsql.Folder('Imported History')
    item.username = ''
    item.database = ''
    item.connectAs = ''
    item.edition = ''
    item.workspace = ''
    item.color = 255

    return item

  def _build_child_2(self):
    item = plsql.Connection('child 1')
    item.username = 'foo'
    item.database = 'mydb'
    item.connectAs = 'Normal'
    item.edition = ''
    item.workspace = ''
    item.password = 'bar'
    item.identifiedExt = False
    item.color = 65535

    return item

  def _build_child_3(self):
    item = plsql.Connection('child 2')
    item.username = 'foo2'
    item.database = 'mydb2'
    item.connectAs = 'Normal'
    item.edition = 'edition'
    item.workspace = 'workspace 1'
    item.password = 'bar2'
    item.identifiedExt = True
    item.color = 255

    return item

  def setUp(self):
    self.root = plsql.Root()
    self.outFile = StringIO()
    self.writer = plsql.Writer(self.outFile)

  def test_single(self):
    self.root.appendChild(self._build_root_folder_0())

    self.writer.write(self.root)
    text = self.outFile.getvalue()

    self.assertEqual(ROOT_FOLDER_0, text)

  def test_tree(self):
    folder_0 = self._build_root_folder_0()
    folder_0.appendChild(self._build_child_2())
    folder_0.appendChild(self._build_child_3())

    self.root.appendChild(folder_0)
    self.root.appendChild(self._build_root_folder_3())

    self.writer.write(self.root)
    text = self.outFile.getvalue()

    self.assertEqual(ROOT_FOLDER_0 + ROOT_FOLDER_0_CHILD_1 + ROOT_FOLDER_0_CHILD_2 + ROOT_FOLDER_3, text)


if __name__ == '__main__':
  unittest.main()
