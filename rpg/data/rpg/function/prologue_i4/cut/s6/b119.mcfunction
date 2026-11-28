execute in rpg:armageddon_4 positioned 0 81.6 0 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7.5f,7.5f,7.5f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_4 positioned 0 81.6 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
execute in rpg:armageddon_4 positioned 0 81.6 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 32
execute in rpg:armageddon_4 positioned 0 81.6 0 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute in rpg:armageddon_4 positioned 0 81.6 0 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_4 positioned 0 81.6 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 10
execute in rpg:armageddon_4 positioned 0 81.6 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 7
execute in rpg:armageddon_4 positioned 0 81.6 0 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute in rpg:armageddon_4 positioned 0 81.06 0 run summon minecraft:item_display ~ ~0.06 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/shockh_0","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[7f,1f,7f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_4 positioned 0 81.06 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 16
execute in rpg:armageddon_4 positioned 0 81.06 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 40
execute in rpg:armageddon_4 positioned 0 81.06 0 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute in rpg:armageddon_4 positioned 1.5 81.5 1 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,5f,5f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_4 positioned 1.5 81.5 1 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 12
execute in rpg:armageddon_4 positioned 1.5 81.5 1 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 36
execute in rpg:armageddon_4 positioned 1.5 81.5 1 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute in rpg:armageddon_4 positioned -1.5 81.5 -1 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,5f,5f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_4 positioned -1.5 81.5 -1 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 12
execute in rpg:armageddon_4 positioned -1.5 81.5 -1 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 36
execute in rpg:armageddon_4 positioned -1.5 81.5 -1 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
particle minecraft:block{block_state:"minecraft:polished_blackstone_bricks"} 0 81.2 0 1.5 0.3 1.5 0.2 120
execute as @a[tag=rpg.pri4] at @s run playsound minecraft:entity.generic.explode master @s ~ ~ ~ 1.2 0.5
execute as @a[tag=rpg.pri4] at @s run playsound minecraft:entity.iron_golem.damage master @s ~ ~ ~ 1.2 0.5
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.beelzebub,distance=0..] run function rpg:prologue_beelzebub/anim/enter/roll_b
execute in rpg:armageddon_4 run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.beelzebub,distance=0..] -3.6 81 -5.2 -16.7 0
