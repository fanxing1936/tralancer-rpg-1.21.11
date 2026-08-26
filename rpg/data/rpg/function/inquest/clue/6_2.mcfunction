execute if entity @s[tag=rpg.name.6] run return 0
execute if entity @s[tag=rpg.clue.6.2] run return 0
tag @s add rpg.clue.6.2
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/6
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"[罪证] ","color":"#DAA520","bold":true,"italic":false},{"text":"贝利尔 · ","color":"#5B2C6F","bold":false,"italic":false},{"text":"迷乱与献身都依靠被篡改的感官。","color":"gray","italic":false},{"text":"　进度 ","color":"dark_gray","italic":false},{"score":{"name":"@s","objective":"rpg_case6"},"color":"white","italic":false},{"text":"/3","color":"dark_gray","italic":false}]
execute if score @s rpg_case6 matches 3.. run function rpg:inquest/reveal/6
