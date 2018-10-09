import os

def get_max_dir(maxid_file):
	with open(maxid_file, "rb") as f:
		return f.read()

def create_web_dirs(maxid_file):
	cwd = os.getcwd()
	max_dir = int(get_max_dir(maxid_file))
	os.chdir('/var/www/')
	os.system("rm -rf *.com")
	for x in range(0, max_dir+1):
		x_dir = str(x)+'.com'
		if not os.path.exists(x_dir):
			os.system('sudo mkdir -p '+x_dir+'/public_html')	
			os.system('sudo chown -R $(whoami):$(whoami) '+x_dir+'/public_html')
		
		if not os.path.exists('../../etc/apache2/sites-available/'+x_dir+'.conf'):
			with open('/etc/apache2/sites-available/'+x_dir+'.conf', 'wb') as f:
				f.write('<VirtualHost *:80>\n\tServerAdmin webmaster@'+x_dir+'\n\tServerName '+x_dir+'\n\tServerAlias www.'+x_dir+'\n\tDocumentRoot /var/www/'+x_dir+'/public_html\n\tErrorLog ${APACHE_LOG_DIR}/error.log\n\tCustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>')
			os.system('sudo a2ensite '+x_dir+'.conf')
	os.chdir(cwd)

#create_web_dirs(maxid_file)
