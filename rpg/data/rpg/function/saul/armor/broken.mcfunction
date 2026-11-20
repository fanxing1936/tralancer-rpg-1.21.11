# 碎甲（as/at 载体）：头盔、左臂甲换成空模型，并在原处抛出碎甲。由 add_saul_model.py 生成。
execute on passengers if entity @s[tag=rpg.slm.p.helmet] at @s run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.shard","rpg.slb.shardnew","rpg.slb.shard.helmet"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:saul/helmet"}},item_display:"none",teleport_duration:3,interpolation_duration:3,view_range:1.5f}
execute on passengers if entity @s[tag=rpg.slm.p.helmet] run data modify entity @e[type=minecraft:item_display,tag=rpg.slb.shardnew,limit=1,sort=nearest] transformation set from entity @s transformation
execute on passengers if entity @s[tag=rpg.slm.p.helmet] run data modify entity @e[type=minecraft:item_display,tag=rpg.slb.shardnew,limit=1,sort=nearest] Rotation set from entity @s Rotation
tag @e[type=minecraft:item_display,tag=rpg.slb.shardnew] remove rpg.slb.shardnew
execute on passengers if entity @s[tag=rpg.slm.p.helmet] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute on passengers if entity @s[tag=rpg.slm.p.l_pauldron] at @s run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.slb.fx","rpg.slb.shard","rpg.slb.shardnew","rpg.slb.shard.l_pauldron"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:saul/l_pauldron"}},item_display:"none",teleport_duration:3,interpolation_duration:3,view_range:1.5f}
execute on passengers if entity @s[tag=rpg.slm.p.l_pauldron] run data modify entity @e[type=minecraft:item_display,tag=rpg.slb.shardnew,limit=1,sort=nearest] transformation set from entity @s transformation
execute on passengers if entity @s[tag=rpg.slm.p.l_pauldron] run data modify entity @e[type=minecraft:item_display,tag=rpg.slb.shardnew,limit=1,sort=nearest] Rotation set from entity @s Rotation
tag @e[type=minecraft:item_display,tag=rpg.slb.shardnew] remove rpg.slb.shardnew
execute on passengers if entity @s[tag=rpg.slm.p.l_pauldron] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
