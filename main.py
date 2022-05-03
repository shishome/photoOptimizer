import photoscript, hashlib, os
import dotenv

dotenv.load_dotenv()

def main():
    try:
        os.mkdir("dupes")
    except:
        print("WARNING: Dir already made... dupes")
    try:
        os.mkdir("export")
    except:
        print("WARNING: Dir already made... export")
    md5list = []
    BUF_SIZE = 65536
    print("SETUP: Launching Photos.app and Connecting. Be sure to allow automation.")
    lib = photoscript.PhotosLibrary()
    lib.activate()
    print("SETUP: Creating a duplicates album.")
    foundalbum = lib.create_album("Dupes")
    print("SETUP: Counting objects in library... this may take awhile.")
    c = int(os.environ.get("PHOTO_LIB_COUNT")) or 0
    print("SETUP: Number of Items: %s" % c)
    if c == 0:
        print("Error. Set Environment Variable PHOTO_LIB_COUNT with total number of photos and videos combined in your library.")
    pgs = round(c / 10) + 1
    z = 1
    print("SETUP: Number of pages: %s" % pgs)
    while pgs != z:
        print("PROGRESS: Fetching %s - %s to process... This may take a moment." % ( (z-1) * 10, z * 10) )
        for x in lib.photos(None, None, [((z - 1) * 10),(z * 10)]):
            ls = x.export('export',True,True)
            md5 = hashlib.md5()
            if(len(ls) == 0):
                print("ERROR: Didn't export anything, this may be a glitch.")
            else:
                with open(ls[0], 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        md5.update(data)
                for n in ls:
                    os.remove(n)
                print("PROCESS: {0} / MD5: {1}".format(str(ls), md5.hexdigest()))
                found = False
                fndindx = 0
                indx = 0
                for y in md5list:
                    if y[0] == md5.hexdigest():
                        found = True
                        fnd = y[1]
                        fndindx = indx
                    indx += 1
                if found:
                    print(" - SUBPROCESS: {0} / Found a duplicate.".format(str(ls)))
                    if len(fnd.albums) >= len(x.albums) or fnd.favorite:
                        foundalbum.add([x])
                        x.export('dupes', False, True)
                    else:
                        print(" - SUBPROCESS: {0} / Previous instance of image has less album assignments -or- Current instance is a favorite. Marking previous instance as a duplicate.".format(str(ls)))
                        foundalbum.add([fnd])
                        md5list[fndindx][1] = x
                        x.export('dupes', False, True)
                else:
                    md5list.append([md5.hexdigest(), x])
        print("///////////////////////////////////////////")
        z = z + 1

if __name__ == '__main__':
    main()