execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.michael,distance=0..] run function rpg:prologue_i4/cut/kill_actor
execute in rpg:armageddon_4 run summon minecraft:vindicator 0 84 -2 {Tags:["rpg.pr.actor","rpg.pr.a.michael","rpg.pr.w.michael","rpg.pr.new"],Rotation:[0f,0f],NoAI:1b,Silent:1b,Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:scale",base:0.0625}],active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] at @s run function rpg:prologue_michael/dress
tag @e[type=minecraft:vindicator,tag=rpg.pr.new,distance=0..] remove rpg.pr.new
execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.michael,distance=0..] run function rpg:prologue_michael/anim/enter/look_down
function rpg:prologue_i4/sub/x02
execute in rpg:armageddon_4 positioned 0 81 -2 run summon minecraft:text_display ~ ~ ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"vertical",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:3f,transformation:{translation:[0f,7.0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,18f,0.6f],right_rotation:[0f,0f,0f,1f]}}
execute in rpg:armageddon_4 positioned 0 81 -2 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 30
execute in rpg:armageddon_4 positioned 0 81 -2 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 49
execute in rpg:armageddon_4 positioned 0 81 -2 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] teleport_duration set value 0
execute in rpg:armageddon_4 run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] 0.8 37.4 1.4 166.8 -85.8
