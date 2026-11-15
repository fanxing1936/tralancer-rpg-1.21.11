scoreboard players set @s rpg_ub_n 0
scoreboard players set #ult rpg_ub 0
execute if score @s rpg_ub matches 1 if score @s rpg_ub_h matches ..625 unless entity @s[tag=rpg.usb.u1] run scoreboard players set #ult rpg_ub 1
execute if score @s rpg_ub matches 1 if score @s rpg_ub_h matches ..375 unless entity @s[tag=rpg.usb.u2] run scoreboard players set #ult rpg_ub 2
execute if score @s rpg_ub matches 1 if score #ult rpg_ub matches 0 if score @s rpg_ub_c matches 900.. run scoreboard players set #ult rpg_ub 9
execute if score @s rpg_ub matches 2 if score @s rpg_ub_h matches ..667 unless entity @s[tag=rpg.usb.u1] run scoreboard players set #ult rpg_ub 1
execute if score @s rpg_ub matches 2 if score @s rpg_ub_h matches ..333 unless entity @s[tag=rpg.usb.u2] run scoreboard players set #ult rpg_ub 2
execute if score @s rpg_ub matches 2 if score #ult rpg_ub matches 0 if score @s rpg_ub_c matches 1200.. run scoreboard players set #ult rpg_ub 9
execute if score #ult rpg_ub matches 1.. run return run function rpg:usurper_boss/ult/pick
execute if score @s rpg_ub matches 2 if entity @s[tag=rpg.usb.auth] run return run function rpg:usurper_boss/skill/summon
execute if score @s rpg_ub matches 1 run scoreboard players operation #r rpg_ub = @s rpg_ub_k
execute if score @s rpg_ub matches 1 if score #r rpg_ub matches 0 run function rpg:usurper_boss/skill/seal
execute if score @s rpg_ub matches 1 if score #r rpg_ub matches 1 run function rpg:usurper_boss/skill/infuse
execute if score @s rpg_ub matches 1 if score #r rpg_ub matches 2 run function rpg:usurper_boss/skill/rewrite
execute if score @s rpg_ub matches 1 run scoreboard players add @s rpg_ub_k 1
execute if score @s rpg_ub matches 1 if score @s rpg_ub_k matches 3.. run scoreboard players set @s rpg_ub_k 0
execute if score @s rpg_ub matches 2 run scoreboard players operation #r rpg_ub = @s rpg_ub_k
execute if score @s rpg_ub matches 2 if score #r rpg_ub matches 0 run function rpg:usurper_boss/skill/launch
execute if score @s rpg_ub matches 2 if score #r rpg_ub matches 1 run function rpg:usurper_boss/skill/strike
execute if score @s rpg_ub matches 2 if score #r rpg_ub matches 2 run function rpg:usurper_boss/skill/slam
execute if score @s rpg_ub matches 2 run scoreboard players add @s rpg_ub_k 1
execute if score @s rpg_ub matches 2 if score @s rpg_ub_k matches 3.. run scoreboard players set @s rpg_ub_k 0
