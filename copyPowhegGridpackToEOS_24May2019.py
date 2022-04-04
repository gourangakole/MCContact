#gkole last used:
#####
# python copyPowhegGridpackToEOS_24May2019.py -h
# python copyPowhegGridpackToEOS_24May2019.py --file file.txt --era UL 
# python copyPowhegGridpackToEOS_24May2019.py --file filedir/HZZ_VBF_4Apr2022.txt --jhugen -copy 
# python copyPowhegGridpackToEOS_24May2019.py --file filedir/HZZ_ZH_4Apr2022.txt --jhugen --jhugenversion 750 -copy
####

import os,sys
from argparse import ArgumentParser
from stat import *

parser = ArgumentParser()

# https://martin-thoma.com/how-to-parse-command-line-arguments-in-python/
# Add more options if you like
parser.add_argument("-f", "--file", dest="filename",
                    help="input FILE", metavar="FILE")
parser.add_argument("-copy", "--copyToEos", action="store_true", dest="doCopy", default=False,
                    help="make it to True if you want to really copy to eos")
parser.add_argument("-jhugen", "--jhugen", action="store_true", dest="jhugen", default=False,
                    help="make it to True if gridpacks are jhugen")
parser.add_argument("-jhugenversion", "--jhugenversion", dest="jhugenversion", default="751",
                    help="default jhuversion is V751")
parser.add_argument("-version", "--version", dest="version", default="v1",
                    help="change if needed")
parser.add_argument("-era", "--era", dest="era", default="UL",
                    help="where to keep the gridpack e.g 2017/UL")
args = parser.parse_args()

#print(args.filename)
#print(args.doCopy)
print("Input Filename: ",args.filename)
print("copyToEos:      ",args.doCopy)
print("version:        ", args.version)
print("era:            ",args.era)
print("jhugen:         ",args.jhugen)
print("jhugenversion   ",args.jhugenversion)

# ##############################################
# ############ CHECK EOS PERMISSIONS ###########
# ##############################################
# print('assign 755 to all EOS gridpack directories'); sys.stdout.flush()
# os.system('find /eos/cms/store/group/phys_generator/cvmfs/gridpacks/ -type d -exec chmod 755 {} +')
# print('assign 644 to all EOS gridpack files'); sys.stdout.flush()
# os.system('find /eos/cms/store/group/phys_generator/cvmfs/gridpacks/ -type f -exec chmod 644 {} +');
# sys.exit(1)
# ##############################################
# ########## END CHECK EOS PERMISSIONS #########
# ##############################################

#my_path = '/tmp/'+os.environ['USER']+'/replace_gridpacks/'
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class colors:
   colordict = {
                'RED'        : '\033[91m',
                'GREEN'      : '\033[92m',
                'BLUE'       : '\033[34m',
                'GRAY'       : '\033[90m',
                'WHITE'      : '\033[00m',
                'ORANGE'     : '\033[33m',
                'CYAN'       : '\033[36m',
                'PURPLE'     : '\033[35m',
                'LIGHTRED'   : '\033[91m',
                'PINK'       : '\033[95m',
                'YELLOW'     : '\033[93m',
                'BLINK'      : '\033[5m' ,
                'NORMAL'     : '\033[28m' ,
                "WARNING"    : '\033[33m',
                "CEND"       : '\033[0m',
                }
   if sys.stdout.isatty():
        RED      = colordict['RED']
        GREEN    = colordict['GREEN']
        BLUE     = colordict['BLUE']
        GRAY     = colordict['GRAY']
        WHITE    = colordict['WHITE']
        ORANGE   = colordict['ORANGE']
        CYAN     = colordict['CYAN']
        PURPLE   = colordict['PURPLE']
        LIGHTRED = colordict['LIGHTRED']
        PINK     = colordict['PINK']
        YELLOW   = colordict['YELLOW']
        BLINK    = colordict['BLINK']
        NORMAL   = colordict['NORMAL']
        WARNING  = colordict['WARNING']
        CEND     = colordict['CEND']
   else:
        RED, GREEN, BLUE, GRAY, WHITE, ORANGE, CYAN, PURPLE, LIGHTRED, PINK, YELLOW, BLINK, NORMAL, WARNING = '', '', '', '', '', '', '', '', '', '', '', '', '', ''

#----------------------------------------------------------------------
# main
#----------------------------------------------------------------------
#if len(sys.argv)<2:
#print "Usage: python test_copy_16Aug.py inputfile"
#	exit(0)

#print "No. of args: ", len(sys.argv)
ARGV0 = sys.argv
inputFname = args.filename


# this is working
#fullgridpackpaths = open("/afs/cern.ch/user/g/gkole/work/public/abcd_v2.txt").read().splitlines()
if not( os.path.isfile(inputFname) ):
   print "WARNING!!! " + str(inputFname) + " not found!"
   exit(0)

fullgridpackpaths = open(inputFname).read().splitlines()
print "Total number of gridpacks: ", len(fullgridpackpaths)

#fullgridpackpaths = [
#'/eos/cms/store/user/gkole/Hgg/MC_contact/2017_gridpack/ggh/ggh012j_5f_NLO_FXFX_125_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz',
#           ]

##########################################
######## START LOOP OVER EACH GRIDPACK #########
##########################################
for fullgridpackpath in fullgridpackpaths:

        #os.system('echo '+fullgridpackpath) # this is just for prining initial full path
	#print('stat -c "%a %n"' +fullgridpackpath) # FIXME in future for check the permission
	gridpackname = fullgridpackpath.split("/")[-1]
	#print("gridpackname", gridpackname)
        newpath = fullgridpackpath.rstrip()
        # check gridpack permission throw errors if not 644
        errormsg = '{:<20} {:<40}'.format("%sGridpack" % (colors.colordict["RED"]) , ": "+fullgridpackpath)
        if (int (oct(os.stat(newpath)[ST_MODE])[-3:])) != 644:
           raise Exception(errormsg + "\nhas different permission than 644!")
           
	gridpackdir = gridpackname.split(".tgz")[0]
	#print("gridpackdir", gridpackdir)
	version = args.version # change if needed by hand
        if (args.era == "2016"): 
           # basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc630/13TeV/Powheg'
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc7_amd64_gcc700/13TeV/powhegV2'
        elif (args.era == "2017"):
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/2017/13TeV/powheg'
        elif (args.era == "UL"):
           if args.jhugen :
              basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/UL/13TeV/jhugen/V'+args.jhugenversion
           else:
              basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/UL/13TeV/powheg'
        else:
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/2018/13TeV/powheg'
           
	# basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/2017/13TeV/madgraph'
	if (args.era == "2016"):
           MGversion = ''
        else:
           if args.jhugen :
              MGversion = ''
           else:
              MGversion = 'V2/'
	eos_dirpath = basedir+'/'+MGversion+gridpackdir+'/'+version+'/'
	eos_path_to_copy = basedir+'/'+MGversion+gridpackdir+'/'+version+'/'+gridpackname
	#print("eos_path_to_copy", eos_path_to_copy)
	gridpack_cvmfs_path = eos_path_to_copy.replace('/eos/cms/store/group/phys_generator/cvmfs/gridpacks/','/cvmfs/cms.cern.ch/phys_generator/gridpacks/')
        os.system('echo "------------------------------------"')
	print "gridpack_cvmfs_path:  ", colors.colordict["GREEN"] + gridpack_cvmfs_path + colors.colordict["CEND"]
	if not os.path.exists(eos_dirpath):
		print colors.colordict["WARNING"] + "ERROR: not existing so creating" + colors.colordict["CEND"]
		print('eos mkdir -p ' + eos_dirpath);sys.stdout.flush() 
		if(args.doCopy):
			print "copy"
			os.system('eos mkdir -p ' + eos_dirpath);sys.stdout.flush()

	if not os.path.isfile(eos_path_to_copy):
		print('eos cp ' +fullgridpackpath+ ' '+eos_path_to_copy); sys.stdout.flush()
		if(args.doCopy):
			print "copy"
			os.system('eos cp ' +fullgridpackpath+ ' '+eos_path_to_copy); sys.stdout.flush()
                        #os.system('cp ' +fullgridpackpath+ ' '+eos_path_to_copy); sys.stdout.flush() # if the user's file on EOS then do "cp bla bla"
        #os.system('mkdir -p '+my_path+'/'+prepid)
        #os.chdir(my_path+'/'+prepid)
        #os.system('wget -q https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/'+prepid+' -O '+prepid)
        #gridpack_cvmfs_path = os.popen('grep \/cvmfs '+prepid).read()
        #gridpack_cvmfs_path = gridpack_cvmfs_path.split('\'')[1]
	#print (gridpack_cvmfs_path)
	#os.system('tar xf '+gridpack_cvmfs_path+' -C'+my_path+'/'+prepid)
	#os.system('more '+my_path+'/'+prepid+'/'+'runcmsgrid.sh | grep "FORCE IT TO"')
	#os.system('grep _CONDOR_SCRATCH_DIR '+my_path+'/'+prepid+'/'+'mgbasedir/Template/LO/SubProcesses/refine.sh')
	#os.system('echo "------------------------------------"')
#        os.system('rm '+prepid)
##########################################
######## END LOOP OVER PREPIDS ###########
##########################################
os.system('echo "------------------------------------"')

#        gridpack_eos_path = gridpack_cvmfs_path.replace('/cvmfs/cms.cern.ch/phys_generator/gridpacks/','/eos/cms/store/group/phys_generator/cvmfs/gridpacks/')

   
       
 
        
              

              
