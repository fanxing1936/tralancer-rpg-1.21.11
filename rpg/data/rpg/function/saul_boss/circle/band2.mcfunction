# 第 3 圈剑环（as/at 他）：9.5～11.5 格
tag @e[tag=rpg.unit.f,distance=9.5..11.5] add rpg.slb.hit
execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 12 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
tag @e[tag=rpg.unit,tag=rpg.slb.hit] add rpg.slb.failed
tag @e[tag=rpg.unit] remove rpg.slb.hit
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[15660282]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[23.0f,1f,23.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 12
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 16
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[14212838]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[23.0f,1f,23.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 16
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 5
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:sweep_attack ~10.50 ~1.00 ~0.00 0 0 0 0 1 force
particle minecraft:sweep_attack ~8.49 ~1.00 ~6.17 0 0 0 0 1 force
particle minecraft:sweep_attack ~3.24 ~1.00 ~9.99 0 0 0 0 1 force
particle minecraft:sweep_attack ~-3.24 ~1.00 ~9.99 0 0 0 0 1 force
particle minecraft:sweep_attack ~-8.49 ~1.00 ~6.17 0 0 0 0 1 force
particle minecraft:sweep_attack ~-10.50 ~1.00 ~0.00 0 0 0 0 1 force
particle minecraft:sweep_attack ~-8.49 ~1.00 ~-6.17 0 0 0 0 1 force
particle minecraft:sweep_attack ~-3.24 ~1.00 ~-9.99 0 0 0 0 1 force
particle minecraft:sweep_attack ~3.24 ~1.00 ~-9.99 0 0 0 0 1 force
particle minecraft:sweep_attack ~8.49 ~1.00 ~-6.17 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~11.50 ~0.40 ~0.00 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~11.11 ~0.40 ~2.98 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~9.96 ~0.40 ~5.75 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~8.13 ~0.40 ~8.13 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~5.75 ~0.40 ~9.96 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~2.98 ~0.40 ~11.11 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~0.00 ~0.40 ~11.50 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-2.98 ~0.40 ~11.11 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-5.75 ~0.40 ~9.96 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-8.13 ~0.40 ~8.13 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-9.96 ~0.40 ~5.75 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-11.11 ~0.40 ~2.98 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-11.50 ~0.40 ~0.00 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-11.11 ~0.40 ~-2.98 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-9.96 ~0.40 ~-5.75 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-8.13 ~0.40 ~-8.13 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-5.75 ~0.40 ~-9.96 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-2.98 ~0.40 ~-11.11 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-0.00 ~0.40 ~-11.50 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~2.98 ~0.40 ~-11.11 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~5.75 ~0.40 ~-9.96 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~8.13 ~0.40 ~-8.13 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~9.96 ~0.40 ~-5.75 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~11.11 ~0.40 ~-2.98 0 0 0 0 1 force
particle minecraft:crit ~10.50 ~0.80 ~0.00 0 0 0 0 1 force
particle minecraft:crit ~9.70 ~0.80 ~4.02 0 0 0 0 1 force
particle minecraft:crit ~7.42 ~0.80 ~7.42 0 0 0 0 1 force
particle minecraft:crit ~4.02 ~0.80 ~9.70 0 0 0 0 1 force
particle minecraft:crit ~0.00 ~0.80 ~10.50 0 0 0 0 1 force
particle minecraft:crit ~-4.02 ~0.80 ~9.70 0 0 0 0 1 force
particle minecraft:crit ~-7.42 ~0.80 ~7.42 0 0 0 0 1 force
particle minecraft:crit ~-9.70 ~0.80 ~4.02 0 0 0 0 1 force
particle minecraft:crit ~-10.50 ~0.80 ~0.00 0 0 0 0 1 force
particle minecraft:crit ~-9.70 ~0.80 ~-4.02 0 0 0 0 1 force
particle minecraft:crit ~-7.42 ~0.80 ~-7.42 0 0 0 0 1 force
particle minecraft:crit ~-4.02 ~0.80 ~-9.70 0 0 0 0 1 force
particle minecraft:crit ~-0.00 ~0.80 ~-10.50 0 0 0 0 1 force
particle minecraft:crit ~4.02 ~0.80 ~-9.70 0 0 0 0 1 force
particle minecraft:crit ~7.42 ~0.80 ~-7.42 0 0 0 0 1 force
particle minecraft:crit ~9.70 ~0.80 ~-4.02 0 0 0 0 1 force
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.2 1.00
