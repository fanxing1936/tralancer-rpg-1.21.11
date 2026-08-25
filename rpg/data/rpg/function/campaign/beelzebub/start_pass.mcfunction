execute if entity @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] run return run tellraw @s ["",{"text":"[第一章] 已有调查实例；请从档案选择加入。","color":"#8B2500","bold":false,"italic":false}]
scoreboard players add #next rpg_ch1_id 1
execute if score #next rpg_ch1_id matches ..0 run scoreboard players set #next rpg_ch1_id 1
summon minecraft:marker ~ ~ ~ {Tags:["rpg.ch1.controller","rpg.ch1.anchor","rpg.ch1.scene","rpg.ch1.new"]}
execute if score @s rpg_ch1_yaw matches 0 run data merge entity @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] {Rotation:[0f,0f]}
execute if score @s rpg_ch1_yaw matches 1 run data merge entity @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] {Rotation:[90f,0f]}
execute if score @s rpg_ch1_yaw matches 2 run data merge entity @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] {Rotation:[-90f,0f]}
execute if score @s rpg_ch1_yaw matches 3 run data merge entity @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] {Rotation:[180f,0f]}
scoreboard players operation @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_id = #next rpg_ch1_id
execute store result score @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_session run random value 1..2147483647
scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_stage 0
scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_time 0
scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_obj 0
scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_roster 1
scoreboard players set @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] rpg_ch1_empty 0
tag @e[type=minecraft:marker,tag=rpg.ch1.new,sort=nearest,limit=1,distance=..2] remove rpg.ch1.new
tag @s add rpg.ch1.accepted
tag @s add rpg.ch1.member
tag @s add rpg.ch1.party
tag @s add rpg.ch1.current
tag @s add rpg.ch1.host
tag @s remove rpg.ch1.kit.issued
tag @s remove rpg.ch1.career.confirmed
scoreboard players operation @s rpg_ch1_id = #next rpg_ch1_id
scoreboard players operation @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_session
execute if score @s rpg_ch1_done matches 1.. run scoreboard players set @s rpg_ch1_replay 1
bossbar add rpg:chapter1 ["",{"text":"第一章 · 空缺者","color":"#B8A98B","bold":true,"italic":false}]
bossbar set rpg:chapter1 max 100
bossbar set rpg:chapter1 color yellow
bossbar set rpg:chapter1 style progress
execute as @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] at @s run function rpg:campaign/beelzebub/stage/0_enter
