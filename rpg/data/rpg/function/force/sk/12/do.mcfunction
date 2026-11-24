playsound minecraft:entity.phantom.flap player @a[distance=..16] ~ ~ ~ 1 1.4
playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 0.5 2
particle minecraft:end_rod ~ ~0.5 ~ 0.6 0.2 0.6 0.05 30
summon minecraft:text_display ^ ^1.4 ^-0.7 {Tags:["rpg.fo.hfx","rpg.fo.hfxnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.75f,3.75f,3.75f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_life 14
scoreboard players set @e[tag=rpg.fo.hfxnew] rpg_fo_kd 19
tag @e[tag=rpg.fo.hfxnew] remove rpg.fo.hfxnew
execute if score #lv rpg_fo matches 1 run scoreboard players set #r rpg_fo 16
execute if score #lv rpg_fo matches 2 run scoreboard players set #r rpg_fo 20
execute if score #lv rpg_fo matches 3 run scoreboard players set #r rpg_fo 24
execute rotated ~ -28 run function rpg:force/blink/step
effect give @s minecraft:slow_falling 4 0 true
