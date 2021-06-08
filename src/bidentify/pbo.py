import struct
import sys

VERSION_HEADER_LENGTH = 15

class PBOEntry:

  def __init__(self, filename, packing_method, original_size, reserved, timestamp, data_size):
    self.filename = filename
    self.packing_method = packing_method
    self.original_size = original_size
    self.reserved = reserved
    self.timestamp = timestamp
    self.data_size = data_size

  def __repr__(self):
    return "%s" % self.__dict__

  def __str__(self):
    return self.filename

class PBOFile:

  def __init__(self, path):
    self.path = path
    self.headers = {}
    self.file = []

  def readline(self, file):
    line = ''

    while True:
      c = file.read(1)
      print(c)
      #print(type(c))
      if c and c != '\0':
        line += str(c)
      else:
        return line

  def read_headers(self, file):
    self.headers = {}
    while True:
      header = self.readline(file)

      if header and len(header) != 0:
        if (header == "sreV"):
          file.seek(VERSION_HEADER_LENGTH, 1)
        else:
          value = self.readline(file)
          self.headers[header] = value
      else:
        return

  def read_files_table(self, file):
    self.files = []
    while True:
      filename = self.readline(file)
      packing_method = struct.unpack('i', file.read(4))[0]
      original_size = struct.unpack('i', file.read(4))[0]
      reserved = struct.unpack('i', file.read(4))[0]
      timestamp = struct.unpack('i', file.read(4))[0]
      data_size = struct.unpack('i', file.read(4))[0]

      if filename and len(filename) != 0:
        self.files.append(PBOEntry(filename, packing_method, original_size, reserved, timestamp, data_size))
      else:
        offset = file.tell()
        for entry in self.files:
          entry.offset = offset
          offset += entry.data_size
        return

  def load(self):
    with open(self.path, "rb") as file:
      if len(self.readline(file)) == 0:
        self.read_headers(file)
      else:
        file.seek(0)
      self.read_files_table(file)

  def read(self, entry, offset, length):
    with open(self.path, "rb") as file:
      file.seek(entry.offset + offset)
      return file.read(length)

  def __repr__(self):
    return self.path

  def __str__(self):
    return self.path

#def main(path):
#  pbo = PBOFile(path)
#  pbo.load()

#if __name__ == '__main__':
#  main(sys.argv[1])
