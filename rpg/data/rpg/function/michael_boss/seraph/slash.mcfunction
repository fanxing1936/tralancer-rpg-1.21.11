execute store result score #r rpg_mk run random value 1..6
execute if score #r rpg_mk matches 1 run function rpg:michael/anim/enter/rib_slash1
execute if score #r rpg_mk matches 2 run function rpg:michael/anim/enter/rib_slash2
execute if score #r rpg_mk matches 3 run function rpg:michael/anim/enter/rib_slash3
execute if score #r rpg_mk matches 4 run function rpg:michael/anim/enter/rib_slash4
execute if score #r rpg_mk matches 5 run function rpg:michael/anim/enter/rib_slash5
execute if score #r rpg_mk matches 6 run function rpg:michael/anim/enter/rib_slash6
execute facing entity @e[tag=rpg.unit.f,distance=..6,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
tag @e[tag=rpg.unit.f,distance=..3.5] add rpg.mkb.hit
execute as @e[tag=rpg.unit,tag=rpg.mkb.hit,predicate=!rpg:in_prologue] run damage @s 5 minecraft:mob_attack by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,predicate=!rpg:in_prologue]
execute if score #stage rpg_mk matches 2 as @e[tag=rpg.unit,tag=rpg.mkb.hit,predicate=!rpg:in_prologue] run function rpg:michael_boss/flame/add
tag @e[tag=rpg.unit,predicate=!rpg:in_prologue] remove rpg.mkb.hit
summon minecraft:text_display ^ ^1.3 ^1.5 {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,3f,3f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_life 12
scoreboard players set @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] rpg_mk_kd 30
tag @e[tag=rpg.mkb.fxnew,predicate=!rpg:in_prologue] remove rpg.mkb.fxnew
