scoreboard players operation #r rpg_pact = @s rpg_pact_s1
scoreboard players remove #r rpg_pact 1
scoreboard players operation #q rpg_pact = #r rpg_pact
scoreboard players operation #r rpg_pact %= #five rpg_pact
scoreboard players operation #q rpg_pact /= #five rpg_pact
scoreboard players add #q rpg_pact 1
scoreboard players set #same rpg_pact 0
execute if score #q rpg_pact = @s rpg_pact run scoreboard players set #same rpg_pact 1
execute if score #r rpg_pact matches 0 if score #same rpg_pact matches 0 run function rpg:pact/seal/m1_1_0
execute if score #r rpg_pact matches 0 if score #same rpg_pact matches 1 run function rpg:pact/seal/m1_1_1
execute if score #r rpg_pact matches 1 if score #same rpg_pact matches 0 run function rpg:pact/seal/m1_2_0
execute if score #r rpg_pact matches 1 if score #same rpg_pact matches 1 run function rpg:pact/seal/m1_2_1
execute if score #r rpg_pact matches 2 if score #same rpg_pact matches 0 run function rpg:pact/seal/m1_3_0
execute if score #r rpg_pact matches 2 if score #same rpg_pact matches 1 run function rpg:pact/seal/m1_3_1
execute if score #r rpg_pact matches 4 if score #same rpg_pact matches 0 run function rpg:pact/seal/m1_5_0
execute if score #r rpg_pact matches 4 if score #same rpg_pact matches 1 run function rpg:pact/seal/m1_5_1
execute if score #r rpg_pact matches 2 run tag @s add rpg.pact.s3
execute if score #r rpg_pact matches 3 run tag @s add rpg.pact.s4
execute if score #r rpg_pact matches 3 run tag @s add rpg.pact.onhit
execute if score #r rpg_pact matches 4 run tag @s add rpg.pact.s5
execute if score #r rpg_pact matches 4 run tag @s add rpg.pact.onhit
