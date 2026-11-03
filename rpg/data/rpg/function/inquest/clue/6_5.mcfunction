execute if entity @s[tag=rpg.name.6] run return 0
execute if entity @s[tag=rpg.clue.6.5] run return 0
tag @s add rpg.clue.6.5
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/6
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"〖罪证〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"贝利尔 · ","color":"#A057A9","bold":false,"italic":false},{"text":"欲障遮住真形，因此最惧怕清醒的映照。","color":"#9C9A94","italic":false},{"text":"　进度 ","color":"#9C9A94","italic":false},{"score":{"name":"@s","objective":"rpg_case6"},"color":"#E6DFCF","italic":false},{"text":"/3","color":"#9C9A94","italic":false}]
execute if score @s rpg_case6 matches 3.. run function rpg:inquest/reveal/6
