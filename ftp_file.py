from ftplib import FTP
import os, sys, string, datetime, time

hostaddr = '10.204.16.2'
username = 'l10n_build'
password = 'Q1234%tt'
port = 21
rootdir_local = 'D://python/sourcebakup/'
rootdir_remote = '/L10N/L10N_System_backup/test1/'

def login(remotedir = '.'):
	try:
		ftp.set_pasv(True) 
		ftp.connect(hostaddr, port)
		ftp.login(username, password)
		log('---------------------')
		log('connect success: ' + ftp.getwelcome())
	except Exception:
		log('connect failed')
		sys.exit()

	try:
		ftp.cwd(remotedir)
	except Exception:
		log('switch dir failed')
		sys.exit()

def is_same_size(localfile, remotefile):
	try:
		remotefile_size = ftp.size(remotefile)
	except:
		remotefile_size = -1

	try:
		localfile_size = os.path.getsize(localfile)
	except:
		localfile_size = -1
	if remotefile_size == localfile_size:
		return True
	else:
		return False

def upload_file(localfile, remotefile):
	if not os.path.isfile(localfile):
		return
	if is_same_size(localfile, remotefile):
		log('file exist: %s' %localfile)
		return
	file_handler = open(localfile, 'rb')
	ftp.storbinary('STOR %s' %remotefile, file_handler)
	file_handler.close()
	log('file upload: %s' %localfile)

def upload_files(localdir = './', remotedir = './'):
	if not os.path.isdir(localdir):
		return
	localnames = os.listdir(localdir)
	ftp.cwd(remotedir)

	for item in localnames:
		src = os.path.join(localdir, item)
		if os.path.isdir(src):
			try:
				ftp.mkd(item)
			except:
				log('dir exist: %s' %item)
			upload_files(src, item)
		else:
			upload_file(src, item)
	ftp.cwd('..')

def log(msg):
	datenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	logstr = '%s : %s \n' %(datenow, msg)
	logfile.write(logstr)

if __name__ == '__main__':
	logfile = open('log.txt', 'a')
	ftp = FTP()
	login(rootdir_remote)
	upload_files(rootdir_local, rootdir_remote)
	log('success')
	log('------------------------')
	logfile.close()