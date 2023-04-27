import subprocess, os, time

REPO_URL = "https://github.com/pafinkbeiner/pDrone.git"
WORKING_DIRECTORY = "pDrone"
EXECUTION_COMMAND = ["python3", "script.py"]
REFRESH_RATE = 3

def clone_repository():
    subprocess.run(["git", "clone", REPO_URL])

def refresh_repo():
    subprocess.run(["git", "pull"], cwd=WORKING_DIRECTORY)
    
def get_size(start_path = WORKING_DIRECTORY):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


last_size = 0
p = None
while True:
    # refresh repo if it changed
    if not os.path.exists(WORKING_DIRECTORY):
        clone_repository()
    else:
        refresh_repo()
    
    # if it changed execute script
    current_size = get_size()
    print("Last Size: " + str(last_size))
    print("Current Size: "+ str(current_size))

    if current_size != last_size:
        if p != None: 
            p.kill()
        print("STARTING SUBPROCESS")
        p = subprocess.Popen(EXECUTION_COMMAND, cwd=WORKING_DIRECTORY)

    last_size = current_size

    # Delay
    time.sleep(REFRESH_RATE)