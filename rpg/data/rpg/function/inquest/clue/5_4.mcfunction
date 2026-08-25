execute if entity @s[tag=rpg.name.5] run return 0
execute if entity @s[tag=rpg.clue.5.4] run return 0
tag @s add rpg.clue.5.4
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/5
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"[罪证] ","color":"#DAA520","bold":true,"italic":false},{"text":"萨麦尔 · ","color":"#7B241C","bold":true,"italic":false},{"text":"血猎循伤而至，怒火只能追逐已经流出的血。","color":"gray","italic":false},{"text":"　进度 ","color":"dark_gray","italic":false},{"score":{"name":"@s","objective":"rpg_case5"},"color":"white","italic":false},{"text":"/3","color":"dark_gray","italic":false}]
execute if score @s rpg_case5 matches 3.. run function rpg:inquest/reveal/5
