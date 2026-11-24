execute store result score #r rpg_q_st run random value 1..7
execute if score #r rpg_q_st matches 1 run function rpg:inquest/give/core1
execute if score #r rpg_q_st matches 2 run function rpg:inquest/give/core2
execute if score #r rpg_q_st matches 3 run function rpg:inquest/give/core3
execute if score #r rpg_q_st matches 4 run function rpg:inquest/give/core4
execute if score #r rpg_q_st matches 5 run function rpg:inquest/give/core5
execute if score #r rpg_q_st matches 6 run function rpg:inquest/give/core6
execute if score #r rpg_q_st matches 7 run function rpg:inquest/give/core7
