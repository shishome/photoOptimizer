import photoscript, hashlib, os
import dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import session
from sqlalchemy_orm.session import Session

from models.image import Image, Base

dotenv.load_dotenv()
engine = create_engine("sqlite:///db.sqlite3", echo=True, future=True)

Image.metadata.create_all(engine)

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
    #z = 1
    z = 1921
    itm = (z - 1) * 10
    print("SETUP: Number of pages: %s" % pgs)
    while pgs != z:
        end = z * 10
        if(end > (c - 1)):
            end = c - 1
        print("PROGRESS: Fetching %s - %s to process... This may take a moment." % ( (z-1) * 10, end) )
        for x in lib.photos(None, None, [((z - 1) * 10),(end)]):
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

                with Session(engine) as session:
                    stmt = select(Image).where(Image.id == md5.hexdigest())
                    for y in session.scalars(stmt):
                        if y.id == md5.hexdigest():
                            found = True
                            fnd = int(y.name)
                            fndid = y.id
                        indx += 1
                    if found:
                        print(" - SUBPROCESS: {0} / Found a duplicate.".format(str(ls)))
                        print("fnd", fnd)
                        lkp = lib.photos(None,None,[fnd,fnd+1])
                        lkpi = 0
                        print(lkp)
                        for fnddex in lkp:
                            if(lkpi == 0):
                                fnd1 = fnddex
                                lkpi += 1
                        if len(fnd1.albums) >= len(x.albums) or fnd1.favorite:
                            foundalbum.add([x])
                            x.export('dupes', False, True)
                        else:
                            print(" - SUBPROCESS: {0} / Previous instance of image has less album assignments -or- Current instance is a favorite. Marking previous instance as a duplicate.".format(str(ls)))
                            foundalbum.add([fnd1])
                            #md5list[fndindx][1] = x
                            stmt = select(Image).where(Image.id == fndid)
                            upd = session.scalars(stmt).one()
                            upd.name = itm
                            x.export('dupes', False, True)
                    else:
                        new = Image(
                            id=md5.hexdigest(),
                            name=str(itm)
                        )
                        session.add_all([new])
                        #md5list.append([md5.hexdigest(), x])
                    session.commit()
            itm += 1
        print("///////////////////////////////////////////")
        z = z + 1

if __name__ == '__main__':
    main()