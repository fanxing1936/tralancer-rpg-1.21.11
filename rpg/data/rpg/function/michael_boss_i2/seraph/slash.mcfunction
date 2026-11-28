execute store result score #r rpg_mk_i2 run random value 1..6
execute if score #r rpg_mk_i2 matches 1 run function rpg:michael/anim/enter/rib_slash1
execute if score #r rpg_mk_i2 matches 2 run function rpg:michael/anim/enter/rib_slash2
execute if score #r rpg_mk_i2 matches 3 run function rpg:michael/anim/enter/rib_slash3
execute if score #r rpg_mk_i2 matches 4 run function rpg:michael/anim/enter/rib_slash4
execute if score #r rpg_mk_i2 matches 5 run function rpg:michael/anim/enter/rib_slash5
execute if score #r rpg_mk_i2 matches 6 run function rpg:michael/anim/enter/rib_slash6
execute facing entity @e[tag=rpg.unit.f,distance=..6,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
tag @e[tag=rpg.unit.f,distance=..3.5] add rpg.mkb.hit
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit,distance=0..] run damage @s 5 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
execute if score #stage rpg_mk_i2 matches 2 as @e[tag=rpg.unit,tag=rpg.mkb.hit,distance=0..] run function rpg:michael_boss_i2/flame/add
tag @e[tag=rpg.unit,distance=0..] remove rpg.mkb.hit
summon minecraft:text_display ^ ^1.3 ^1.5 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 30
tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
