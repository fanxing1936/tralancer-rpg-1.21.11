execute if score @s rpg_end_vital matches ..7 run scoreboard players add @s rpg_end_vital 1
effect give @s minecraft:instant_health 1 2 true
effect give @s minecraft:regeneration 12 1 true
function rpg:endless/member/apply_boons
tellraw @s ["",{"text":"[圣恩入档] ","color":"#B5D957","bold":true,"italic":false},{"text":"生存恩赐提升至 ","color":"#AAB4C3","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_end_vital"},"color":"#FFF2A8","bold":true,"italic":false},{"text":" / 8","color":"dark_gray","bold":false,"italic":false}]
