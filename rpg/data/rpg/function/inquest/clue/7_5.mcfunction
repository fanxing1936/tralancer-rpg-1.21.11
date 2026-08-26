execute if entity @s[tag=rpg.name.7] run return 0
execute if entity @s[tag=rpg.clue.7.5] run return 0
tag @s add rpg.clue.7.5
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/7
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"[罪证] ","color":"#DAA520","bold":true,"italic":false},{"text":"玛门 · ","color":"#B7950B","bold":false,"italic":false},{"text":"金牢困住的是占有者，而非被主动放下的黄金。","color":"gray","italic":false},{"text":"　进度 ","color":"dark_gray","italic":false},{"score":{"name":"@s","objective":"rpg_case7"},"color":"white","italic":false},{"text":"/3","color":"dark_gray","italic":false}]
execute if score @s rpg_case7 matches 3.. run function rpg:inquest/reveal/7
