# 学习 / 升级 庇护所
execute unless score @s rpg_force matches 1 unless score @s rpg_force matches 3 run return run function rpg:force/fail/say {m:"你没有圣力，学不了圣力树"}
execute unless score @s rpg_k05 matches 1.. run return run function rpg:force/fail/say {m:"先学会「祝福」"}
execute if score @s rpg_k06 matches 3.. run return run function rpg:force/fail/say {m:"「庇护所」已经满级"}
execute if score @s rpg_k06 matches 1 unless score @s rpg_sef matches 5.. run return run function rpg:force/fail/say {m:"2 级要到美丽阶（第 5 阶）"}
execute if score @s rpg_k06 matches 2 unless score @s rpg_sef matches 8.. run return run function rpg:force/fail/say {m:"3 级要到理解阶（第 8 阶）"}
scoreboard players set #c rpg_fo 1
execute if score @s rpg_k06 matches 2 run scoreboard players set #c rpg_fo 2
execute if score @s rpg_k06 matches 2 if score @s rpg_pillar matches 2 run scoreboard players set #c rpg_fo 1
execute unless score @s rpg_sp >= #c rpg_fo run return run function rpg:force/fail/say {m:"技能点不够"}
scoreboard players operation @s rpg_sp -= #c rpg_fo
scoreboard players operation @s rpg_fo_sh += #c rpg_fo
scoreboard players add @s rpg_k06 1
execute if score @s rpg_k06 matches 1 run function rpg:force/slot/auto_6
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 1.2
tellraw @s ["",{"text":"[力] ","color":"#C9A646","bold":true,"italic":false},{"text":"庇护所","color":"#FFD85A","bold":true,"italic":false},{"text":" 升到 ","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_k06"},"color":"#E6DFCF"},{"text":" 级","color":"#9C9A94","bold":false,"italic":false}]
