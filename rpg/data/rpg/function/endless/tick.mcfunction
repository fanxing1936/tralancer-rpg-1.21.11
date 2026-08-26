tag @e[type=minecraft:marker,tag=rpg.end.controller] remove rpg.end.controller.current
tag @s add rpg.end.controller.current
tag @a remove rpg.end.member.current
execute as @a[tag=rpg.end.member] if score @s rpg_end_id = @e[type=minecraft:marker,tag=rpg.end.controller.current,limit=1] rpg_end_id run tag @s add rpg.end.member.current
execute as @a[tag=rpg.end.member,tag=!rpg.end.member.current] run function rpg:endless/member/stale_cleanup
scoreboard players operation #floor rpg_end_tmp = @s rpg_end_floor
bossbar set rpg:endless players @a[tag=rpg.end.member.current,distance=..96,gamemode=!spectator]
scoreboard players enable @a[tag=rpg.end.member.current] rpg_end_leave
execute as @a[tag=rpg.end.member.current,scores={rpg_end_leave=1..}] run function rpg:endless/leave
execute if entity @a[tag=rpg.end.member.current,distance=..96,gamemode=!spectator,limit=1] run scoreboard players set @s rpg_end_idle 0
execute unless entity @a[tag=rpg.end.member.current,distance=..96,gamemode=!spectator,limit=1] run scoreboard players add @s rpg_end_idle 1
execute if score @s rpg_end_idle matches 6000.. run return run function rpg:endless/cleanup
execute unless entity @a[tag=rpg.end.member.current,distance=..96,gamemode=!spectator,limit=1] run return 0
execute if score @s rpg_end_state matches 0 run function rpg:endless/state/prepare
execute if score @s rpg_end_state matches 1 run function rpg:endless/state/combat
execute if score @s rpg_end_state matches 2 run function rpg:endless/state/reward
execute if score @s rpg_end_state matches 3 run function rpg:endless/state/intermission
