import sys
import run_gkmexplain


def main(args):

    for gwas in ['Kunkle', '23andme_PD', 'Chang', 'Nalls']:
        run_gkmexplain.main([args[0], 'all', gwas, 'overlap', int(args[1])])


if __name__ == "__main__":
    main(sys.argv[1:])
