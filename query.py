if __name__ == '__main__':
    import sys
    import os
    import os.path
    import argparse
    import codecs

    def passcode(s):
        try:
            regcode, userid = s.split(',')
        except:
            raise argparse.ArgumentTypeError("Passcode must be regcode,userid")
        try:
            regcode = codecs.decode(regcode, 'hex')
        except:
            raise argparse.ArgumentTypeError(
                "regcode must be a 32 bytes hexadecimal string")
        return regcode, userid

    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--extract', action="store_true",
                        help='extract mdx to source format and extract files from mdd')
    parser.add_argument('-s', '--substyle', action="store_true",
                        help='substitute style definition if present')
    parser.add_argument('-d', '--datafolder', default="data",
                        help='folder to extract data files from mdd')
    parser.add_argument('-e', '--encoding', default="",
                        help='override the encoding specified in the mdx file')
    parser.add_argument('-p', '--passcode', default=None, type=passcode,
                        help='register_code,email_or_deviceid')
    parser.add_argument("filename", nargs='?', help="mdx file name")
    args = parser.parse_args()

    # use GUI to select file, default to extract
    if not args.filename:
        if sys.hexversion < 0x03000000:
            import Tkinter
            import tkFileDialog
        else:
            import tkinter as Tkinter
            import tkinter.filedialog as tkFileDialog
        root = Tkinter.Tk()
        root.withdraw()
        args.filename = tkFileDialog.askopenfilename(parent=root)
        args.extract = True

    if not os.path.exists(args.filename):
        print("Please specify a valid MDX/MDD file")

    base, ext = os.path.splitext(args.filename)

    # read mdx file
    if ext.lower() == os.path.extsep + 'mdx':
        mdx = MDX(args.filename, args.encoding, args.substyle, args.passcode)
        if type(args.filename) is unicode:
            bfname = args.filename.encode('utf-8')
        else:
            bfname = args.filename
        print('======== %s ========' % bfname)
        print('  Number of Entries : %d' % len(mdx))
        for key, value in mdx.header.items():
            print('  %s : %s' % (key, value))
    else:
        mdx = None

    # find companion mdd file(s)
    i = 0
    mdds = []
    while True:
        extra = '' if i == 0 else '.%d' % i
        mdd_filename = ''.join([base, extra, os.path.extsep, 'mdd'])
        if os.path.exists(mdd_filename):
            mdd = MDD(mdd_filename, args.passcode)
            if type(mdd_filename) is unicode:
                bfname = mdd_filename.encode('utf-8')
            else:
                bfname = mdd_filename
            print('======== %s ========' % bfname)
            print('  Number of Entries : %d' % len(mdd))
            for key, value in mdd.header.items():
                print('  %s : %s' % (key, value))
            mdds.append(mdd)
        else:
            break
        i += 1

    if args.extract:
        # write out glos
        if mdx:
            output_fname = ''.join([base, os.path.extsep, 'txt'])
            tf = open(output_fname, 'wb')
            for key, value in mdx.items():
                tf.write(key)
                tf.write(b'\r\n')
                tf.write(value)
                if not value.endswith(b'\n'):
                    tf.write(b'\r\n')
                tf.write(b'</>\r\n')
            tf.close()
            # write out style
            if mdx.header.get(b'StyleSheet'):
                style_fname = ''.join([base, '_style', os.path.extsep, 'txt'])
                sf = open(style_fname, 'wb')
                sf.write(b'\r\n'.join(mdx.header[b'StyleSheet'].splitlines()))
                sf.close()
        # write out optional data files
        if mdds:
            datafolder = os.path.join(
                os.path.dirname(args.filename), args.datafolder)
            if not os.path.exists(datafolder):
                os.makedirs(datafolder)
            for mdd in mdds:
                for key, value in mdd.items():
                    fname = key.decode('utf-8').replace('\\', os.path.sep)
                    dfname = datafolder + fname
                    if not os.path.exists(os.path.dirname(dfname)):
                        os.makedirs(os.path.dirname(dfname))
                    df = open(dfname, 'wb')
                    df.write(value)
                    df.close()
