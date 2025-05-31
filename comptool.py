import os, subprocess, argparse, sys, datetime, configparser, platform

# get folder paths from config file
try:
    config = configparser.ConfigParser()
    config.read(f'{os.path.dirname(os.path.realpath(__file__))}/comptool.config') # config file name
    section = platform.node()
    LEFT_ROOT = config[section]['left']
    RITE_ROOT = config[section]['rite']
    LOG_FILE = config[section]['logfile']
    IGNORES = config[section]['ignores'].split(',')
except Exception as e: print(f"Could not read configuration: {e}"); sys.exit(3)

def choice(prompt: str):
    print(prompt, end=' ')
    while True:
        r = input()
        if r.upper() == 'Y': return True
        elif r.upper() == 'N': return False
        else: print('Please respond with "y" or "n":', end=' ')

# run diff for a quick comparison. if different, ask to run meld. in any case, prompt to try again.
def unix_compare():
    while True:
        # create exclude arguments
        diff_ignores = []
        for item in IGNORES: 
            parsed = item.replace('\\','').replace(' ',r'\ ')
            diff_ignores.append("-x"); 
            diff_ignores.append(parsed)
        
        # run diff
        diff_args = ["diff", "-rq"] + diff_ignores + [LEFT_ROOT+ITEM, RITE_ROOT+ITEM]
        p = subprocess.run(diff_args)
        if p.returncode == 0:
            print("Items are identical between copies.")
            break
        elif p.returncode == 1:
            if choice("\nItems have differences as described above.\nOpen meld to investigate? (y/n):"): 
                # meld runs with sudo permissions to avoid permission errors trying to delete files
                p = subprocess.run(["sudo", "meld", LEFT_ROOT+ITEM, RITE_ROOT+ITEM])
        else: raise Exception("diff failed; see above.") # diff will have printed detailed error

        # try again
        if not choice("Rerun comparison?"): break

# open winmerge to perform file comparison.
def windows_compare():
    print("Calling WinMerge...")
    winmerge_install = config[section]['winmerge']
    win_ignores = ''.join(f"!{item};" for item in IGNORES).replace('\\\\','\\')
    p = subprocess.run([f"{winmerge_install}", LEFT_ROOT+ITEM, RITE_ROOT+ITEM, "/f", f"{win_ignores}"])

############################# MAIN EXECUTION STARTS HERE #############################

# comparison prerequisites
try:
    # get commandline arguments
    parser = argparse.ArgumentParser(prog='comptool', description='A platform-agnostic tool for comparing an internal drive to an external copy.')
    parser.add_argument('-s', '--subfolder', help='Path to a subfolder to compare.')
    ARGS = parser.parse_args()

    # extract just item to compare from given path (define ITEM constant)
    # if subfolder is provided, strip the containing root from the path so it can be added to both roots.
    if ARGS.subfolder == None: ITEM = ""
    else:
        ITEM = os.path.realpath(ARGS.subfolder)
        if   ITEM.startswith(LEFT_ROOT): ITEM = ITEM[len(LEFT_ROOT):]
        elif ITEM.startswith(RITE_ROOT): ITEM = ITEM[len(RITE_ROOT):]
        else: raise Exception("Given subfolder path is not in either data root.")

    # validate existence of item to compare
    print(f"Trying to compare:\n{LEFT_ROOT+ITEM}\n{RITE_ROOT+ITEM}\n")
    if not (os.path.exists(LEFT_ROOT+ITEM) and os.path.exists(RITE_ROOT+ITEM)): raise Exception("One of the items above was not found.")

except Exception as e: print(f"Input parameters error: {e}"); sys.exit(2)

# perform comparison
try: 
    if not choice("Press y to start, or n to cancel..."): sys.exit(0)
    if os.name == 'nt':     windows_compare()
    if os.name == 'posix':  unix_compare()

    # log
    with open(LOG_FILE,'a') as log: log.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ({platform.node()})  /{ITEM}\n")
except Exception as e: print(f"Error during comparison: {e}"); sys.exit(1)

sys.exit(0)