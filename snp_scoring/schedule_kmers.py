import sys
import score_kmers


def main(args):

    for cluster in range(int(args[0]), int(args[1])):
        score_kmers.main([str(cluster), args[2]])


if __name__ == "__main__":
    main(sys.argv[1:])
