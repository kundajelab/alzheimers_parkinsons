import sys
import run_ism


def main(args):

    for cluster in range(int(args[0]), int(args[1])):
        run_ism.main([str(cluster), args[2]])


if __name__ == "__main__":
    main(sys.argv[1:])
