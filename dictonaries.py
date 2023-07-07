# Contains various dictonaries that are needed regularly throughout the course of play.

# Available starting pokemon
starting_pokemon = {
    "bulbasaur": "001",
    "charmander": "004",
    "squirtle": "007"
}


# Contains the minimum experience for each level. There are six different growth rates in pokemon, here there is one.
levelingBounds = {
    1: 0,
    2: 10,
    3: 33,
    4: 80,
    5: 156,
    6: 270,
    7: 428,
    8: 640,
    9: 911,
    10: 1250,
    11: 1663,
    12: 2160,
    13: 2746,
    14: 3430,
    15: 4218,
    16: 5120,
    17: 6141,
    18: 7290,
    19: 8573,
    20: 10000,
    21: 11576,
    22: 13310,
    23: 15208,
    24: 17280,
    25: 19531,
    26: 21970,
    27: 24603,
    28: 27440,
    29: 30486,
    30: 33750,
    31: 37238,
    32: 40960,
    33: 44921,
    34: 49130,
    35: 53593,
    36: 58320,
    37: 63316,
    38: 68590,
    39: 74148,
    40: 80000,
    41: 86151,
    42: 92610,
    43: 99383,
    44: 106480,
    45: 113906,
    46: 121670,
    47: 129778,
    48: 138240,
    49: 147061,
    50: 156250,
    51: 165813,
    52: 175760,
    53: 186096,
    54: 196830,
    55: 207968,
    56: 219520,
    57: 231491,
    58: 243890,
    59: 256723,
    60: 270000,
    61: 283726,
    62: 297910,
    63: 312558,
    64: 327680,
    65: 343281,
    66: 359370,
    67: 375953,
    68: 393040,
    69: 410636,
    70: 428750,
    71: 447388,
    72: 466560,
    73: 486271,
    74: 506530,
    75: 527343,
    76: 548720,
    77: 570666,
    78: 593190,
    79: 616298,
    80: 640000,
    81: 664301,
    82: 689210,
    83: 714733,
    84: 740880,
    85: 767656,
    86: 795070,
    87: 823128,
    88: 851840,
    89: 881211,
    90: 911250,
    91: 941963,
    92: 973360,
    93: 1005446,
    94: 1038230,
    95: 1071718,
    96: 1105920,
    97: 1140841,
    98: 1176490,
    99: 1212873,
    100: 1250000,
}

# Multipliers to the main 6 stats for each stage
# Yes, the fractions could be simplified, but this makes it clearer how the rates were determines
statStageMultiplers = {
    -6: 2/8,
    -5: 2/7,
    -4: 2/6,
    -3: 2/5,
    -2: 2/4,
    -1: 2/3,
    0: 2/2,
    1: 3/2,
    2: 4/2,
    3: 5/2,
    4: 6/2,
    5: 7/2,
    6: 8/2
}

# Multiplier to evasion and acccuracy based on stage
battleStageMultipliers = {
    -6: 3/9,
    -5: 3/8,
    -4: 3/7,
    -3: 3/6,
    -2: 3/5,
    -1: 3/4,
    0: 3/3,
    1: 4/3,
    2: 5/3,
    3: 6/3,
    4: 7/3,
    5: 8/3,
    6: 9/3
}

critStages = {
    0: 24,
    1: 8,
    2: 4,
    3: 3,
    4: 2
}

# Integer IDs for the different types from the PokeAPI and itsJavi datasets
type_IDs = {
    1: "Normal",
    2: "Fighting",
    3: "Flying",
    4: "Poison",
    5: "Ground",
    6: "Rock",
    7: "Bug",
    8: "Ghost",
    9: "Steel",
    10: "Fire",
    11: "Water",
    12: "Grass",
    13: "Electric",
    14: "Psychic",
    15: "Ice",
    16: "Dragon",
    17: "Dark",
    18: "Fairy"
}

type_matching = {
    # StrongTowards, WeakTowards, StrongAgainst, WeakAgainst, Nullifies, NullifiedBy
    # (2x damage to),(0.5x damages to),(0.5x damage from),(2x damage from),(0x damage from),(0x damage to)
    "": [[],[],[],[],[],[]],
    "Normal": [[],["Rock","Steel"],[],["Fighting"],[],["Ghost"]],
    "Fire": [["Grass","Ice","Bug","Steel"],["Fire","Water","Rock","Dragon"],["Fire","Grass","Ice","Bug","Steel","Fairy"],["Water","Ground","Rock"],[],[]],
    "Water": [["Fire","Ground","Rock"],["Water","Grass","Dragon"],["Fire","Water","Ice","Steel"],["Grass","Electric"],[],[]],
    "Grass": [["Water","Ground","Rock"],["Fire","Grass","Poison","Flying","Bug","Steel"],["Water","Grass","Electric","Ground"],["Fire","Ice","Poison","Flying","Bug"],[],[]],
    "Electric": [["Water","Flying"],["Grass","Electric","Dragon"],["Electric","Flying","Steel"],["Ground"],[],["Ground"]],
    "Ice": [["Grass","Ground","Flying","Dragon"],["Fire","Water","Ice","Steel"],["Ice"],["Fire","Fighting","Rock","Steel"],[],[]],
    "Fighting": [["Normal","Ice","Rock","Dark","Steel"],["Posion","Flying","Psychic","Bug","Fairy"],["Bug","Rock","Dark"],["Flying","Psychic","Fairy"],[],["Ghost"]],
    "Poison": [["Grass","Fairy"],["Poison","Ground","Rock","Ghost"],["Grass","Fighting","Posion","Bug","Fairy"],["Ground","Psychic"],[],["Steel"]],
    "Ground": [["Fire","Electric","Poison","Rock","Steel"],["Grass", "Bug"],["Posion","Rock"],["Water","Grass","Ice"],["Electric"],["Flying"]],
    "Flying": [["Grass","Fighting","Psychic"],["Electric","Bug","Steel"],["Grass","Fighting","Bug"],["Electric","Ice","Rock"],["Ground"],[]],
    "Psychic": [["Fighting","Poison"],["Psychic","Steel"],["Fighting","Psychic"],["Bug","Ghost","Dark"],[],["Dark"]],
    "Bug": [["Grass","Psychic","Dark"],["Fire","Fighting","Poison","Flying","Ghost","Steel","Fairy"],["Grass","Fighting","Ground"],["Fire","Flying","Rock"],[],[]],
    "Rock": [["Fire","Ice","Flying","Bug"],["Fighting","Ground","Steel"],["Normal","Fire","Poison","Flying"],["Water","Grass","Fighting","Ground","Steel"],[],[]],
    "Ghost": [["Psychic","Ghost"],["Dark"],["Poison","Bug"],["Ghost","Dark"],["Normal","Fighting"],["Normal"]],
    "Dragon": [["Dragon"],["Steel"],["Fire","Water","Grass","Electric"],["Ice","Dragon","Fairy"],[],["Fairy"]],
    "Dark": [["Posion","Ghost"],["Fighting","Dark","Fairy"],["Ghost","Dark"],["Fighting","Bug","Fairy"],["Psychic"],[]],
    "Steel": [["Ice","Rock","Fairy"],["Fire","Water","Electric","Steel"],["Normal","Grass","Ice","Flying","Psychic","Bug","Rock","Dragon","Steel","Fairy"],["Fire","Fighting","Ground"],["Poison"],[]],
    "Fairy": [["Fighting","Dragon","Dark"],["Fire","Posion","Steel"],["Fighting","Bug","Dark"],["Poison","Steel"],["Dragon"],[]],
}

# Natures raise one stat by 10% and also lowers another by 10%
# HP is never affected by a pokemons nature,so there are 25 to reflect every combination of ATK,DEF,SP.A,SP.D,SPE
# Name, Raise Stat, Lowers Stat
pokemon_natures = {
    1: ["Hardy",2,2],
    2: ["Bold",2,3],
    3: ["Modest",2,4],
    4: ["Calm",2,5],
    5: ["Timid",2,6],
    6: ["Lonely",3,2],
    7: ["Docile",3,3],
    8: ["Mild",3,4],
    9: ["Gentle",3,5],
    10: ["Hasty",3,6,],
    11: ["Adamant",4,2],
    12: ["Impish",4,3],
    13: ["Bashful",4,4],
    14: ["Careful",4,5],
    15: ["Rash",5,4],
    16: ["Jolly",4,6],
    17: ["Naughty",5,2],
    18: ["Lax",5,3],
    19: ["Quirky",5,5],
    20: ["Naive",5,6],
    21: ["Brave",6,2],
    22: ["Relaxed",6,3],
    23: ["Quiet",6,4],
    24: ["Sassy",6,5],
    25: ["Serious",6,6]
}

move_damage_classes = {
    1: "Status",
    2: "Physical",
    3: "Special"
}

move_meta_catergories = {
    0: "damage",
    1: "ailment",
    2: "net-good-stats",
    3: "heal",
    4: "damage+ailment",
    5: "swagger",
    6: "damage+lower",
    7: "damage+raise",
    8: "damage+heal",
    9: "ohko",
    10: "whole-field-effect",
    11: "field-effect",
    12: "force-switch",
    13: "unique"
}

# Why there are gaps I don't know, this is just the data that I could find
move_meta_ailment_name = {
    "-1": "????",
    "0": "None",
    "1": "Paralysis",
    "2": "Sleep",
    "3": "Freeze",
    "4": "Burn",
    "5": "Poison",
    "6": "Confusion",
    "7": "Attraction",
    "8": "Trap",
    "9": "Nightmare",
    "12": "Torment",
    "13": "Disable",
    "14": "Yawn",
    "15": "Heal Block",
    "17": "No type immuntity",
    "18": "Leech Seed",
    "19": "Embargo",
    "20": "Perish Song",
    "21": "Ingrain",
    "24": "Silence",
    "42": "Tar Shot"
}

# Gives the relative likelihood of a given enocounter types happening
# Trainer, Wild Pokemon, Find Item
encounter_type_ratios = {
    "Index": ["Trainer","Wild","Item"],
    "Route 001": [5,5,1]
}

# Base cash payout for average team level mod 10
base_payout = {
    0: 200,
    1: 400,
    2: 600,
    3: 900,
    4: 1200,
    5: 1600,
    6: 2000,
    7: 2500,
    8: 3000,
    9: 3600,
    10: 4200,
}

# How much health and what defbuffswill be cured by a given medicine
medicine_stats = {
    "Potion": [20,0,"None"],
    "Super Potion": [60,0,"None"],
    "Hyper Potion": [120,0,"None"],
    "Max Potion": [1000,0,"None"],
    "Full Restore": [1000,0,"Poison","Burning","Frozen","Sleep","Paralysis"],

    "Antidote": [0,0,"Poison"],
    "Burn Heal": [0,0,"Burning"],
    "Ice Heal": [0,0,"Frozen"],
    "Awakening": [0,0,"Sleep"],
    "Paralyze Heal": [0,0,"Paralysis"],
    "Full Heal": [0,0,"Poison","Burning","Frozen","Sleep","Paralysis"],

    "Ether": [],
    "Max Ether":[]
}

# How much each type of pokeball increases 
pokeball_catch_multiplier = {
    "Poke Ball": 1,
    "Great Ball": 1.5,
    "Ultra Ball": 2,
    "Master Ball": 255,
}
