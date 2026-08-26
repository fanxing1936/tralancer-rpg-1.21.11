execute if entity @s[tag=rpg.name.2] run return 0
execute if entity @s[tag=rpg.clue.2.4] run return 0
tag @s add rpg.clue.2.4
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/2
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"[罪证] ","color":"#DAA520","bold":true,"italic":false},{"text":"利维坦 · ","color":"#1B4F72","bold":false,"italic":false},{"text":"逆潮不断重写远近，因为嫉妒从不接受平等的位置。","color":"gray","italic":false},{"text":"　进度 ","color":"dark_gray","italic":false},{"score":{"name":"@s","objective":"rpg_case2"},"color":"white","italic":false},{"text":"/3","color":"dark_gray","italic":false}]
execute if score @s rpg_case2 matches 3.. run function rpg:inquest/reveal/2
