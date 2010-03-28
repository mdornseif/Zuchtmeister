# we assume this redisdes in a hierachy vreated by silver-build-layout.sh
# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ../../bin:$(PATH)
SILVERNODE := mischosting

runserver: dependencies
	silver serve ../..

deploy:
	silver update --host 'asksheila.org' --node $(SILVERNODE) ../..

firstdeploy:
	# make SURE all dependencis are in the virtualenv
	../../bin/pip install -I -r ./requirements.txt
	silver -v update --host 'asksheila.org' --node $(SILVERNODE) ../..
	(cd ../../; silver run $(SILVERNODE) manage.py syncdb  --noinput)

#generic_templates:
#	sh -c 'echo p | svn co https://cybernetics.hudora.biz/intern/svn/code/projects/html/trunk/templates generic_templates'

setup: dependencies
	../../bin/python ../../bin/manage.py syncdb --noinput

dependencies:
	../../bin/pip -q install -r ./requirements.txt

clean:
	find . -name '*.pyc' -or -name '*.pyo' | xargs rm
