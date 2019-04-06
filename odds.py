import random
import itertools

"""
The purpose of this script is to produce a list of useful data regarding the 
possible combinations in a 52 card deck. The product is a text file containing 
lists of tuples which hold the length of combinations, and the total number of 
combinations. The data can be used to determine the probability of reaching a 
certain value in blackjack. For instance if the value of a hand in blackjack 
is 9, this data can be used to determine the probability of increases that value 
by 12.

Created by: Barry Nailor, April of 2019
"""

######################
#Global Declarations
combinations = list()
filtered_combinations = list()
optomized_combos = list()
combo_dict = dict()
perm_dict = dict()
fperm_len_dict = dict()

for i in range(20):
    combinations.append(list())
    optomized_combos.append(list())


#######################

"""
*****************       GetCombinations      *****************
GetCombinations is a recursive function that takes a list of numbers and 
a target sum. It determines all of the possible combinations in the list 
that can be summed to equal the target value. The combination is then added
to the combinations list. It returns if the combination already exists without
adding it to the list again. The number of duplicate combinations is calculated
and added to combo_dict under the key of the combination. 
"""
def GetCombinations(numbers, target, partial = []):
    if len(partial) > 7: #i dont want any combinations longer than 7 cards
        return 

    if(partial.__contains__('A')): #to account for aces having two values 
        
        a_as_1 = [x if x != 'A' else 1 for x in partial]     
        temp_list = a_as_1.copy()
        temp_list.remove(1)
        temp_list.append(11)
        a_as_11 = temp_list
            
        sum_with_11 = sum(a_as_11)
        sum_with_1 = sum(a_as_1)

        if(sum_with_11 == target):
            if str(a_as_11) in combo_dict:
                return
            duplicates = GetDuplicateCombos(partial)
            combinations[target].append(a_as_11)
            combo_dict[str(a_as_11)] = duplicates
            #no return since there may be another combo with ace as 1 
        if(sum_with_1 == target):
            if str(a_as_1) in combo_dict:
                return
            duplicates = GetDuplicateCombos(partial)
            combinations[target].append(a_as_1)
            combo_dict[str(a_as_1)] = duplicates
            return
        if(sum_with_1 > target):
            return
    else:
        s = sum(partial)
        if s == target:
            if str(partial) in combo_dict:
                return
            duplicates = GetDuplicateCombos(partial)
            combinations[target].append(partial)
            combo_dict[str(partial)] = duplicates
            return

        if s > target:
            return

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i + 1:]
        GetCombinations(remaining, target, partial + [n])



"""
***************     GetDuplicateCombos     *****************
GetDuplicateCombos function takes a single combination and returns the
number of identical combinations that can be achieved using a 52 card deck
"""
def GetDuplicateCombos(combination):
    set_of_combination = set(combination) #get unique values from combo
    count_list = list()
    ten_count = 0
    for value in set_of_combination:
        if value == 10:
            ten_count = 1
        else:
            count_list.append(combination.count(value)) #record the count of each unique value
    total_count = 1
    for x in count_list: 
        if x == 1:
            total_count *= 4 # one for each suit
        if x == 2:
            total_count *= 6 # ex. [2,2] can be represented by [2S,2C,2H,2D] = 6 combos
        if x == 3:
            total_count *= 4 # ex [2,2,2] with 4 suits can have 4 combos
        # if 4 total_count * 1 ... 
    if ten_count != 0:
        total_count *= 16 # one for each ten in the deck
    return total_count


"""
*****************       GetEveryPossibleOrder       *****************
The GetEveryPossibleOrder generator takes a list of combinations. Each element
in the list contains multiple combinations. It has no return value, instead 
it gets every possible permutation of a combination and adds them to the perm_dict
under the key of the original combination. It yields after all of the combinations
in an element of the main list have been calculate. This was done to save memory.
Once this function yields, the perm_dict goes thru the rest of the functions to 
finish processing and then clears the perm_dict so doesn't become overlogged with 
millions of combinations at once. 
"""
def GetEveryPossibleOrder(combos):    
    for combo in combos:
        for each_combo in combo:
            for permutation in itertools.permutations(each_combo, len(each_combo)):
                if str(each_combo) in perm_dict:
                    perm_dict[str(each_combo)].append(list(permutation))
                else:
                    perm_dict[str(each_combo)] = list()
                    perm_dict[str(each_combo)].append(list(permutation))
        yield
        


"""
*****************       FilterCombinations      *****************
FilterCombinations function takes a combination dictionary, with each permutation
for a combination listed under a key which is the original combination. It has no return value.
It filters out the combos in which the result would be obtained
With an Ace representing 11 prior to the other results being added 
For example in finding combinations for 11, both (1,10) and (10,1)
would be returned but in practice if a played draws an ace first then
they wouldn't draw another card, so this function removes (1,10) as insignificant.
Combos that have not been filtered are added to the filtered_combinations list. 
The number of permutations that are not filtered from a given key are tracked with
the occurances variable. That number is added to fperm_len_dict under the key of the
original combination to track how many permutations each key has after being filtered.
"""
def  FilterCombinations(combos, target):
    for key in combos:
        occurances = 0
        if len(combos[key]) > 1:
            for i in combos[key]:
                subtotal = 0
                filtered = False
                if(not i.__contains__(1)):
                    filtered_combinations.append(i)
                    occurances += 1
                    continue
                temp_list = i.copy()
                first_ace_index = temp_list.index(1)
                temp_list[first_ace_index] = 11
                for z in range(len(temp_list)-1):
                    subtotal += temp_list[z]
                    if(subtotal == target):
                        filtered = True
                if(not filtered):
                    filtered_combinations.append(i)
                    occurances += 1
            fperm_len_dict[key] = occurances
        else:
            occurances = 1
            filtered_combinations.append(combos[key][0])
            fperm_len_dict[key] = occurances



"""
*****************       OptomizeCombos       *****************
This function uses the combo_dict, which holds the number produced by the 
GetDuplicateCombos function for each original combination. And the fperm_len_dict,
which holds the number of permutations, after being filtered, for each original 
combination. It optomizes the list by only focusing on the length of the combination
rather than the combination itself. All of the combinations of the same length for
a given target are grouped together and ultimately stored in a tuple of =
(length of combination, all of the possible duplicates and permutations)
It adds these tuples to the optomize_combos list for each target, which is later used
to write all of the information to combinations.txt
"""
def OptomizeCombos(fcombos,target):
    for i in range(1,8):
        occurances = 0
        for combo in fcombos:
            if not len(combo) == i:
                continue
            if combo in combinations[target]:
                occurances += combo_dict[str(combo)] * fperm_len_dict[str(combo)]
        optomized_combos[target].append((i,occurances))




def WriteToFile():
    with open("combinations.txt", 'w') as f:
        for combo in optomized_combos:
            f.write(str(combo) + '\n')



#######################################
#Main Start


suit = [1,2,3,4,5,6,7,8,9,10,10,10,10]
deck = suit * 4
deck.sort()
deck = [card if card != 1 else 'A' for card in deck]


for h in range(1,20):
    GetCombinations(deck, h)
print("Get Combinations complete.")


target = 0 # tracks the target
for i in GetEveryPossibleOrder(combinations):
    # print(f"Target: {target}")
    print("Get Every Possible Order complete.")
    FilterCombinations(perm_dict, target)
    print("Filter Combinations complete.")
    OptomizeCombos(combinations[target],target)
    print("Optomize Combos complete")
    perm_dict = dict()
    fperm_len_dict = dict()
    filtered_combinations = list()
    target += 1 

WriteToFile()
print("All complete")


#Main End
#######################################


    