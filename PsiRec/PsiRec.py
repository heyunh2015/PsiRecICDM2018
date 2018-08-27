import argparse
import networkx as nx
from Support import SPPMI, evaluation, randomWalks
from Support.alsMF import MF


def parse_args():
    parser = argparse.ArgumentParser(description="Run PsiRec")

    '''Parameters of Random Walks'''
    parser.add_argument('--train_file', nargs='?',
                        default='Data/preProcessedData/toy/reviews_Toys_and_Games_5_train.interactions',
                        help='the training dataset file')

    parser.add_argument('--test_file', nargs='?',
                        default='Data/preProcessedData/toy/reviews_Toys_and_Games_5_test.interactions',
                        help='the testing dataset file (or validation dataset file)')

    parser.add_argument('--walk_length', type=int, default=80,
                        help='the length of a random walk; the default is 80.')

    parser.add_argument('--num_walks', type=int, default=10,
                        help='the number of random walks visiting each user and item; the default is 10.')

    parser.add_argument('--window_size', type=int, default=3,
                        help='the context size for sampling the indirect user-item pairs; the default is 3.')

    parser.add_argument('--user_number', type=int, default=19412,
                        help='the number of users in the dataset.')

    parser.add_argument('--item_number', type=int, default=11924,
                        help='the number of items in the dataset.')

    '''Parameters of ALS Matrix Factorization'''
    parser.add_argument('--train_epoch', type=int, default=25,
                        help='the iterations of ALS matrix factorization; the default is 25')

    parser.add_argument('--lambda_value', type=float, default=0.25,
                        help='the regularization value for ALS matrix factorization; the default is 0.25')

    parser.add_argument('--latent_factors', type=int, default=100,
                        help='the number of latent factors of ALS matrix factorization; the default is 100')

    parser.add_argument('--validation', type=int, default=0,
                        help='the Boolean variable to decide if do the validation on the validation dataset; the default is 0')

    return parser.parse_args()


def read_graph():
    G = nx.read_edgelist(args.train_file, nodetype=int, data=(('weight', float),), create_using=nx.DiGraph())
    G = G.to_undirected()
    return G

def PsiRec(args):
    nx_G = read_graph()
    G = randomWalks.Graph(nx_G)
    G.preprocess_transition_probs()
    walks = G.simulate_walks(args.num_walks, args.walk_length)

    train_R = SPPMI.calculatePMIfromWalks(walks, args.window_size, args.walk_length, args.user_number, args.item_number)

    resultMF = MF(train_R, args)

    evaluation.test_model_all(resultMF, args.train_file, args.test_file)

if __name__ == '__main__':
    args = parse_args()
    PsiRec(args)
