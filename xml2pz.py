import sys
import os
import getopt
from cmd import Cmd
from obspy import read_inventory

helpstring = """XML to Poles-Zeros Program
---------------------------

USAGE:
    python xml2pz.py -i <input_file>
    OR
    python xml2pz.py --ifile <input_file>

THE ALLOWED FILE EXTENSIONS:
    *.XML OR *.xml
"""

def polezero_f(NETWORK, STATION, CHANNEL, CREATED, START, END, DESCRIPTION, LATITUDE, LONGITUDE, ELEVATION, DEPTH,
               DIP, AZIMUTH, SAMPLE_RATE, INPUT_UNIT, INSTTYPE, INSTGAIN, COMMENT, SENSITIVITY, A0, SACPZ):
    polezero=f"""* **********************************
* NETWORK   (KNETWK): {NETWORK}
* STATION    (KSTNM): {STATION}
* LOCATION   (KHOLE): 
* CHANNEL   (KCMPNM): {CHANNEL}
* CREATED           : {CREATED}
* START             : {START}
* END               : {END}
* DESCRIPTION       : {DESCRIPTION}
* LATITUDE          : {LATITUDE:.6f} 
* LONGITUDE         : {LONGITUDE:.6f} 
* ELEVATION         : {ELEVATION:.1f}  
* DEPTH             : {DEPTH:.1f}  
* DIP               : {DIP:.1f} 
* AZIMUTH           : {AZIMUTH:.1f} 
* SAMPLE RATE       : {SAMPLE_RATE:.1f}
* INPUT UNIT        : {INPUT_UNIT}
* OUTPUT UNIT       : COUNTS
* INSTTYPE          : {INSTTYPE}
* INSTGAIN          : {INSTGAIN:.6e} (M/S)
* COMMENT           : {COMMENT}
* SENSITIVITY       : {SENSITIVITY:.6e} (M/S)
* A0                : {A0:.6e}
* **********************************
{SACPZ}"""
    return polezero

def polezero_f_mod(NETWORK, STATION, CHANNEL, SACPZ):
    polezero=f"""* **********************************
* NETWORK   (KNETWK): {NETWORK}
* STATION    (KSTNM): {STATION}
* LOCATION   (KHOLE): 
* CHANNEL   (KCMPNM): {CHANNEL}
* **********************************
{SACPZ}"""
    return polezero

def convert2pz(inv):
    currdir = os.getcwd()
    destdir = os.path.join(currdir,'output')
    if not os.path.isdir(destdir):
        os.mkdir(destdir)

    for i in range(len(inv)):
        NETWORK = inv[i].code
        for j in range(len(inv[i])):
            STATION = inv[i][j].code
            for k in range(len(inv[i][j])):
                CHANNEL = inv[i][j][k].code
                LOCATION_CODE = inv[i][j][k].location_code
                SACPZ = inv[i][j][k].response.get_sacpz()
                FILENAME = f'SAC_PZs_{NETWORK}_{STATION}_{LOCATION_CODE}_{CHANNEL}'
                CONTENT = polezero_f_mod(NETWORK,STATION,CHANNEL,SACPZ)
                file = open(os.path.join(destdir,FILENAME),'w')
                file.write(CONTENT)
                file.close()
                print(f'{FILENAME} has been created!')

class xml2pz(Cmd):
    prompt = 'xml2pz> '
    intro = """XML to Poles-Zeros Program\n---------------------------\n"""
    inputfile = None
    inv = None

    def __init__(self, arg=None):
        super(xml2pz, self).__init__()
        if arg != None:
            if arg.split('.')[-1] in ('xml', 'XML'):
                self.inputfile = arg
                self.intro += f"file = {self.inputfile}"
                self.inv = read_inventory(self.inputfile)
            else:
                print("""THE ALLOWED FILE EXTENSIONS:\n\t*.XML OR *.xml""")
                sys.exit(2)

    def do_exit(self, arg):
        return True

    def do_quit(self, arg):
        return True

    def do_read(self, arg):
        arg = arg.split()[0]
        if arg.split('.')[-1] in ('xml', 'XML'):
            if os.path.isfile(arg):
                self.inputfile = arg
                self.intro += f"file = {self.inputfile}"
                self.inv = read_inventory(self.inputfile)
            else:
                print("""File Is Not Found.""")
        else:
            print("""THE ALLOWED FILE EXTENSIONS:\n\t*.XML OR *.xml""")

    def do_print(self, arg):
        if self.inputfile != None:
            print(self.inv)
        else:
            print("You Do Not Input The File!\nUse 'read <input_file>' First To Do This")

    def do_convert(self, arg):
        if self.inputfile != None:
            convert2pz(self.inv)
        else:
            print("You Do Not Input The File!\nUse 'read <input_file>' First To Do This")

def main(argv):
    inputfile = None
    try:
        opts, args = getopt.getopt(argv, "hi:co",["ifile="])
    except getopt.GetoptError:
        print("""python xml2pz.py -i <input_file>""")
        sys.exit(2)
    if not opts:
        xml2pz().cmdloop()
    else:
        for opt, arg in opts:
            if opt == '-h':
                print(helpstring)
                sys.exit()
            elif opt in ("-i", "--ifile"):
                if arg.split('.')[-1] in ('xml', 'XML'):
                    inputfile = arg
                else:
                    print("""THE ALLOWED FILE EXTENSIONS:\n\t*.XML OR *.xml""")
                    sys.exit(2)
            elif opt == "-c":
                if inputfile != None:
                    xml2pz(inputfile).cmdloop()
                    sys.exit()
            elif opt == "-o":
                # THE MAIN SCRIPT
                inv = read_inventory(inputfile)
                convert2pz(inv)
                sys.exit()
    if inputfile != None:
        # THE MAIN SCRIPT
        inv = read_inventory(inputfile)
        print(inv)

if __name__ == '__main__':
    main(sys.argv[1:])