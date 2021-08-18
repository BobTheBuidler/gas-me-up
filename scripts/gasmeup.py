import subprocess
from brownie import run
from my_details import handle
from datetime import datetime

def main():
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

    #run('scripts/gasmeup')
    process = subprocess.Popen(["git", "add", "--all"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

    commitmsg = f'{handle} thru {datetime.utcnow()}'
    process = subprocess.Popen(["git", "commit", "-m", commitmsg], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)