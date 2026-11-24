# 退回圣力树的全部技能点
scoreboard players add @s rpg_fo_sh 0
execute if score @s rpg_fo_sh matches 1.. run tellraw @s ["",{"text":"[力] ","color":"#C9A646","bold":true,"italic":false},{"text":"圣力树的技能点退回 ","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_fo_sh"},"color":"#C9A646"}]
scoreboard players operation @s rpg_sp += @s rpg_fo_sh
scoreboard players set @s rpg_fo_sh 0
scoreboard players set @s rpg_k01 0
scoreboard players set @s rpg_k02 0
scoreboard players set @s rpg_k03 0
scoreboard players set @s rpg_k04 0
scoreboard players set @s rpg_k05 0
scoreboard players set @s rpg_k06 0
scoreboard players set @s rpg_k07 0
scoreboard players set @s rpg_k08 0
scoreboard players set @s rpg_k09 0
scoreboard players set @s rpg_k10 0
scoreboard players set @s rpg_k11 0
scoreboard players set @s rpg_k12 0
scoreboard players set @s rpg_fs_h1 0
scoreboard players set @s rpg_fs_h2 0
scoreboard players set @s rpg_fs_h3 0
