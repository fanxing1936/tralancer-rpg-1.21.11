tag @s add rpg.te.taken
data merge entity @s {Invulnerable:1b}
execute store result score #ox rpg_te run data get entity @s Pos[0]
execute store result score #oz rpg_te run data get entity @s Pos[2]
execute as @e[type=minecraft:marker,tag=rpg.tw.at.grave] if score @s rpg_tw_id = #run rpg_te at @s run tp @e[type=minecraft:villager,tag=rpg.te.taken] ^ ^ ^-14
execute as @e[type=minecraft:marker,tag=rpg.tw.at.grave] if score @s rpg_tw_id = #run rpg_te at @s run execute as @e[type=minecraft:villager,tag=rpg.te.taken] at @s run tp @s ~ ~ ~ ~ ~
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#FF6B5E","bold":true,"italic":false},{"text":"  有人被拖走了！到墓地那边把人救回来（走到他身边）。","color":"#9C9A94","bold":false,"italic":false}]
