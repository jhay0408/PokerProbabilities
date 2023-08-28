import random

def deck_list():
    suits = ['♥', '♦', '♣', '♠']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [(rank, suit) for suit in suits for rank in ranks]
    return deck

def sim_hands(deck, hand, board = []):
    # Initialise
    wins = 0
    hands = 0
    # Update deck with my hand and board already there
    deck = [card for card in deck if card not in hand + board]
    # Find how many cards have been dealt to board
    n = len(board)

    for sim_wins in range(1000):
        # Shuffle the deck
        random.shuffle(deck)
        # Give the opponent cards
        op_hand = deck[:2]
        # Remove the op_hand from the temp deck
        sim_deck = list(set(deck) - set(op_hand))
        # Simulating boards
        board_wins = 0
        board_plays = 0
        for sim_boards in range(10000):
            # Simulate the full board
            full_board = board + sim_board(sim_deck, n)
            op_comb = op_hand + full_board
            my_comb = hand + full_board
            op_rank = eval_hand(op_comb)
            my_rank = eval_hand(my_comb)
            if my_rank > op_rank:
                board_wins += 1
            board_plays += 1
        wins += (board_wins/board_plays)
        hands += 1
    prob = wins/hands
    return prob


def sim_board(deck, n):
    num = 5-n
    random.shuffle(deck)
    board = deck[:num]
    return board


def eval_hand(hand):
    suits = ['♥', '♦', '♣', '♠']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    hand_ranks = [card[0] for card in hand]
    hand_suits = [card[1] for card in hand]

#   Check high card
    high_card_rank = (1, 0)
    for i in range(7):
        high_test = ranks.index(hand[i][0])
        if high_test > high_card_rank[1]:
            high_card_rank = (1, high_test)

#   Check pair
    pairs = []
    pair_rank = (0, 0)
    copy_hand = hand_ranks.copy()
    unique_ranks = list(set(hand_ranks))
    for i in range(len(unique_ranks)):
        if unique_ranks[i][0] in ranks:
            copy_hand.remove(unique_ranks[i][0])
    for rank in copy_hand:
        pair_test = ranks.index(rank)
        pairs.append(pair_test)
        if pair_test > pair_rank[1]:
            pair_rank = (2, pair_test)

#   Check two pair
    two_pair_rank = (0, 0, 0)
    if len(copy_hand) >= 2:
        copy_hand = sorted(copy_hand, key=lambda x: hand_ranks.index(x))
        high_pair = ranks.index(copy_hand[-1])
        second_pair = ranks.index(copy_hand[-2])
        two_pair_rank = (3, high_pair, second_pair)

    # Check trips
    trips = []
    trips_rank = (0, 0)
    for i in range(len(copy_hand)-1):
        if copy_hand[i] == copy_hand[i+1]:
            trips_test = ranks.index(copy_hand[i])
            trips.append(trips_test)
            if trips_test > trips_rank[1]:
                trips_rank = (4, ranks.index(copy_hand[i]))

    # Check straight
    straight_rank = (0, 0)
    copy_hand2 = hand_ranks.copy()
    copy_hand2 = sorted(copy_hand2, key=lambda x: ranks.index(x))
    straight_rank_test = [ranks.index(rank) for rank in copy_hand2]
    for i in range(3):
        if (straight_rank_test[i] + 1 == straight_rank_test[i+1]) and (
                straight_rank_test[i+1] + 1 == straight_rank_test[i+2]) and (
                straight_rank_test[i+2] + 1 == straight_rank_test[i+3]) and (
                straight_rank_test[i+3] + 1 == straight_rank_test[i+4]):
            straight_rank = (5, straight_rank_test[i+4])

    # Check flush
    flush_rank = (0, 0)
    flush_hand = hand.copy()
    copy_hand3 = hand_suits.copy()
    copy_hand3 = sorted(copy_hand3, key=lambda x: hand_suits.index(x))
    suit_count = [0, 0, 0, 0]
    for i in range(7):
        suit = suits.index(copy_hand3[i])
        suit_count[suit] += 1
    for i in range(4):
        if suit_count[i]>=5:
            flush_hand = [rank[0] for rank in hand if rank[1] == suits[i]]
            flush_hand.sort()
            flush_hand = flush_hand[-5:]
            flush_rank = (6, ranks.index(flush_hand[-1]))

    # Check full house
    full_house_rank = (0, 0, 0)
    if trips_rank[0] != 0 and pair_rank != 0:
        full_trips = trips_rank[1]
        pairs.sort()
        for i in range(len(pairs)):
            if pairs[i] != full_trips:
                full_house_rank = (7, full_trips, pairs[i])


    # Check quads
    quads_rank = (0, 0)
    for i in range(len(copy_hand) - 2):
        if (copy_hand[i] == copy_hand[i + 1]) and (copy_hand[i + 1] == copy_hand[i + 2]):
            quads_test = ranks.index(copy_hand[i])
            if quads_test > quads_rank[1]:
                quads_rank = (8, ranks.index(copy_hand[i]))

    # Check straight flush
    straight_flush_rank = (0, 0)
    if straight_rank[0] != 0 and flush_rank[0] != 0 and copy_hand2[0] == flush_hand[0] and straight_rank[1] == flush_rank[1]:
        straight_flush_rank = (9, straight_rank[1])

    # Check royal flush
    royal_flush_rank = (0,)
    if straight_flush_rank[1] == 12:
        royal_flush_rank = (10,)

    # Find largest
    largest = [high_card_rank, pair_rank, two_pair_rank, trips_rank, straight_rank, flush_rank, full_house_rank,
               quads_rank, straight_flush_rank, royal_flush_rank]
    largest = sorted(largest, key=lambda x: x[0])
    eval = largest[-1]
    return eval


def input_hand():
    pass


def input_board():
    pass


def run():
    pass


hand = [('5', '♠'), ('5', '♥')]
deck = deck_list()
deck = list(set(deck) - set(hand))
board = sim_board(deck, 0)
full = hand + board
print(eval_hand(full))