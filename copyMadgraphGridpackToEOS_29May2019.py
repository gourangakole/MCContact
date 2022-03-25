import os,sys
from argparse import ArgumentParser
from stat import *
'''
#Last used:
python copyMadgraphGridpackToEOS_29May2019.py --file filedir/Lata_07May_2021.txt 
python copyMadgraphGridpackToEOS_29May2019.py --file filedir/dynunu_Tommaso_17Mar2021.txt --era UL --MGversion V5_2.6.5
python copyMadgraphGridpackToEOS_29May2019.py --file filedir/HWW_one.txt --era 2016 --MGversion V5_2.6.5 --version v2
python copyMadgraphGridpackToEOS_29May2019.py --file filedir/HExtended_T_16Mar2022.txt --extraDir True --extraDirName GF_Spin_0
python copyMadgraphGridpackToEOS_29May2019.py --file filedir/Thomasso_25Mar2022.txt --era 2017 --MGversion V5_2.4.2 --arch slc6 -copy
'''
parser = ArgumentParser()

# https://martin-thoma.com/how-to-parse-command-line-arguments-in-python/
# Add more options if you like
parser.add_argument("-f", "--file", dest="filename",
                    help="input FILE", metavar="FILE")
parser.add_argument("-copy", "--copyToEos", action="store_true", dest="doCopy", default=False,
                    help="make it to True if you want to really copy to eos")
parser.add_argument("-is4FS", "--is4FS", dest="is4FS", default=False,
                    help="make it to true if you want to make a subdir with 4FS")
parser.add_argument("-version", "--version", dest="version", default="v1",
                    help="if you want to copy in v2 directry")
parser.add_argument("-era", "--era", dest="era", default="UL",
                    help="where to keep the gridpack e.g 2017")
parser.add_argument("-MGversion", "--MGversion", dest="mgversion", default="V5_2.6.5",
                    help="which version of MadGraph5 e.g V5_2.6.5/V5_2.4.2")
parser.add_argument("-arch", "--arch", dest="arch", default="slc7",
                    help="which Arch what to keep for gridpack")

parser.add_argument("-extraDir", "--extraDir", dest="extraDir", default=False,
                    help="if you want to copy gridpack in a paricular dir make it True")

parser.add_argument("-extraDirName", "--extraDirName", dest="extraDirName", default="besure",
                    help="if you want to copy gridpacks in a particular dir")

args = parser.parse_args()

print("Filename: ",args.filename)
print("copyToEos: ",args.doCopy)
print("is4FS: ",args.is4FS)
print("version: ", args.version)
print("era: ",args.era)
print("MGversion: ",args.mgversion)
print("arch: ",args.arch)
print("extraDir: ", args.extraDir)
print("extraDirName: ", args.extraDirName)
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

print "No. of args: ",len(sys.argv)
ARGV0 = sys.argv
inputFname = args.filename


# this is working
#fullgridpackpaths = open("/afs/cern.ch/user/g/gkole/work/public/abcd_v2.txt").read().splitlines()
if not( os.path.isfile(inputFname) ):
   print "WARNING!!! " + str(inputFname) + " not found!"
   exit(0)

fullgridpackpaths = open(inputFname).read().splitlines()
print "Total number of gridpack: ", len(fullgridpackpaths)

#fullgridpackpaths = [
#'/afs/cern.ch/work/w/wshi/public/MSSMD_Mneu1_60_MAD_8p5_cT_1_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz',
#'/afs/cern.ch/work/w/wshi/public/MSSMD_Mneu1_60_MAD_8p5_cT_3_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz',
#'/eos/cms/store/user/gkole/Hgg/MC_contact/2017_gridpack/ggh/ggh012j_5f_NLO_FXFX_125_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz',
#           ]

##########################################
######## START LOOP OVER EACH GRIDPACK #########
##########################################
for fullgridpackpath in fullgridpackpaths:

        #os.system('echo '+fullgridpackpath) # this is just for prining initial full path
	gridpackname = fullgridpackpath.split("/")[-1]
        #print "check: ", fullgridpackpath
        newpath = fullgridpackpath.rstrip()
        # check gridpack permission throw errors if not 644
        errormsg = '{:<20} {:<40}'.format("%sGridpack" % (colors.colordict["RED"]) , ": "+fullgridpackpath)
        if (int (oct(os.stat(newpath)[ST_MODE])[-3:])) != 644:
           raise Exception(errormsg + "\nhas different permission than 644!")
	#print("gridpackname", gridpackname)
        gridpackdir = gridpackname.split("_"+args.arch)[0]
        #gridpackdir = gridpackname.split("_slc7")[0]
	#print("gridpackdir", gridpackdir)
	version = args.version 
        if (args.era == "2016"): 
           # basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc630/13TeV/madgraph'
           # basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc481/13TeV/madgraph'
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/pre2017/13TeV/madgraph'
        elif (args.era == "2017"):
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/2017/13TeV/madgraph'
        elif (args.era == "UL"):
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/UL/13TeV/madgraph'
        else:
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/2018/13TeV/madgraph'

        MGversion = args.mgversion #'V5_2.6.5'
        if (args.extraDir):
           extraDirName = args.extraDirName

	if (args.is4FS):
           eos_dirpath = basedir+'/'+MGversion+'/4FS/'+gridpackdir+'/'+version+'/'
        else:
           eos_dirpath = basedir+'/'+MGversion+'/'+gridpackdir+'/'+version+'/'

        if (args.is4FS):
           eos_path_to_copy = basedir+'/'+MGversion+'/4FS/'+gridpackdir+'/'+version+'/'+gridpackname
        else:
           eos_path_to_copy = basedir+'/'+MGversion+'/'+gridpackdir+'/'+version+'/'+gridpackname

        if (args.extraDir):
           if(args.is4FS):
              eos_path_to_copy = basedir+'/'+MGversion+'/4FS/'+extraDirName+'/'+gridpackdir+'/'+version+'/'+gridpackname
              eos_dirpath = basedir+'/'+MGversion+'/4FS/'+extraDirName+'/'+gridpackdir+'/'+version+'/'
           else:
              eos_path_to_copy = basedir+'/'+MGversion+'/'+extraDirName+'/'+gridpackdir+'/'+version+'/'+gridpackname
              eos_dirpath = basedir+'/'+MGversion+'/'+extraDirName+'/'+gridpackdir+'/'+version+'/'
              
	#print("Sanity: eos_path_to_copy", eos_path_to_copy)
        #print("Sanity: eos_dirpath", eos_dirpath)

	gridpack_cvmfs_path = eos_path_to_copy.replace('/eos/cms/store/group/phys_generator/cvmfs/gridpacks/','/cvmfs/cms.cern.ch/phys_generator/gridpacks/')
        os.system('echo "------------------------------------"')
	print "gridpack_cvmfs_path:  ", colors.colordict["GREEN"] + gridpack_cvmfs_path + colors.colordict["CEND"]

	if not os.path.exists(eos_dirpath):
		print colors.colordict["WARNING"]+"ERROR: not existing so creating"+colors.colordict["CEND"]
		print('eos mkdir -p ' + eos_dirpath);sys.stdout.flush() 
		if(args.doCopy):
			print "copy"
			os.system('eos mkdir -p ' + eos_dirpath);sys.stdout.flush()

	if not os.path.isfile(eos_path_to_copy):
		print('eos cp ' +fullgridpackpath+ ' '+eos_path_to_copy); sys.stdout.flush()
		if(args.doCopy):
			print "copy"
			os.system('eos cp ' +fullgridpackpath+ ' '+eos_path_to_copy); sys.stdout.flush()
                        # os.system('cp ' +fullgridpackpath+ ' '+eos_path_to_copy); sys.stdout.flush() # if the user's file on EOS then do "cp bla bla" 
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
