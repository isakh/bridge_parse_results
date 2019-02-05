"""" From:
https://pagehalffull.wordpress.com/2013/03/05/simple-python-script-that-runs-sql-scripts-against-a-given-sqlite-database/
""""

#!/usr/bin/python2.7 -tt

import sqlite3 as sqlite
import sys

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print "\n\tRequires two arguments:"        
        print "\n\t\tRunSQLiteScript.py {scriptfilename} {databasefilename}\n\n"
        sys.exit()
           
    scriptfilename = sys.argv[1]
    dbfilename = sys.argv[2]

    try:
        print "\nOpening DB"
        connection = sqlite.connect(dbfilename)
        cursor = connection.cursor()
       
        print "Reading Script..."
        scriptFile = open(scriptfilename, 'r')
        script = scriptFile.read()
        scriptFile.close()
        
        print "Running Script..."
        cursor.executescript(script)
        
        connection.commit()
        print "Changes successfully committed\n"        
                        
    except Exception, e:
        print "Something went wrong:"
        print e
    finally:    
        print "\nClosing DB"
        connection.close()
