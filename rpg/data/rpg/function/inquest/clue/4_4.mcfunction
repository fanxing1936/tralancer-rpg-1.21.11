execute if entity @s[tag=rpg.name.4] run return 0
execute if entity @s[tag=rpg.clue.4.4] run return 0
tag @s add rpg.clue.4.4
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/4
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"〖罪证〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"别西卜 · ","color":"#8CA83D","bold":false,"italic":false},{"text":"腐宴把宾客也算作菜肴，却惧怕已经坏死的食物。","color":"#9C9A94","italic":false},{"text":"　进度 ","color":"#9C9A94","italic":false},{"score":{"name":"@s","objective":"rpg_case4"},"color":"#E6DFCF","italic":false},{"text":"/3","color":"#9C9A94","italic":false}]
execute if score @s rpg_case4 matches 3.. run function rpg:inquest/reveal/4
