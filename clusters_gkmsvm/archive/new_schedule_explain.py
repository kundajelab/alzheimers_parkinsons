import sys
import new_run_explain


def main(args):

    for cluster in range(int(args[1]), int(args[2])):
        new_run_explain.main([args[0], str(cluster), args[3]])


if __name__ == "__main__":
    main(sys.argv[1:])
