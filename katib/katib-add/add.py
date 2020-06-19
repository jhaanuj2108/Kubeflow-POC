import argparse


def add(args):
    val1=args.val1
    val2=args.val2
    total=val1+val2
    print("total={}".format(total))
    

if __name__ == '__main__':

    # This python script will be our MAIN entrypoint, hence parsing here the command line arguments.
    parser = argparse.ArgumentParser(description="Training my_model()",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--val1', type=float, default=1,
                    help='value1')
    parser.add_argument('--val2', type=float, default=1,
                    help='value 2')


    args = parser.parse_args()
    add(args)
