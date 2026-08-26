execute if entity @s[tag=rpg.ch1.accepted] run return run tellraw @s ["",{"text":"[第一章] 你已经在参与名单中。","color":"gray","bold":false,"italic":false}]
execute unless entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,limit=1] run return run tellraw @s ["",{"text":"[第一章] 请先抵达调查区域。","color":"#8B2500","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,limit=1,scores={rpg_ch1_stage=3..}] run return run tellraw @s ["",{"text":"[第一章] 罪仆已经封锁街区，成员名单已锁定。","color":"#8B2500","bold":false,"italic":false}]
execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,limit=1,scores={rpg_ch1_roster=4..}] run return run tellraw @s ["",{"text":"[第一章] 调查队已满（最多 4 人）。","color":"#8B2500","bold":false,"italic":false}]
tag @s add rpg.ch1.accepted
tag @s add rpg.ch1.member
tag @s remove rpg.ch1.kit.issued
tag @s remove rpg.ch1.career.confirmed
scoreboard players operation @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,sort=nearest,limit=1] rpg_ch1_id
scoreboard players operation @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,sort=nearest,limit=1] rpg_ch1_session
tag @s add rpg.ch1.roster.joiner
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,distance=..96,sort=nearest,limit=1] if score @s rpg_ch1_id = @a[tag=rpg.ch1.roster.joiner,limit=1] rpg_ch1_id run scoreboard players add @s rpg_ch1_roster 1
tag @s remove rpg.ch1.roster.joiner
execute unless items entity @s inventory.* minecraft:totem_of_undying[minecraft:custom_data~{totem_tag:1b}] run function rpg:campaign/beelzebub/give/totem
tellraw @s ["",{"text":"[参与登记] ","color":"#D4AF37","bold":true,"italic":false},{"text":"共享进度；首通奖励仍按个人档案幂等结算。","color":"gray","bold":false,"italic":false}]
