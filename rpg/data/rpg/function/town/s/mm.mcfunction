# 取样（positioned 在地表上一格）：水和岩浆不行；树干、树叶不算
execute if block ~ ~-1 ~ #rpg:town_wet run return run scoreboard players set #ok rpg_tw 0
execute if block ~ ~-1 ~ #rpg:town_clear run return 0
execute summon minecraft:marker run function rpg:town/s/mm2
