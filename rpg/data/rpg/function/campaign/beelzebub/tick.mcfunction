tag @a[tag=rpg.ch1.party] remove rpg.ch1.party
tag @a[tag=rpg.ch1.accepted] remove rpg.ch1.current
execute as @a[tag=rpg.ch1.member,distance=..96,gamemode=!spectator] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id if score @s rpg_ch1_session = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_session run tag @s add rpg.ch1.party
execute as @a[tag=rpg.ch1.party] run tag @s add rpg.ch1.current
bossbar set rpg:chapter1 players @a[tag=rpg.ch1.current,distance=..128]
execute if score @s rpg_ch1_stage matches 3 run function rpg:campaign/beelzebub/roster/failure_tick
execute if score @s rpg_ch1_stage matches 7 run function rpg:campaign/beelzebub/roster/failure_tick
execute unless entity @a[tag=rpg.ch1.current,distance=..128,gamemode=!spectator] as @e[type=minecraft:vindicator,tag=rpg.ch1.boss] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run scoreboard players add @s rpg_fall 1
execute as @e[type=minecraft:vindicator,tag=rpg.ch1.boss,scores={rpg_fall=12001..}] run scoreboard players set @s rpg_fall 12000
execute unless entity @a[tag=rpg.ch1.current,distance=..96,gamemode=!spectator] run return 0
scoreboard players add @s rpg_ch1_time 1
execute if score @s rpg_ch1_time matches 24001.. run scoreboard players set @s rpg_ch1_time 24000
execute if score @s rpg_ch1_stage matches 0 run function rpg:campaign/beelzebub/stage/0_tick
execute if score @s rpg_ch1_stage matches 1 run function rpg:campaign/beelzebub/stage/1_tick
execute if score @s rpg_ch1_stage matches 2 run function rpg:campaign/beelzebub/stage/2_tick
execute if score @s rpg_ch1_stage matches 3 run function rpg:campaign/beelzebub/stage/3_tick
execute if score @s rpg_ch1_stage matches 4 run function rpg:campaign/beelzebub/stage/4_tick
execute if score @s rpg_ch1_stage matches 5 run function rpg:campaign/beelzebub/stage/5_tick
execute if score @s rpg_ch1_stage matches 6 run function rpg:campaign/beelzebub/stage/6_tick
execute if score @s rpg_ch1_stage matches 7 run function rpg:campaign/beelzebub/stage/7_tick
execute if score @s rpg_ch1_stage matches 8 run function rpg:campaign/beelzebub/stage/8_tick
execute if score @s rpg_ch1_stage matches 9 run function rpg:campaign/beelzebub/stage/9_tick
execute if score @s rpg_ch1_stage matches 10 run function rpg:campaign/beelzebub/stage/10_tick
