$scoreboard players set #tn rpg_te $(n)
execute if score #tn rpg_te matches 1 run function rpg:town/ev/g/t1
execute if score #tn rpg_te matches 2 run function rpg:town/ev/g/t2
execute if score #tn rpg_te matches 3 run function rpg:town/ev/g/t3
particle minecraft:dust{color:[0.35,0.42,0.12],scale:1.4} ~ ~0.8 ~ 0.5 0.5 0.5 0 30
kill @e[type=minecraft:item_display,tag=rpg.tw.ev,distance=..1.5]
kill @s
execute if score #found rpg_te matches 3 run function rpg:town/ev/g/named
