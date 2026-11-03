execute if entity @s[tag=rpg.name.7] run return 0
execute if entity @s[tag=rpg.clue.7.1] run return 0
tag @s add rpg.clue.7.1
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/7
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"〖罪证〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"玛门 · ","color":"#D19C26","bold":false,"italic":false},{"text":"点金给每条命标价，夺财则拒绝无主之物。","color":"#9C9A94","italic":false},{"text":"　进度 ","color":"#9C9A94","italic":false},{"score":{"name":"@s","objective":"rpg_case7"},"color":"#E6DFCF","italic":false},{"text":"/3","color":"#9C9A94","italic":false}]
execute if score @s rpg_case7 matches 3.. run function rpg:inquest/reveal/7
