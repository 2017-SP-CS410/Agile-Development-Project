
all:
	cd sipgen
	$(MAKE)
	@cd ..
	cd siplib
	$(MAKE)
	@cd ..

install:
	cd sipgen
	$(MAKE) install
	@cd ..
	cd siplib
	$(MAKE) install
	@cd ..
	@if not exist "C:\Program Files (x86)\Python36-32\Lib\site-packages" mkdir "C:\Program Files (x86)\Python36-32\Lib\site-packages"
	copy /y sipconfig.py "C:\Program Files (x86)\Python36-32\Lib\site-packages\sipconfig.py"
	copy /y C:\Users\Anthony\Desktop\Agile-Development-Project\package\sip-4.19.2\sipdistutils.py "C:\Program Files (x86)\Python36-32\Lib\site-packages\sipdistutils.py"

clean:
	cd sipgen
	$(MAKE) clean
	@cd ..
	cd siplib
	$(MAKE) clean
	@cd ..
