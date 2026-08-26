execute if entity @s[tag=rpg.name.1] run return 0
execute if entity @s[tag=rpg.clue.1.3] run return 0
tag @s add rpg.clue.1.3
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/1
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"[罪证] ","color":"#DAA520","bold":true,"italic":false},{"text":"路西法 · ","color":"#00491C","bold":false,"italic":false},{"text":"以一枚轻羽代替王冠，能使傲慢接受宣判。","color":"gray","italic":false},{"text":"　进度 ","color":"dark_gray","italic":false},{"score":{"name":"@s","objective":"rpg_case1"},"color":"white","italic":false},{"text":"/3","color":"dark_gray","italic":false}]
execute if score @s rpg_case1 matches 3.. run function rpg:inquest/reveal/1
