execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute positioned ^ ^ ^1.6 run tag @a[distance=..2.4,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 10
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
summon minecraft:text_display ^ ^1.2 ^0.9 {Tags:["rpg.dt.fx","rpg.dt.fxnew"],text:{text:"",font:"rpg:daath_vfx",color:"#FFFFFF"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.925f,2.925f,2.925f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_life 12
scoreboard players set @e[tag=rpg.dt.fxnew] rpg_dt_kd 27
tag @e[tag=rpg.dt.fxnew] remove rpg.dt.fxnew
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..48] ~ ~ ~ 1 0.9
