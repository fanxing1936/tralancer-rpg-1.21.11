# 一条圆弧（at 圆心）：地上亮一圈，圆心标记带一根飞行的肋骨
$summon minecraft:marker ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.orb","rpg.mkb.orb$(side)"]}
$scoreboard players set @e[tag=rpg.mkb.orb$(side)] rpg_mk_life 152
$scoreboard players set @e[tag=rpg.mkb.orb$(side)] rpg_mk_kd 0
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_r","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[21f,1f,21f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 150
scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 0
tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
$summon minecraft:item_display ~ ~1.2 ~ {Tags:["rpg.mkb.fx","rpg.mkb.rib","rpg.mkb.rib$(side)"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_boss/rib"}},item_display:"none",brightness:{sky:15,block:15},teleport_duration:1,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[-0.7071068f,0f,0f,0.7071068f],scale:[2f,2f,2f],right_rotation:[0f,0f,0f,1f]}}
$scoreboard players set @e[tag=rpg.mkb.rib$(side)] rpg_mk_life 152
$scoreboard players set @e[tag=rpg.mkb.rib$(side)] rpg_mk_kd 0
