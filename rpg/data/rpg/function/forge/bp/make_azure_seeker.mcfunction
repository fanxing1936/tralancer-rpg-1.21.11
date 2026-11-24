item replace entity @s weapon.offhand with minecraft:air
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_tear"}] 3
clear @s minecraft:netherite_ingot[!minecraft:custom_data] 2
clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 6
item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}
function rpg:world/bp/give_azure_seeker
execute at @e[type=minecraft:marker,tag=rpg.fg.fire,distance=..8,limit=1,sort=nearest] run particle minecraft:soul_fire_flame ~ ~0.6 ~ 0.3 0.5 0.3 0.05 60
playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 1 0.8
playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.2
tellraw @s ["",{"text":"[锻造]","color":"#E39745","bold":true,"italic":false},{"text":"　按图纸锻成：","color":"#9C9A94","bold":false,"italic":false},{"text":"[传说]","color":"#FFAA00","bold":true,"italic":false},{"text":"蔚蓝追寻者","color":"#E6DFCF","bold":true,"italic":false}]
