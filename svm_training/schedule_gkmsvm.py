import sys
import run_gkmsvm


def main(args):

    for cluster in range(1, 25):
        run_gkmsvm.main([str(cluster), 'all', 40])


if __name__ == "__main__":
    main()
