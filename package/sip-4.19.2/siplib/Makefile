TARGET = sip.pyd
OFILES = siplib.obj apiversions.obj descriptors.obj qtlib.obj threads.obj objmap.obj voidptr.obj array.obj bool.obj
HFILES = sip.h sipint.h array.h 

CC = bcc32
CXX = bcc32
LINK = ilink32
CPPFLAGS = -DNDEBUG -DUNICODE -I. -I"C:\Program Files (x86)\Python36-32\include"
CFLAGS = -tWR -tWM -tWC -O2 -w -w-hid
CXXFLAGS = -tWR -tWM -x- -RT- -tWC -O2 -w -w-hid
LFLAGS = -c -x -Gn -Gi -aa -Tpd c0d32.obj -ap -Tpe c0x32.obj
LIBS = -L\lib -L"C:\Program Files (x86)\Python36-32\libs" import32.lib cw32mti.lib python36.lib
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
	$(LFLAGS) $(OFILES) ,$(TARGET),,$(LIBS),sip
|

install: $(TARGET)
	@if not exist "C:\Program Files (x86)\Python36-32\Lib\site-packages" mkdir "C:\Program Files (x86)\Python36-32\Lib\site-packages"
	copy /y $(TARGET) "C:\Program Files (x86)\Python36-32\Lib\site-packages\$(TARGET)"
	@if not exist "C:\Program Files (x86)\Python36-32\include" mkdir "C:\Program Files (x86)\Python36-32\include"
	copy /y C:\Users\Anthony\Desktop\Agile-Development-Project\package\sip-4.19.2\siplib\sip.h "C:\Program Files (x86)\Python36-32\include\sip.h"
	@if not exist "C:\Program Files (x86)\Python36-32\Lib\site-packages" mkdir "C:\Program Files (x86)\Python36-32\Lib\site-packages"
	copy /y C:\Users\Anthony\Desktop\Agile-Development-Project\package\sip-4.19.2\sip.pyi "C:\Program Files (x86)\Python36-32\Lib\site-packages\sip.pyi"

clean:
	-del $(TARGET)
	-del siplib.obj
	-del apiversions.obj
	-del descriptors.obj
	-del qtlib.obj
	-del threads.obj
	-del objmap.obj
	-del voidptr.obj
	-del array.obj
	-del bool.obj
