scoreboard players set @s rpg_ex_kind 0
function rpg:inquest/stability/hit20
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14]
tellraw @a[distance=..16,gamemode=!spectator] ["",{"text":"[嫉妒得逞] ","color":"dark_red","bold":true,"italic":false},{"text":"妒影带走了法阵的一部分力量。","color":"gray","italic":false}]
