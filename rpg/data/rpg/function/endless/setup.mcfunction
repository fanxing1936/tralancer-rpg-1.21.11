tag @s remove rpg.end.controller.new
tag @s add rpg.end.controller.current
scoreboard players set @s rpg_end_floor 1
scoreboard players set @s rpg_end_state 0
scoreboard players set @s rpg_end_time 0
scoreboard players set @s rpg_end_idle 0
tag @a[distance=..12,gamemode=!spectator] add rpg.end.member
tag @a[tag=rpg.end.member,distance=..12,gamemode=!spectator] add rpg.end.member.current
scoreboard players operation @a[tag=rpg.end.member.current,distance=..12] rpg_end_id = @s rpg_end_id
scoreboard players set @a[tag=rpg.end.member.current,distance=..12] rpg_end_power 0
scoreboard players set @a[tag=rpg.end.member.current,distance=..12] rpg_end_vital 0
scoreboard players set @a[tag=rpg.end.member.current,distance=..12] rpg_end_claim 0
execute as @a[tag=rpg.end.member.current,distance=..12] run function rpg:endless/member/clear_boons
bossbar set rpg:endless players @a[tag=rpg.end.member.current,distance=..96]
playsound minecraft:block.end_portal.spawn master @a[tag=rpg.end.member.current,distance=..12] ~ ~ ~ 0.8 0.72
title @a[tag=rpg.end.member.current,distance=..12] times 10 45 15
title @a[tag=rpg.end.member.current,distance=..12] title ["",{"text":"七柱回廊","color":"#D4AF37","bold":true,"italic":false}]
title @a[tag=rpg.end.member.current,distance=..12] subtitle ["",{"text":"无尽驱魔协议已建立","color":"#C28BE0","bold":false,"italic":false}]
tellraw @a[tag=rpg.end.member.current,distance=..12] ["",{"text":"[回廊协议] ","color":"#D4AF37","bold":true,"italic":false},{"text":"每层清除不同编队，随后选择一项个人奖励；第 5 层起每五层迎战一位罪之领主。","color":"#AAB4C3","bold":false,"italic":false}]
