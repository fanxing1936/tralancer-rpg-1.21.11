execute if entity @s[tag=rpg.name.5] run return 0
execute if entity @s[tag=rpg.clue.5.5] run return 0
tag @s add rpg.clue.5.5
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/5
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"[罪证] ","color":"#DAA520","bold":true,"italic":false},{"text":"萨麦尔 · ","color":"#7B241C","bold":false,"italic":false},{"text":"怒潮把众人推远，暴露了暴怒无法承受接近。","color":"gray","italic":false},{"text":"　进度 ","color":"dark_gray","italic":false},{"score":{"name":"@s","objective":"rpg_case5"},"color":"white","italic":false},{"text":"/3","color":"dark_gray","italic":false}]
execute if score @s rpg_case5 matches 3.. run function rpg:inquest/reveal/5
