import string, random

def generate_random_name(seed_name: str):
    """
    Function responsible for generating random names using Markov chain

    Args:
        seed_name (str): name of the seed file contained in name_generator directory
    Returns:
        random_name (str): string generated procedurally basing on the seed provided
    """

    letter_dict = {}
    for letter in string.ascii_letters+' ':
        letter_dict[letter] = {}
        for letter_key in string.ascii_letters+' ':
            letter_dict[letter][letter_key] = 0

    letter_dict[' '] = {}
    for letter_key in string.ascii_letters:
        letter_dict[' '][letter_key] = 0

    with open('name_generator/'+seed_name+'.txt', "r") as seed:
        for line in seed:
            first_letter = True
            line = line[:-1] + ' '
            for letter in line:
                if not first_letter and letter != '\n':
                    letter_dict[prev_letter][letter] += 1
                first_letter = False
                prev_letter = letter

    random_name = random.choice(string.ascii_uppercase)

    dictlist = []
    for key, value in letter_dict[random_name].items():
        for amount in range(value):
            dictlist.append(key)

    next_letter = random.choice(dictlist)
    random_name = random_name+next_letter

    length_counter = 0

    while next_letter != ' ' and length_counter < 12:
        length_counter += 1
        dictlist = []
        for key, value in letter_dict[random_name[len(random_name)-1]].items():
            for amount in range(value):
                dictlist.append(key)
        next_letter = random.choice(dictlist)
        random_name = random_name + next_letter

    if random.randint(0,100) < 30:
        next_letter = random.choice(string.ascii_uppercase)
        random_name += next_letter
        while next_letter != ' ' and length_counter < 12:
            length_counter += 1
            dictlist = []
            for key, value in letter_dict[random_name[len(random_name) - 1]].items():
                for amount in range(value):
                    dictlist.append(key)
            next_letter = random.choice(dictlist)
            if next_letter == ' ':
                break
            random_name = random_name + next_letter
    else:
        random_name = random_name[:-1]

    return random_name

def generate_random_seed(size: int, name: str, source_seed_name: str):
    """
    Function responsible for creating a new seed file using generate_random_name()
    basing on some source seed.
    Args:
         size (int): size of generated seed (in words/placenames)
         name (str): name of generated seed file (without extension)
         source_seed_name (str): name of source seed file (without extension)
    """
    with open('name_generator/'+name, 'w') as new_seed:
        for amount in range(size):
            new_seed.write(generate_random_name(source_seed_name)[:-1]+'\n')