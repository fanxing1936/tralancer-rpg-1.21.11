# 变身演出（as/at 载体，约 6 秒）：白金光柱降下，新约玩家身上牵出光线，书碎，光柱吞没，换成首席附魔师，王冠闪光
scoreboard players add @s rpg_ub_c 1
execute if score @s rpg_ub_c matches 1..100 run particle minecraft:end_rod ~ ~2 ~ 0.4 2 0.4 0.02 6
execute if score @s rpg_ub_c matches 1 run function rpg:usurper_boss/morph/pillar
execute if score @s rpg_ub_c matches 28 as @e[tag=rpg.usb.totem] at @s run function rpg:usurper_boss/morph/totem_pop
execute if score @s rpg_ub_c matches 10..60 run scoreboard players operation #m rpg_ub = @s rpg_ub_c
scoreboard players set #k rpg_ub 10
execute if score @s rpg_ub_c matches 10..60 run scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score @s rpg_ub_c matches 10..60 if score #m rpg_ub matches 0 run function rpg:usurper_boss/morph/lines
execute if score @s rpg_ub_c matches 60 run function rpg:usurper_boss/morph/shatter
execute if score @s rpg_ub_c matches 61 run function rpg:usurper_boss/morph/pages_fly
execute if score @s rpg_ub_c matches 70 run function rpg:usurper_boss/morph/engulf
execute if score @s rpg_ub_c matches 72 run function rpg:usurper_boss/look2/swap
execute if score @s rpg_ub_c matches 95 run function rpg:usurper_boss/morph/crown
execute if score @s rpg_ub_c matches 120.. run function rpg:usurper_boss/stage/begin2
