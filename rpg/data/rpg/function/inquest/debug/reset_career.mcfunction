scoreboard players set @s rpg_ex_xp 0
scoreboard players set @s rpg_ex_lvl 1
scoreboard players set @s rpg_ex_path 0
scoreboard players set @s rpg_ex_seen 0
tag @s remove rpg.ex.claim2
tag @s remove rpg.ex.claim3
tag @s remove rpg.ex.claim4
tag @s remove rpg.ex.claim5
tellraw @s ["",{"text":"[驱魔师档案] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"职业阅历、路线与领取记录已重置。","color":"gray","italic":false}]
