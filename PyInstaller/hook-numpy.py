from PyInstaller import log as logging 
from PyInstaller import compat
from os import listdir

mkldir = compat.base_prefix + "/Library/bin" 
logger = logging.getLogger(__name__)
logger.info("MKL installed as part of numpy, importing that!")
binaries = [(mkldir + "/" + mkl, '') for mkl in listdir(mkldir) if mkl.startswith('mkl_')] 
