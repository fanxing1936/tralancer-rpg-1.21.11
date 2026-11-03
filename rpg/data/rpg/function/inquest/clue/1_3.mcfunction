execute if entity @s[tag=rpg.name.1] run return 0
execute if entity @s[tag=rpg.clue.1.3] run return 0
tag @s add rpg.clue.1.3
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/1
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"〖罪证〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"路西法 · ","color":"#34975A","bold":false,"italic":false},{"text":"以一枚轻羽代替王冠，能使傲慢接受宣判。","color":"#9C9A94","italic":false},{"text":"　进度 ","color":"#9C9A94","italic":false},{"score":{"name":"@s","objective":"rpg_case1"},"color":"#E6DFCF","italic":false},{"text":"/3","color":"#9C9A94","italic":false}]
execute if score @s rpg_case1 matches 3.. run function rpg:inquest/reveal/1
