# Michael Lasutschinkow
# For use in group project with Daniel Tracht and Lucy  Chen

# newsToWiki.py
# reads in file(s) from News Databases


import sys,getopt,os

def main(argv):

    # Expect 2 args (input dir, output dir)
    arglen = len(sys.argv)
    if(arglen!=2):
        print("Need input and output directories")
        sys.exit(1)
    args = str(sys.argv)
    indir = args[0]
    outdir = args[1]
    
    # DO STUFF

    return 0

    
