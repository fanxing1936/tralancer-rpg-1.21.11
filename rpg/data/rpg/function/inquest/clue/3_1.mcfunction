execute if entity @s[tag=rpg.name.3] run return 0
execute if entity @s[tag=rpg.clue.3.1] run return 0
tag @s add rpg.clue.3.1
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/3
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"[罪证] ","color":"#DAA520","bold":true,"italic":false},{"text":"亚巴顿 · ","color":"#6A6A70","bold":false,"italic":false},{"text":"收割只偏爱已经停滞的灵魂。","color":"gray","italic":false},{"text":"　进度 ","color":"dark_gray","italic":false},{"score":{"name":"@s","objective":"rpg_case3"},"color":"white","italic":false},{"text":"/3","color":"dark_gray","italic":false}]
execute if score @s rpg_case3 matches 3.. run function rpg:inquest/reveal/3
