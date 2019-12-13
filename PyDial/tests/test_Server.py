
import os,sys
curdir = os.path.dirname(os.path.realpath(__file__))
curdir = curdir.split('/')
curdir = '/'.join(curdir[:-1]) +'/'
os.chdir(curdir)
sys.path.append(curdir)

#from nose.tools import with_setup
from ontology import Ontology
from utils import Settings, dummyDialogueServerClient, ContextLogger
import multiprocessing as mp
import DialogueServer
import time
import signal

class TServer():
	"""
	"""
	def __init__(self):
		cfg = 'tests/test_configs/dialogueserver-KUSTOM.cfg'
		assert(os.path.exists(cfg))
		Settings.init(config_file=cfg)
		ContextLogger.createLoggingHandlers(config=Settings.config)

	def ds(self):
		reload(Ontology.FlatOntologyManager)
		Ontology.init_global_ontology()
		dial_server = DialogueServer.DialogueServer()
		dial_server.run()

def Test():
	test = TServer()
	print "\nExecuting tests in",test.__class__.__name__

	global p
	p = mp.Process(target=test.ds)
	p.start()
	print "Listening..."
	

def signal_handler(sig, frame):
	p.terminate()
	print "\nClosing server."
	exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	Test()

#END OF FILE
