import random

suits = ['♥', '♦', '♣', '♠']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


def deck_list():
    deck = [(rank, suit) for suit in suits for rank in ranks]
    return deck


def sim_hands(hand):
    # Initialise
    wins = 0
    hands = 0
    deck = deck_list()
    board = hand[2:]
    hand = hand[0:2]
    # Update deck with my hand and board already there
    deck = [card for card in deck if card not in hand + board]
    # Find how many cards have been dealt to board
    n = len(board)
    if n < 3:
        no_boards = 500
        no_hands = 100
    else:
        no_hands = 500
        no_boards = 100

    for sim_wins in range(no_hands):
        # Shuffle the deck
        random.shuffle(deck)
        # Give the opponent cards
        op_hand = deck[:2]
        # Remove the op_hand from the temp deck
        sim_deck = list(set(deck) - set(op_hand))
        # Simulating boards
        board_wins = 0
        board_plays = 0
        for sim_boards in range(no_boards):
            # Simulate the full board
            full_board = board + sim_board(sim_deck, n)
            op_comb = op_hand + full_board
            my_comb = hand + full_board
            op_rank = eval_hand(op_comb)
            my_rank = eval_hand(my_comb)
            if my_rank[0] > op_rank[0]:
                board_wins += 1
            elif my_rank[0] == op_rank[0]:
                try:
                    if my_rank[1] > op_rank[1]:
                        board_wins += 1
                    elif my_rank[1] == op_rank[1]:
                        try:
                            my_sec = my_rank[2]
                            op_sec = op_rank[2]
                            if my_sec > op_sec:
                                board_wins += 1
                            elif my_sec == op_sec:
                                board_wins += 0.5
                        except IndexError:
                            board_wins += 0.5
                except IndexError:
                    board_wins += 0.5
                    pass
            #         both have a royal flush
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
        if unique_ranks[i] in ranks:
            copy_hand.remove(unique_ranks[i])
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
    copy_hand2 = sorted(list(set(copy_hand2)), key=lambda x: ranks.index(x))
    straight_rank_test = [ranks.index(rank) for rank in copy_hand2]
    for i in range(len(straight_rank_test)-4):
        if (straight_rank_test[i] + 1 == straight_rank_test[i+1]) and (
                straight_rank_test[i+1] + 1 == straight_rank_test[i+2]) and (
                straight_rank_test[i+2] + 1 == straight_rank_test[i+3]) and (
                straight_rank_test[i+3] + 1 == straight_rank_test[i+4]):
            straight_rank = (5, straight_rank_test[i+4])
            index = straight_rank_test.index(straight_rank[1])
            copy_hand2a = copy_hand2[index-4:index+1]

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
        if suit_count[i] >= 5:
            flush_hand = [rank[0] for rank in hand if rank[1] == suits[i]]
            flush_hand = sorted(flush_hand, key=lambda x: ranks.index(x))
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
    if straight_rank[0] != 0 and flush_rank[0] != 0 and copy_hand2a[0] == flush_hand[0] and straight_rank[1] == flush_rank[1]:
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


def input_hand(hand_string):
    rank_strings = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suit_strings = ['H', 'D', 'C', 'S']
    hand_string = hand_string.split(', ')
    for i in range(len(hand_string)):
        if len(hand_string[i]) == 3:
            hand_string[i] = [hand_string[i][0:2], hand_string[i][2]]
        else:
            hand_string[i] = list(hand_string[i])
    card1_value = hand_string[0][0]
    card1_suit = hand_string[0][1]
    card2_value = hand_string[1][0]
    card2_suit = hand_string[1][1]
    hand = [(ranks[rank_strings.index(card1_value)], suits[suit_strings.index(card1_suit)]),
            (ranks[rank_strings.index(card2_value)], suits[suit_strings.index(card2_suit)])]
    return hand


def input_board(board_string):
    rank_strings = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suit_strings = ['H', 'D', 'C', 'S']
    board_string = board_string.split(', ')
    board = []
    for i in range(len(board_string)):
        if len(board_string[i]) == 3:
            board_string[i] = [board_string[i][0:2], board_string[i][2]]
        else:
            board_string[i] = list(board_string[i])
    for i in range(len(board_string)):
        board.append((ranks[rank_strings.index(board_string[i][0])],
                      suits[suit_strings.index(board_string[i][1])]))
    return board


def full_convert(full):
    board = []
    for i in range(len(full)):
        if len(full[i]) == 3:
            full[i] = [full[i][0:2], full[i][2]]
        else:
            full[i] = list(full[i])
    for i in range(len(full)):
        board.append((full[i][0], full[i][1]))
    return board


def run():
    # Get initial deck
    deck = deck_list()
    # Get input hand
    hand_string = input("Input Hand: ")
    hand = input_hand(hand_string)
    # Run prob
    pre_flop_prob = sim_hands(hand)
    print(f'Probability of hand winning: {pre_flop_prob*100:.2f}%')
    # Get flop cards
    board_string = input("Input Flop: ")
    board = input_board(board_string)
    hand += board
    # Run prob
    flop_prob = sim_hands(hand)
    print(f'Probability of hand winning: {flop_prob * 100:.2f}%')
    # Get turn
    board_string = input("Input Turn: ")
    hand += input_board(board_string)
    # Run prob
    turn_prob = sim_hands(hand)
    print(f'Probability of hand winning: {turn_prob * 100:.2f}%')
    # Get river
    board_string = input("Input River: ")
    hand += input_board(board_string)
    # Run prob
    river_prob = sim_hands(hand)
    print(f'Probability of hand winning: {river_prob * 100:.2f}%')


# TODO Extensions: Plot graph of sets that occur for a given hand
# TODO List hands that beat the given hand
