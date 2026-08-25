# 逆圣化点燃。图腾这次不往外净化 —— 它朝着那个人烧。
tag @s add rpg.totem.inv
scoreboard players add #inv_seq rpg_inv_id 1
scoreboard players operation @s rpg_inv_id = #inv_seq rpg_inv_id
tag @a[tag=!rpg.inv.subject,distance=..7,scores={rpg_taint=100}] add rpg.inv.new
execute as @a[tag=rpg.inv.new,distance=..7] run scoreboard players operation @s rpg_inv_id = #inv_seq rpg_inv_id
tag @a[tag=rpg.inv.new,distance=..7] add rpg.inv.subject
# 寿命比图腾的 200 刻多给 20 刻，防止死在圈外留下幽灵标签。
scoreboard players set @a[tag=rpg.inv.new,distance=..7] rpg_inv 220
particle minecraft:flash{color:6684672} ~ ~0.8 ~ 0 0 0 0 1
particle sculk_charge_pop ~ ~0.8 ~ 0.6 0.6 0.6 0.1 80
particle dust{color:[0.42,0.06,0.10],scale:3} ~ ~0.8 ~ 0.6 0.7 0.6 0.03 90
playsound minecraft:entity.wither.spawn master @a[distance=..40] ~ ~ ~ 1 0.7
playsound minecraft:block.end_portal.spawn master @a[distance=..40] ~ ~ ~ 0.6 1.6
title @a[tag=rpg.inv.new,distance=..7] times 10 50 20
title @a[tag=rpg.inv.new,distance=..7] title ["",{"text":"逆 圣 化","italic":false,"color":"dark_red","bold":true}]
title @a[tag=rpg.inv.new,distance=..7] subtitle ["",{"text":"负与负相乘，站住别走","italic":false,"color":"gold"}]
tag @a[tag=rpg.inv.new,distance=..7] remove rpg.inv.new
