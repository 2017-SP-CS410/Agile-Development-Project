TARGET = sip.exe
OFILES = main.obj transform.obj gencode.obj extracts.obj export.obj type_hints.obj heap.obj parser.obj lexer.obj
HFILES = sip.h parser.h

CC = bcc32
CXX = bcc32
LINK = ilink32
CPPFLAGS = -DNDEBUG -DUNICODE -I.
CFLAGS = -tWR -tWM -tWC -O2 -w -w-hid
CXXFLAGS = -tWR -tWM -x- -RT- -tWC -O2 -w -w-hid
LFLAGS = -c -x -Gn -ap -Tpe c0x32.obj
LIBS = -L\lib import32.lib cw32mti.lib
.SUFFIXES: .c .cpp .cc .cxx .C


.cpp.obj:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o$@ $<

.cc.obj:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o$@ $<

.cxx.obj:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o$@ $<

.C.obj:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o$@ $<

.c.obj:
	$(CC) -c $(CFLAGS) $(CPPFLAGS) -o$@ $<

all: $(TARGET)

$(OFILES): $(HFILES)

$(TARGET): $(OFILES)
	$(LINK) @&&|
	$(LFLAGS) $(OFILES) ,$(TARGET),,$(LIBS),,
|

install: $(TARGET)
	@if not exist "C:\Program Files (x86)\Python36-32" mkdir "C:\Program Files (x86)\Python36-32"
	copy /y $(TARGET) "C:\Program Files (x86)\Python36-32\$(TARGET)"

clean:
	-del $(TARGET)
	-del main.obj
	-del transform.obj
	-del gencode.obj
	-del extracts.obj
	-del export.obj
	-del type_hints.obj
	-del heap.obj
	-del parser.obj
	-del lexer.obj
