scoreboard players set #ch1_online rpg_ch1_empty 0
scoreboard players set #ch1_alive rpg_ch1_empty 0
tag @s add rpg.ch1.failure.controller
execute as @a[tag=rpg.ch1.member] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_session run scoreboard players add #ch1_online rpg_ch1_empty 1
execute as @a[tag=rpg.ch1.member,gamemode=!spectator] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_session store result score @s rpg_ch1_hp run data get entity @s Health 100
execute as @a[tag=rpg.ch1.member,gamemode=!spectator,scores={rpg_ch1_hp=1..}] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.failure.controller,limit=1] rpg_ch1_session run scoreboard players set #ch1_alive rpg_ch1_empty 1
tag @s remove rpg.ch1.failure.controller
execute if score #ch1_online rpg_ch1_empty matches 0 run scoreboard players set @s rpg_ch1_empty 0
execute if score #ch1_alive rpg_ch1_empty matches 1.. run scoreboard players set @s rpg_ch1_empty 0
execute if score #ch1_online rpg_ch1_empty matches 1.. if score #ch1_alive rpg_ch1_empty matches 0 run scoreboard players add @s rpg_ch1_empty 1
execute if score @s rpg_ch1_empty matches 1 run tellraw @a[tag=rpg.ch1.member] ["",{"text":"[检查点] ","color":"#8B2500","bold":true,"italic":false},{"text":"全体成员已死亡或进入旁观；持续 10 秒将重置本阶段。","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_ch1_empty matches 200.. run function rpg:campaign/beelzebub/roster/failure_recover
