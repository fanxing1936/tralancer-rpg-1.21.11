execute if entity @s[tag=rpg.name.4] run return 0
execute if entity @s[tag=rpg.clue.4.2] run return 0
tag @s add rpg.clue.4.2
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/4
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"[罪证] ","color":"#DAA520","bold":true,"italic":false},{"text":"别西卜 · ","color":"#5A6B1E","bold":false,"italic":false},{"text":"吞噬与蝇群都从永不满足的胃中孵化。","color":"gray","italic":false},{"text":"　进度 ","color":"dark_gray","italic":false},{"score":{"name":"@s","objective":"rpg_case4"},"color":"white","italic":false},{"text":"/3","color":"dark_gray","italic":false}]
execute if score @s rpg_case4 matches 3.. run function rpg:inquest/reveal/4
