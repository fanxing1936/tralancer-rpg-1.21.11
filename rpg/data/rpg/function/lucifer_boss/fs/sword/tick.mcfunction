scoreboard players operation #m rpg_lub = @s rpg_l2_t
scoreboard players set #k rpg_lub 4
scoreboard players operation #m rpg_lub %= #k rpg_lub
execute if score @s rpg_l2_t matches 2..30 if score #m rpg_lub matches 0 at @s run function rpg:lucifer_boss/fs/sword/warn
execute if score @s rpg_l2_t matches 24 as @e[tag=rpg.lub.sword] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{scale:[0.9f,0.9f,11f]}}
execute if score @s rpg_l2_t matches 30..90 as @e[tag=rpg.lub.sword] at @s run function rpg:lucifer_boss/fs/sword/turn
execute if score @s rpg_l2_t matches 91 run kill @e[tag=rpg.lub.sword]
execute if score @s rpg_l2_t matches 94.. run function rpg:lucifer_fight/free
