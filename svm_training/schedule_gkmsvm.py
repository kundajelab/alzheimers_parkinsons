import sys
import run_gkmsvm


def main(args):

    for cluster in range(int(args[0]), int(args[1]) + 1):
        run_gkmsvm.main([str(cluster), 'all', 5])


if __name__ == "__main__":
    main(sys.argv[1:])

