import sys
import run_gkmexplain


def main(args):

    for cluster in range(int(args[0]), int(args[1])):
        new_run_explain.main([str(cluster), args[2]])


if __name__ == "__main__":
    main(sys.argv[1:])
