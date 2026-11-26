item replace entity @s weapon.offhand with minecraft:air
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_stone"}] 1
clear @s minecraft:diamond[!minecraft:custom_data] 6
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 4
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
function rpg:world/bp/give_vine_whip
execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.3 0.5 0.3 0.05 60
playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 1 0.8
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.2
tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　按图纸锻成：","color":"#9C9A94","bold":false,"italic":false},{"text":"[史诗]","color":"#B85CF0","bold":true,"italic":false},{"text":"藤蔓之鞭","color":"#E6DFCF","bold":true,"italic":false}]
scoreboard players add @s rpg_pa_fg 1
