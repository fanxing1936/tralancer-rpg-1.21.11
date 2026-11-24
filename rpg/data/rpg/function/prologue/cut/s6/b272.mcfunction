execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.belial] run function rpg:prologue/cut/kill_actor
execute in rpg:armageddon positioned -8.39 81.6 1.17 run summon minecraft:text_display ~ ~1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon positioned -8.39 81.6 1.17 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_life 12
execute in rpg:armageddon positioned -8.39 81.6 1.17 run scoreboard players set @e[tag=rpg.mkb.fxnew] rpg_mk_kd 36
execute in rpg:armageddon positioned -8.39 81.6 1.17 run tag @e[tag=rpg.mkb.fxnew] remove rpg.mkb.fxnew
particle minecraft:large_smoke -8.39 82 1.17 0.5 0.8 0.5 0.02 30
particle minecraft:witch -8.39 82 1.17 0.6 1 0.6 0 40
execute in rpg:armageddon run summon minecraft:item_display -8.39 82.2 1.17 {Tags:["rpg.pr.wisp","rpg.pr.ent"],billboard:"center",teleport_duration:1,brightness:{sky:15,block:15},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:prologue_fx/smoke_0"}},item_display:"fixed",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[3.4f,3.4f,3.4f]}}
execute as @a[tag=rpg.pr] at @s run playsound minecraft:entity.phantom.flap master @s ~ ~ ~ 1.2 0.6
execute as @a[tag=rpg.pr] at @s run playsound minecraft:entity.breeze.whirl master @s ~ ~ ~ 1 0.7
