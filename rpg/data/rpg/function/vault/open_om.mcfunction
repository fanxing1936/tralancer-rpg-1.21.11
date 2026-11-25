# 开灾厄宝库（as 触发星，at 宝库底面中心）
kill @s
# 不在宝库旁边（被人捡走又丢出来之类）：直接给一份勇者奖
execute unless block ~ ~ ~ minecraft:vault run return run loot spawn ~ ~1 ~ loot rpg:vault/t1
setblock ~ ~ ~ minecraft:air
setblock ~ ~ ~ minecraft:vault[ominous=true]{config:{loot_table:"rpg:loot/loot_ominous",override_loot_table_to_display:"rpg:vault/decoy",key_item:{id:"minecraft:ominous_trial_key",count:1,components:{"minecraft:custom_name":["",{"text":"[传说]","color":"#FFAA00","bold":1b,"italic":0b},{"text":"灾厄试炼之匙","color":"#FFFFFF","bold":0b,"italic":0b}],"minecraft:lore":[["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}],["",{"text":"开辟神启的","color":"gray","bold":0b,"italic":0b},{"text":"[钥匙]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"唤出传奇的","color":"gray","bold":0b,"italic":0b},{"text":"[宝具]","color":"#FFAA00","bold":1b,"italic":0b}],["",{"text":"+------------------+","color":"#FFFFFF","bold":0b,"italic":0b}]]}},activation_range:0.0d,deactivation_range:0.0d}}
scoreboard players add #id rpg_vt 1
tag @a remove rpg.vt.op
tag @p[distance=..8,gamemode=!spectator] add rpg.vt.op
scoreboard players operation @a[tag=rpg.vt.op] rpg_vt_id = #id rpg_vt
summon minecraft:marker ~ ~1.55 ~ {Tags:["rpg.vt.c","rpg.vt.new"]}
execute as @e[type=minecraft:marker,tag=rpg.vt.new] at @s run function rpg:vault/begin_1
