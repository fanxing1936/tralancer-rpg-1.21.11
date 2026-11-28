# 这一点的群系合不合适（positioned 那一点；#lmk 0 是城镇，1–3 是地标）
execute if score #lmk rpg_tw matches 0 unless biome ~ ~ ~ #rpg:town_ok run scoreboard players set #ok rpg_tw 0
execute if score #lmk rpg_tw matches 1 if score #relax rpg_tw matches 0 unless biome ~ ~ ~ #rpg:lm_1 run scoreboard players set #ok rpg_tw 0
execute if score #lmk rpg_tw matches 2 if score #relax rpg_tw matches 0 unless biome ~ ~ ~ #rpg:lm_2 run scoreboard players set #ok rpg_tw 0
execute if score #lmk rpg_tw matches 3 if score #relax rpg_tw matches 0 unless biome ~ ~ ~ #rpg:lm_3 run scoreboard players set #ok rpg_tw 0
execute if score #lmk rpg_tw matches 1 if score #relax rpg_tw matches 1.. unless biome ~ ~ ~ #rpg:lm_1 unless biome ~ ~ ~ #rpg:town_relaxed run scoreboard players set #ok rpg_tw 0
execute if score #lmk rpg_tw matches 2 if score #relax rpg_tw matches 1.. unless biome ~ ~ ~ #rpg:lm_2 unless biome ~ ~ ~ #rpg:town_relaxed run scoreboard players set #ok rpg_tw 0
execute if score #lmk rpg_tw matches 3 if score #relax rpg_tw matches 1.. unless biome ~ ~ ~ #rpg:lm_3 unless biome ~ ~ ~ #rpg:town_relaxed run scoreboard players set #ok rpg_tw 0
