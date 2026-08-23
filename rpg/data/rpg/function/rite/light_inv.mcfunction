# 逆圣化点燃。图腾这次不往外净化 —— 它朝着那个人烧。
tag @s add rpg.totem.inv
tag @a[distance=..7,scores={rpg_taint=100}] add rpg.inv.subject
# 配一份寿命。受术者若死在圈外，没人来摘这个标签 ——
# 留着它会干扰下一场仪式的判定。
scoreboard players set @a[tag=rpg.inv.subject,distance=..7] rpg_inv 220
particle minecraft:flash{color:6684672} ~ ~0.8 ~ 0 0 0 0 1
particle sculk_charge_pop ~ ~0.8 ~ 0.6 0.6 0.6 0.1 80
particle dust{color:[0.42,0.06,0.10],scale:3} ~ ~0.8 ~ 0.6 0.7 0.6 0.03 90
playsound minecraft:entity.wither.spawn master @a[distance=..40] ~ ~ ~ 1 0.7
playsound minecraft:block.end_portal.spawn master @a[distance=..40] ~ ~ ~ 0.6 1.6
title @a[tag=rpg.inv.subject] times 10 50 20
title @a[tag=rpg.inv.subject] title ["",{"text":"逆 圣 化","italic":false,"color":"dark_red","bold":true}]
title @a[tag=rpg.inv.subject] subtitle ["",{"text":"负与负相乘，站住别走","italic":false,"color":"gold"}]
