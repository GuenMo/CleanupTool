# coding:utf-8
def cleanup_run():
    try:
        filePath = __file__
        app_Path = filePath.rpartition('\\')[0]
    except:
        print "Environ Value 'cleanup Tool' not exist."
    
    else:
        import sys
        path = app_Path
        
        if not path in sys.path:
            sys.path.append(path)
        
        import cleanupTool 
        reload(cleanupTool)
        cleanupTool.main(True)

if __name__ == 'cleanup_run':  
    cleanup_run()