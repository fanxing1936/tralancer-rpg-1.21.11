# 再核对：靠近灵魂火、材料够，才扣
scoreboard players operation #me rpg_fg = @s rpg_fg_id
scoreboard players set #fire rpg_fg 0
execute as @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8] if score @s rpg_fg_eo = #me rpg_fg at @s if block ~ ~ ~ #rpg:forge/soul_fire run scoreboard players set #fire rpg_fg 1
execute if score #fire rpg_fg matches 0 run return run tellraw @s ["",{"text":"[炼药]","color":"#8FD0C0","bold":true,"italic":false},{"text":"　离灵魂火太远了，靠近些","color":"#C04A3C","bold":false,"italic":false}]
execute if score @s rpg_fg_arg matches 0 run return run function rpg:alc/make_0
execute if score @s rpg_fg_arg matches 1 run return run function rpg:alc/make_1
execute if score @s rpg_fg_arg matches 2 run return run function rpg:alc/make_2
execute if score @s rpg_fg_arg matches 3 run return run function rpg:alc/make_3
execute if score @s rpg_fg_arg matches 4 run return run function rpg:alc/make_4
execute if score @s rpg_fg_arg matches 5 run return run function rpg:alc/make_5
execute if score @s rpg_fg_arg matches 6 run return run function rpg:alc/make_6
execute if score @s rpg_fg_arg matches 7 run return run function rpg:alc/make_7
execute if score @s rpg_fg_arg matches 8 run return run function rpg:alc/make_8
execute if score @s rpg_fg_arg matches 9 run return run function rpg:alc/make_9
execute if score @s rpg_fg_arg matches 10 run return run function rpg:alc/make_10
execute if score @s rpg_fg_arg matches 11 run return run function rpg:alc/make_11
execute if score @s rpg_fg_arg matches 12 run return run function rpg:alc/make_12
execute if score @s rpg_fg_arg matches 13 run return run function rpg:alc/make_13
execute if score @s rpg_fg_arg matches 14 run return run function rpg:alc/make_14
execute if score @s rpg_fg_arg matches 15 run return run function rpg:alc/make_15
execute if score @s rpg_fg_arg matches 16 run return run function rpg:alc/make_16
execute if score @s rpg_fg_arg matches 17 run return run function rpg:alc/make_17
execute if score @s rpg_fg_arg matches 18 run return run function rpg:alc/make_18
execute if score @s rpg_fg_arg matches 19 run return run function rpg:alc/make_19
execute if score @s rpg_fg_arg matches 20 run return run function rpg:alc/make_20
execute if score @s rpg_fg_arg matches 21 run return run function rpg:alc/make_21
execute if score @s rpg_fg_arg matches 22 run return run function rpg:alc/make_22
execute if score @s rpg_fg_arg matches 23 run return run function rpg:alc/make_23
execute if score @s rpg_fg_arg matches 24 run return run function rpg:alc/make_24
execute if score @s rpg_fg_arg matches 25 run return run function rpg:alc/make_25
execute if score @s rpg_fg_arg matches 26 run return run function rpg:alc/make_26
execute if score @s rpg_fg_arg matches 27 run return run function rpg:alc/make_27
execute if score @s rpg_fg_arg matches 28 run return run function rpg:alc/make_28
execute if score @s rpg_fg_arg matches 29 run return run function rpg:alc/make_29
execute if score @s rpg_fg_arg matches 30 run return run function rpg:alc/make_30
execute if score @s rpg_fg_arg matches 31 run return run function rpg:alc/make_31
