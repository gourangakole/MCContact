import os,sys
from argparse import ArgumentParser

parser = ArgumentParser()

# https://martin-thoma.com/how-to-parse-command-line-arguments-in-python/
# Add more options if you like
parser.add_argument("-f", "--file", dest="filename",
                    help="input FILE", metavar="FILE")
parser.add_argument("-copy", "--copyToEos", dest="doCopy", default=False,
                    help="make it to true if you want to really copy to eos")

parser.add_argument("-is4FS", "--is4FS", dest="is4FS", default=False,
                    help="make it to true if you want to make a subdir with 4FS")
parser.add_argument("-version", "--version", dest="version", default="v1",
                    help="make it to true if you want to make a subdir with 4FS")
parser.add_argument("-era", "--era", dest="era", default="2017",
                    help="where to keep the gridpack e.g 2017")
parser.add_argument("-MGversion", "--MGversion", dest="mgversion", default="V5_2.6.0",
                    help="which version of MadGraph5 e.g V5_2.6.5/V5_2.4.2")

args = parser.parse_args()

print("Filename: ",args.filename)
print("copyToEos: ",args.doCopy)
print("is4FS: ",args.is4FS)
print("version: ", args.version)
print("era: ",args.era)
print("MGversion: ",args.mgversion)

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
#'/afs/cern.ch/work/w/wshi/public/MSSMD_Mneu1_60_MAD_8p5_cT_2_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz',
#'/afs/cern.ch/work/w/wshi/public/MSSMD_Mneu1_60_MAD_8p5_cT_3_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz',
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
	gridpackdir = gridpackname.split("_slc6")[0]
	#print("gridpackdir", gridpackdir)
	version = args.version # change if needed by hand
        if (args.era == "2016"): 
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc630/13TeV/madgraph'
           # basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/slc6_amd64_gcc481/13TeV/madgraph'
           # basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/pre2017/13TeV/madgraph'
        elif (args.era == "2017"):
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/2017/13TeV/madgraph'
        elif (args.era == "UL"):
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/UL/13TeV/madgraph'
        else:
           basedir = '/eos/cms/store/group/phys_generator/cvmfs/gridpacks/2018/13TeV/madgraph'

        #MGversion = 'V5_2.4.2'
        MGversion = args.mgversion #'V5_2.6.5'

	if (args.is4FS):
           eos_dirpath = basedir+'/'+MGversion+'/4FS/'+gridpackdir+'/'+version+'/'
        else:
           eos_dirpath = basedir+'/'+MGversion+'/'+gridpackdir+'/'+version+'/'

        if (args.is4FS):
           eos_path_to_copy = basedir+'/'+MGversion+'/4FS/'+gridpackdir+'/'+version+'/'+gridpackname
        else:
           eos_path_to_copy = basedir+'/'+MGversion+'/'+gridpackdir+'/'+version+'/'+gridpackname
	#print("eos_path_to_copy", eos_path_to_copy)
	gridpack_cvmfs_path = eos_path_to_copy.replace('/eos/cms/store/group/phys_generator/cvmfs/gridpacks/','/cvmfs/cms.cern.ch/phys_generator/gridpacks/')
        os.system('echo "------------------------------------"')
	print "gridpack_cvmfs_path:  ", gridpack_cvmfs_path
	if not os.path.exists(eos_dirpath):
		print "ERROR: not existing so creating"
		print('eos mkdir -p ' + eos_dirpath);sys.stdout.flush() 
		if(args.doCopy):
			print "copy"
			os.system('eos mkdir -p ' + eos_dirpath);sys.stdout.flush()

	if not os.path.isfile(eos_path_to_copy):
		print('eos cp ' +fullgridpackpath+ ' '+eos_path_to_copy); sys.stdout.flush()
		if(args.doCopy):
			print "copy"
			os.system('eos cp ' +fullgridpackpath+ ' '+eos_path_to_copy); sys.stdout.flush()
		
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

   
       
 
        
              

              
