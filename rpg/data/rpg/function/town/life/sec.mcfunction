# 每秒：现实日计数、圣火庇护、死后还东西
schedule function rpg:town/life/sec 20t
scoreboard players add #sec rpg_tl 1
scoreboard players operation #day rpg_tl = #sec rpg_tl
scoreboard players operation #day rpg_tl /= #day0 rpg_tl
execute unless score #day rpg_tl = #lastday rpg_tl run function rpg:town/life/newday
execute store result score #gt rpg_tl run time query gametime
execute as @a[tag=rpg.tl.holy] run function rpg:town/life/holy
execute as @a[tag=rpg.tl.kept] at @s unless entity @s[nbt={Health:0.0f}] run function rpg:town/life/regive
execute as @a[tag=rpg.tl.ch] at @s run function rpg:town/life/scroll_tick
execute as @a[scores={rpg_tl_q3=1..}] at @s run function rpg:town/life/q/watch_tick
execute as @a[scores={rpg_tl_q4=1}] at @s run function rpg:town/life/q/wheat_tick
execute as @a[scores={rpg_tl_q6=1..}] at @s run function rpg:town/life/q/bard_tick
scoreboard players add #folkt rpg_tl 1
execute if score #folkt rpg_tl matches 30.. run function rpg:town/life/folk_scan
execute as @e[type=minecraft:interaction,tag=rpg.tl.target] run function rpg:town/life/q/target_age
# 镇上的人不交易（用户 2026-11-28「右键都会打开交易面板」）：老存档里已有的村民改成无职业、清掉交易
execute as @e[type=minecraft:villager,tag=rpg.tnpc,tag=!rpg.tl.notrade] run function rpg:town/life/notrade
