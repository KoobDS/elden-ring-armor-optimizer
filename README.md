# Elden Ring Armor Optimization
Finding the optimal armor set combinations in Elden Ring using multi-criteria optimization with various goals:

## Motivation
My goal in this study was to answer a question never before mathematically solved: What are the truly best/most optimal armor combinations in Elden Ring?
Elden Ring, the 2022 "Game of the Year" winner, alongside its 2024 expansion "Shadow of the Erdtree," has 708 different armor pieces. Most armor in the game is collected in sets of 4 pieces (corresponding to the 4 slots: Helm, Chest, Gauntlets, Legs).
However, there are no set bonuses and no inherent advantages to keeping sets 'together.' This undermines past community efforts for determing the best armor, as they have almost always solely considered full sets.
Using data orignally compiled by eldenring.wiki.fextralife.com of armor attributes viewable in game, I set out to find Elden Ring's best possible armor combinations.

## Methodology

### Data Cleaning and Feature Creation
The data, as I downloaded it, has significant flaws that I fixed in this order in clean.py:
- Most importantly, use mapping to parse and extract important features from "damage negation" and "resistance" fields, which are in key-value pair dictionary lists.
- Scale these important attributes from 0-100 where 100 is the best-in-class for a stat (as nominal values are not very relevant or co-meaningful).
- Drop armor sets not obtainable in the game (only existing in game files).
- Create "Power" columns, a major feature in this study (described below).
- Drop and rename columns for clarity.

To create the Power column, I first considered what factors were truly significant:
- Weight: higher-weight armor requires leveling Endurance, diverting levels away from other important stats
- Poise: this determines how many hits you can take without getting staggered; this is important as getting staggered can lead to hit-chaining and death
  - With 11 poise, you can withstand a projectile; with 51 poise, you can withstand most small enemies' attacks; you need 101 poise to withstand a large enemy's attack, which is unreachable through armor alone
  - With that said, I consider 51 poise to be necessary with no additonal benefit to higher values
- All damage negation stats and all infliction resistance stats, which control how much damage you negate by enemy damage type and how long it takes for negative status effects to build-up on you, respecively, but there are a total of 12 of those
- Special effects, but I will not be considering those as they are situational and only benefit certain builds

Considering this, it became clear that the features of interest were weight, poise, and a yet-to-be created synthesis of the damage negation and infliction resistance stats
To create this synthesized variable, Power, I considered the main challenge of the game and where armor matters most, remembrance (main) bosses. In Elden Ring, there are 26 main bosses, each dealing certain damage types and inflictions.
As different damage types and inflictions occur at different frequencies, it should be considered that resistance to more common damage types and inflictions is more important. I therefore compiled the below table:

| Main Boss                     | Damage Types                               | Inflictions  |
|--------------------------------|------------------------------------------|--------------|
| Godrick the Grafted           | standard, strike, fire                   |              |
| Rennala, Queen of the Full Moon | standard, magic, fire                    |              |
| Starscourge Radahn            | standard, pierce, magic                   |              |
| Regal Ancestor Spirit         | standard, magic                           |              |
| Morgott, the Omen King        | slash, pierce, holy, fire                 | bleed        |
| Astel, Naturalborn of the Void | standard, magic                           |              |
| Rykard, Lord of Blasphemy     | standard, fire, pierce                    | poison       |
| Lichdragon Fortissax          | standard, fire, lightning                 | death blight |
| Fire Giant                    | standard, strike, fire                    |              |
| Mohg, Lord of Blood           | standard, pierce, fire                    | bleed        |
| Maliketh, the Black Blade     | standard, slash, pierce, magic, holy      |              |
| Dragonlord Placidusax         | standard, fire, lightning                 |              |
| Hoarah Loux, Warrior          | standard, strike                          |              |
| Malenia, Blade of Miquella    | standard, slash, pierce, holy             | scarlet rot  |
| Elden Beast                   | standard, holy                            |              |
| Divine Beast Dancing Lion     | standard, strike, magic, lightning        | frostbite    |
| Rellana, Twin Moon Knight     | standard, slash, pierce, magic, fire      |              |
| Putrescent Knight             | standard, slash, magic                    | frostbite    |
| Commander Gaius               | standard, slash, strike, pierce, magic    |              |
| Scadutree Avatar              | standard, strike, magic, holy             | bleed        |
| Messmer the Impaler           | standard, slash, strike, pierce, fire     |              |
| Romina, Saint of the Bud      | standard, slash, strike, pierce           | scarlet rot  |
| Metyr, Mother of Fingers      | standard, slash, strike, magic, holy      |              |
| Midra, Lord of Frenzied Flame | standard, pierce, fire, holy              | madness      |
| Bayle the Dread               | standard, fire, lightning                 |              |
| Radahn, Consort of Miquella   | standard, pierce, magic, fire, holy       | bleed        |

Stats affecting infliction resistances map to the inflictions as shown below:
robustness: bleed and frostbite; immunity: scarlet rot and poison; vitality: death blight; focus: madness

Considering frequency of type/infliction amongst main bosses as a pure coefficient multiplier of importance, we get the table below:

| Type/Infliction | Importance Multiplier |
|-----------------|----------------------|
| standard        | 26                   |
| fire           | 10                   |
| magic         | 10                   |
| pierce        | 8                    |
| strike        | 8                    |
| holy         | 7                    |
| slash        | 7                    |
| robustness    | 6                    |
| lightning    | 5                    |
| immunity      | 3                    |
| focus        | 1                    |
| vitality      | 1                    |

Thus, the calculation for armor piece Power is below (remember, input features are scaled values):
Power = 26 × Physical + 10 × Fire + 10 × Magic + 8 × Pierce + 8 × Strike + 7 × Holy + 7 × Slash + 6 × Robustness + 5 × Lightning + 3 × Immunity + Focus + Vitality

### Defining and Implementing Methods






## Results

## Discussion
