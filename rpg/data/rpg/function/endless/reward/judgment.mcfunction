execute if score @s rpg_end_power matches ..7 run scoreboard players add @s rpg_end_power 1
function rpg:endless/member/apply_boons
tellraw @s ["",{"text":"[断罪入档] ","color":"#FF665E","bold":true,"italic":false},{"text":"输出恩赐提升至 ","color":"#AAB4C3","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_end_power"},"color":"#FFF2A8","bold":true,"italic":false},{"text":" / 8","color":"dark_gray","bold":false,"italic":false}]
