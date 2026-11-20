# 第 1 圈剑环（as/at 他）：1.0～3.5 格
tag @e[tag=rpg.unit.f,distance=1.0..3.5] add rpg.slb.hit
execute as @e[tag=rpg.unit,tag=rpg.slb.hit] run damage @s 12 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1]
tag @e[tag=rpg.unit,tag=rpg.slb.hit] add rpg.slb.failed
tag @e[tag=rpg.unit] remove rpg.slb.hit
summon minecraft:item_display ~ ~0.08 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/ring","minecraft:custom_model_data":{colors:[15660282]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.0f,1f,7.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 12
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 16
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:usurper_fx/shock_0","minecraft:custom_model_data":{colors:[14212838]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.0f,1f,7.0f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 16
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 5
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
particle minecraft:sweep_attack ~2.25 ~1.00 ~0.00 0 0 0 0 1 force
particle minecraft:sweep_attack ~1.82 ~1.00 ~1.32 0 0 0 0 1 force
particle minecraft:sweep_attack ~0.70 ~1.00 ~2.14 0 0 0 0 1 force
particle minecraft:sweep_attack ~-0.70 ~1.00 ~2.14 0 0 0 0 1 force
particle minecraft:sweep_attack ~-1.82 ~1.00 ~1.32 0 0 0 0 1 force
particle minecraft:sweep_attack ~-2.25 ~1.00 ~0.00 0 0 0 0 1 force
particle minecraft:sweep_attack ~-1.82 ~1.00 ~-1.32 0 0 0 0 1 force
particle minecraft:sweep_attack ~-0.70 ~1.00 ~-2.14 0 0 0 0 1 force
particle minecraft:sweep_attack ~0.70 ~1.00 ~-2.14 0 0 0 0 1 force
particle minecraft:sweep_attack ~1.82 ~1.00 ~-1.32 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~3.50 ~0.40 ~0.00 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~3.38 ~0.40 ~0.91 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~3.03 ~0.40 ~1.75 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~2.47 ~0.40 ~2.47 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~1.75 ~0.40 ~3.03 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~0.91 ~0.40 ~3.38 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~0.00 ~0.40 ~3.50 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-0.91 ~0.40 ~3.38 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-1.75 ~0.40 ~3.03 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-2.47 ~0.40 ~2.47 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-3.03 ~0.40 ~1.75 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-3.38 ~0.40 ~0.91 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-3.50 ~0.40 ~0.00 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-3.38 ~0.40 ~-0.91 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-3.03 ~0.40 ~-1.75 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-2.47 ~0.40 ~-2.47 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-1.75 ~0.40 ~-3.03 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-0.91 ~0.40 ~-3.38 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~-0.00 ~0.40 ~-3.50 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~0.91 ~0.40 ~-3.38 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~1.75 ~0.40 ~-3.03 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~2.47 ~0.40 ~-2.47 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~3.03 ~0.40 ~-1.75 0 0 0 0 1 force
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~3.38 ~0.40 ~-0.91 0 0 0 0 1 force
particle minecraft:crit ~2.25 ~0.80 ~0.00 0 0 0 0 1 force
particle minecraft:crit ~2.08 ~0.80 ~0.86 0 0 0 0 1 force
particle minecraft:crit ~1.59 ~0.80 ~1.59 0 0 0 0 1 force
particle minecraft:crit ~0.86 ~0.80 ~2.08 0 0 0 0 1 force
particle minecraft:crit ~0.00 ~0.80 ~2.25 0 0 0 0 1 force
particle minecraft:crit ~-0.86 ~0.80 ~2.08 0 0 0 0 1 force
particle minecraft:crit ~-1.59 ~0.80 ~1.59 0 0 0 0 1 force
particle minecraft:crit ~-2.08 ~0.80 ~0.86 0 0 0 0 1 force
particle minecraft:crit ~-2.25 ~0.80 ~0.00 0 0 0 0 1 force
particle minecraft:crit ~-2.08 ~0.80 ~-0.86 0 0 0 0 1 force
particle minecraft:crit ~-1.59 ~0.80 ~-1.59 0 0 0 0 1 force
particle minecraft:crit ~-0.86 ~0.80 ~-2.08 0 0 0 0 1 force
particle minecraft:crit ~-0.00 ~0.80 ~-2.25 0 0 0 0 1 force
particle minecraft:crit ~0.86 ~0.80 ~-2.08 0 0 0 0 1 force
particle minecraft:crit ~1.59 ~0.80 ~-1.59 0 0 0 0 1 force
particle minecraft:crit ~2.08 ~0.80 ~-0.86 0 0 0 0 1 force
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 1.2 1.40
