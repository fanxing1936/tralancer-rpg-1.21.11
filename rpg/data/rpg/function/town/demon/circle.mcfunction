particle minecraft:dust{color:[0.45,0.2,0.55],scale:1.6} ~ ~0.1 ~ 1.6 0.05 1.6 0 80
particle minecraft:soul_fire_flame ~ ~0.3 ~ 1.2 0.1 1.2 0 30
summon minecraft:item_display ~ ~0.05 ~ {Tags:["rpg.dm.fx"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:town/fx_rev_circle"}},transformation:{translation:[0f,0f,0f],left_rotation:[-0.7071f,0f,0f,0.7071f],right_rotation:[0f,0f,0f,1f],scale:[4f,4f,4f]}}
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..24] ~ ~ ~ 1 0.6
schedule function rpg:town/demon/fx_clear 200t
