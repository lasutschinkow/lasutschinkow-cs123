# Michael Lasutschinkow
# For use in group project with Daniel Tracht and Lucy  Chen

# newsToWiki.py
# reads in file(s) from News Databases


import sys,getopt,os
import multiprocessing as mp
from multiprocessing import Queue

WIKI_DB_DIR = ""
OUT_DB_DIR = ""
NUM_FILE_WORKERS = 2   # number of file-read processes
NUM_DATA_WORKERS = 8   # number of queue-process processes


# File-parsing MP job
def parseFile(fq,hq): # args file_queue, headline_queue
    for db_file in iter(fq.get, 'EMPTY'):
        f = open(db_file)
        data = f.readLines()
        for Line in data:
            entry = line.split(';')
            # Expected Data Format :
            # Date, headline, [keywords], description, articleID
            date = entry[0]
            headline = entry[1]
            keywords = entry[2].split(',')
            description = entry[4]
            articleID = int(entry[5].strip()) 
            for keyword in keywords:
                hq.put([date,keyword])
        f.close()
    return True







def main():

    # Expect 3 args (Wiki dir, News dir, output dir)
    arglen = len(sys.argv)
    if(arglen!=4):
        print("Need Wiki, input and output directories")
        sys.exit(1)
    global WIKI_DB_DIR
    WIKI_BB_DIR = sys.argv[1]
    in_dir = os.listdir(sys.argv[2])
    global OUT_DB_DIR
    OUT_DB_DIR = sys.argv[3]
    
    # Creating Queues
    
    file_queue = Queue()
    for f in in_dir:
        file_queue.put(f)
    file_queue.put('EMPTY')
    hl_queue = Queue()


    # Using file_queue to populate hl_queue
    global NUM_FILE_WORKERS
    file_workers=[]
    for i in range(NUM_FILE_WORKERS):
        p = mp.Process(target=parseFile,args=(file_queue, hl_queue))
        p.start()
        file_workers.append(p)
    for fw in file_workers:
        fw.join()


    # Now need to creatae processes to use data in hl_queue



    return 0

    
main()
