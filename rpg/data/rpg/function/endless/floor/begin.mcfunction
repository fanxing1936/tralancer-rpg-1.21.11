scoreboard players set @s rpg_end_state 1
scoreboard players set @s rpg_end_time 0
scoreboard players operation #floor rpg_end_tmp = @s rpg_end_floor
scoreboard players operation #ordinary rpg_end_tmp = @s rpg_end_floor
scoreboard players operation #skipped rpg_end_tmp = @s rpg_end_floor
scoreboard players set #five rpg_end_tmp 5
scoreboard players operation #skipped rpg_end_tmp /= #five rpg_end_tmp
scoreboard players operation #ordinary rpg_end_tmp -= #skipped rpg_end_tmp
scoreboard players operation #deck rpg_end_tmp = #ordinary rpg_end_tmp
scoreboard players remove #deck rpg_end_tmp 1
scoreboard players set #cycle_size rpg_end_tmp 72
scoreboard players operation #deck rpg_end_tmp %= #cycle_size rpg_end_tmp
scoreboard players add #deck rpg_end_tmp 1
scoreboard players operation #cycle rpg_end_tmp = #ordinary rpg_end_tmp
scoreboard players remove #cycle rpg_end_tmp 1
scoreboard players operation #cycle rpg_end_tmp /= #cycle_size rpg_end_tmp
scoreboard players add #cycle rpg_end_tmp 1
scoreboard players operation #tier rpg_end_tmp = @s rpg_end_floor
scoreboard players add #tier rpg_end_tmp 4
scoreboard players operation #tier rpg_end_tmp /= #five rpg_end_tmp
execute if score #tier rpg_end_tmp matches 21.. run scoreboard players set #tier rpg_end_tmp 20
scoreboard players operation #mod rpg_end_tmp = @s rpg_end_floor
scoreboard players operation #mod rpg_end_tmp %= #five rpg_end_tmp
scoreboard players set #boss rpg_end_tmp 0
execute if score #mod rpg_end_tmp matches 0 run scoreboard players set #boss rpg_end_tmp 1
execute store result score #party rpg_end_tmp if entity @a[tag=rpg.end.member.current,distance=..96,gamemode=!spectator]
scoreboard players set #spawn rpg_end_tmp 3
execute if score #floor rpg_end_tmp matches 10.. run scoreboard players set #spawn rpg_end_tmp 4
execute if score #floor rpg_end_tmp matches 25.. run scoreboard players set #spawn rpg_end_tmp 5
execute if score #party rpg_end_tmp matches 2.. if score #spawn rpg_end_tmp matches ..3 run scoreboard players set #spawn rpg_end_tmp 4
execute if score #party rpg_end_tmp matches 4.. run scoreboard players set #spawn rpg_end_tmp 5
scoreboard players set @a[tag=rpg.end.member.current] rpg_end_pick 0
execute as @a[tag=rpg.end.member.current,distance=..96,gamemode=!spectator] at @s run function rpg:endless/member/apply_boons
bossbar set rpg:endless color red
execute if score #boss rpg_end_tmp matches 0 store result bossbar rpg:endless max run scoreboard players get #spawn rpg_end_tmp
execute if score #boss rpg_end_tmp matches 0 store result bossbar rpg:endless value run scoreboard players get #spawn rpg_end_tmp
execute if score #boss rpg_end_tmp matches 1 run bossbar set rpg:endless max 1
execute if score #boss rpg_end_tmp matches 1 run bossbar set rpg:endless value 1
bossbar set rpg:endless name ["",{"text":"七柱回廊｜第 ","color":"#D4AF37","bold":true,"italic":false},{"score":{"name":"#floor","objective":"rpg_end_tmp"},"color":"#FFF2A8","bold":true,"italic":false},{"text":" 层","color":"#D4AF37","bold":true,"italic":false},{"text":"　轮回 ","color":"dark_gray","bold":false,"italic":false},{"score":{"name":"#cycle","objective":"rpg_end_tmp"},"color":"#C28BE0","bold":false,"italic":false}]
title @a[tag=rpg.end.member.current,distance=..96] times 5 35 10
title @a[tag=rpg.end.member.current,distance=..96] title ["",{"text":"第 ","color":"#D4AF37","bold":false,"italic":false},{"score":{"name":"#floor","objective":"rpg_end_tmp"},"color":"#FFF2A8","bold":true,"italic":false},{"text":" 层","color":"#D4AF37","bold":false,"italic":false}]
execute if score #boss rpg_end_tmp matches 0 run title @a[tag=rpg.end.member.current,distance=..96] subtitle ["",{"text":"所罗门七十二柱 · 编队不重复","color":"#AAB4C3","bold":false,"italic":false}]
execute if score #boss rpg_end_tmp matches 1 run title @a[tag=rpg.end.member.current,distance=..96] subtitle ["",{"text":"领主层 · 七罪降临","color":"#FF665E","bold":true,"italic":false}]
execute if score #boss rpg_end_tmp matches 0 run function rpg:endless/deck/dispatch
execute if score #boss rpg_end_tmp matches 1 run function rpg:endless/boss/dispatch
function rpg:endless/enemy/refresh
