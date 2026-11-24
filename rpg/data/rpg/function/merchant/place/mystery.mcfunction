# 管理员：在脚下放一位Mystery Merchant（货里的契约书随机一柱）
execute store result score #pp rpg_ev run random value 1..7
execute if score #pp rpg_ev matches 1 run function rpg:merchant/spawn_mystery_1
execute if score #pp rpg_ev matches 2 run function rpg:merchant/spawn_mystery_2
execute if score #pp rpg_ev matches 3 run function rpg:merchant/spawn_mystery_3
execute if score #pp rpg_ev matches 4 run function rpg:merchant/spawn_mystery_4
execute if score #pp rpg_ev matches 5 run function rpg:merchant/spawn_mystery_5
execute if score #pp rpg_ev matches 6 run function rpg:merchant/spawn_mystery_6
execute if score #pp rpg_ev matches 7 run function rpg:merchant/spawn_mystery_7
playsound minecraft:entity.villager.celebrate neutral @a[distance=..16] ~ ~ ~ 1 1
