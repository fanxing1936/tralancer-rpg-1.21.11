# 募兵旗 —— 由 rpg:item/squad_hire 在长按右键时触发。
advancement revoke @s only rpg:item/squad_hire
execute if entity @s[scores={rpg_sq_t=1..}] run return 0
scoreboard players set @s rpg_sq_t 10

# 头一次募兵先领一个队伍编号。多人下认人全靠它，不靠"最近的玩家"。
execute unless score @s rpg_squad = @s rpg_squad run function rpg:squad/enroll

# 数一数现有几个人
scoreboard players operation #sq rpg_squad = @s rpg_squad
scoreboard players set #cnt rpg_squad 0
execute as @e[type=minecraft:husk,tag=rpg.squad] if score @s rpg_squad = #sq rpg_squad run scoreboard players add #cnt rpg_squad 1
scoreboard players operation @s rpg_sq_n = #cnt rpg_squad
execute if entity @s[scores={rpg_sq_n=4..}] run return run function rpg:squad/full

# 手上有多少钱。`clear ... 0` 是**只数不拿**，原版惯用写法。
execute store result score @s rpg_sq_have run clear @s minecraft:raw_gold[minecraft:custom_data~{currency_tag:1b}] 0
execute if entity @s[scores={rpg_sq_n=0}] run function rpg:squad/hire0
execute if entity @s[scores={rpg_sq_n=1}] run function rpg:squad/hire1
execute if entity @s[scores={rpg_sq_n=2}] run function rpg:squad/hire2
execute if entity @s[scores={rpg_sq_n=3}] run function rpg:squad/hire3
