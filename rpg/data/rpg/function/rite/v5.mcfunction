# 反转的第 5 道。灼烧越来越烈，光却越来越白 —— 那是它正在翻面。
particle minecraft:flash{color:16774336} ~ ~0.9 ~ 0 0 0 0 1
particle end_rod ~ ~0.7 ~ 0.5 0.4 0.5 0.20 140
particle dust{color:[1.0,0.94,0.72],scale:2} ~ ~0.8 ~ 0.6 0.5 0.6 0.03 140
playsound minecraft:block.respawn_anchor.charge master @a[distance=..24] ~ ~ ~ 1 1.70
execute as @a[tag=rpg.inv.subject,distance=..7] run damage @s 5 minecraft:magic
execute as @a[tag=rpg.inv.subject,distance=..7] run effect give @s minecraft:slowness 3 2 true
execute as @a[tag=rpg.inv.subject,distance=..7] at @s run particle soul_fire_flame ~ ~1 ~ 0.4 0.8 0.4 0.06 40
data merge entity @s {transformation:{translation:[0f,0.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.36f,0.36f,0.36f],right_rotation:[0f,0f,0f,1f]}}
