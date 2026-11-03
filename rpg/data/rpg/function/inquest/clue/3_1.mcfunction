execute if entity @s[tag=rpg.name.3] run return 0
execute if entity @s[tag=rpg.clue.3.1] run return 0
tag @s add rpg.clue.3.1
scoreboard players add @s rpg_ex_xp 4
function rpg:inquest/recount/3
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.45
tellraw @s ["",{"text":"〖罪证〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"亚巴顿 · ","color":"#8C90A1","bold":false,"italic":false},{"text":"收割只偏爱已经停滞的灵魂。","color":"#9C9A94","italic":false},{"text":"　进度 ","color":"#9C9A94","italic":false},{"score":{"name":"@s","objective":"rpg_case3"},"color":"#E6DFCF","italic":false},{"text":"/3","color":"#9C9A94","italic":false}]
execute if score @s rpg_case3 matches 3.. run function rpg:inquest/reveal/3
