# 退回魔力树的全部技能点
scoreboard players add @s rpg_fo_sm 0
execute if score @s rpg_fo_sm matches 1.. run tellraw @s ["",{"text":"[力] ","color":"#C9A646","bold":true,"italic":false},{"text":"魔力树的技能点退回 ","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_fo_sm"},"color":"#C9A646"}]
scoreboard players operation @s rpg_sp += @s rpg_fo_sm
scoreboard players set @s rpg_fo_sm 0
scoreboard players set @s rpg_k13 0
scoreboard players set @s rpg_k14 0
scoreboard players set @s rpg_k15 0
scoreboard players set @s rpg_k16 0
scoreboard players set @s rpg_k17 0
scoreboard players set @s rpg_k18 0
scoreboard players set @s rpg_k19 0
scoreboard players set @s rpg_k20 0
scoreboard players set @s rpg_k21 0
scoreboard players set @s rpg_k22 0
scoreboard players set @s rpg_k23 0
scoreboard players set @s rpg_k24 0
scoreboard players set @s rpg_fs_m1 0
scoreboard players set @s rpg_fs_m2 0
scoreboard players set @s rpg_fs_m3 0
