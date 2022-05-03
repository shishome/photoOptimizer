import photoscript, hashlib, os


def main():
    try:
        os.mkdir("dupes")
    except:
        print("Dir already made... dupes")
    try:
        os.mkdir("export")
    except:
        print("Dir already made... export")
    md5list = []
    BUF_SIZE = 65536
    lib = photoscript.PhotosLibrary()
    lib.activate()

    print(lib.albums())

    foundalbum = lib.create_album("Dupes")

    for x in lib.albums():
        print(x.name)
    for x in lib.photos():
        print(x.albums)
        ls = x.export('export',True,True)
        print(ls)
        md5 = hashlib.md5()
        with open(ls[0], 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
        for n in ls:
            os.remove(n)
        print("MD5: {0}".format(md5.hexdigest()))
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
            if len(fnd.albums) >= len(x.albums):
                foundalbum.add([x])
            else:
                foundalbum.add([fnd])
                md5list[fndindx][1] = x
            x.export('dupes', True, True)
        else:
            md5list.append([md5.hexdigest(), x])

if __name__ == '__main__':
    main()