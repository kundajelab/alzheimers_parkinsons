import sys

def main(args):

    with open(args[0]) as infile, open(args[1], 'w') as outfile:
        outfile.write('[\n')
        i = 0
        for line in infile:
            loc = line[29:].strip()
            name1 = line.split('outputs/')[1].split('/cromwell')[0].strip()
            name2 = line.split('.signal.bigwig')[0].split('gz.')[1].strip()
            name = name1 + '_' + name2
            if i != 0:
                outfile.write(',\n')
            outfile.write('{"type": "bigwig","url": "http://mitra.stanford.edu/kundaje')
            outfile.write(loc)
            outfile.write('","mode": 1,"name": "')
            outfile.write(name)
            outfile.write('","qtc": {"anglescale":1,"pr":255,"pg":71,"pb":20,"nr":255,"ng":0,"nb":0,"pth":"rgb(0,0,178)","nth":"#800000","thtype":1,"thmin":0,"thmax":25,"thpercentile":90,"height":50,"summeth":1}}')
            i += 1
        outfile.write('\n]')


if __name__ == '__main__':
    main(sys.argv[1:])
