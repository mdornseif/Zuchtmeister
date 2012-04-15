# we assume this redisdes in a hierachy created by silver-build-layout.sh
# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ../../bin:$(PATH)
SILVERNODE := mischosting

runserver:
	silver serve ../..

deploy:
	silver update --host 'asksheila.org' --node $(SILVERNODE) ../..

firstdeploy:
	# make SURE all dependencis are in the virtualenv
	../../bin/pip install -I -r ./requirements.txt
	silver -v update --host 'asksheila.org' --node $(SILVERNODE) ../..
	(cd ../../; silver run $(SILVERNODE) manage.py syncdb  --noinput)

livedb_to_test:
	# copies database from the live system onto your box
	scp root@asksheila.org:/var/lib/silverlining/apps/taskmaster/taskmaster.db ~/.silverlining-app-data/files/taskmaster/taskmaster.db

setup: dependencies
	../../bin/python ../../bin/manage.py syncdb --noinput

dependencies:
	../../bin/pip -q install -r ./requirements.txt

clean:
	find . -name '*.pyc' -or -name '*.pyo' | xargs rm
