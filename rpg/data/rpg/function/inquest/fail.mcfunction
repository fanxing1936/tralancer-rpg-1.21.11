tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"[仪式失败] ","color":"dark_red","bold":true,"italic":false},{"text":"法阵失去约束，裁决被迫进入消灭步骤。","color":"gray","italic":false}]
function rpg:inquest/outcome/eliminate_boss
kill @e[type=minecraft:armor_stand,tag=rpg.counter.name,distance=..12]
kill @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14]
