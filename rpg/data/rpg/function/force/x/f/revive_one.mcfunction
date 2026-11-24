tp @s @a[tag=rpg.fo.self,limit=1]
tag @s remove rpg.fo.down
scoreboard players set @s rpg_fo_dn 0
effect give @s minecraft:instant_health 1 2 true
effect give @s minecraft:resistance 5 2 true
effect give @s minecraft:regeneration 10 1 true
execute at @s run particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.8 0.4 0.3 40
tellraw @a[distance=..64] ["",{"text":"[力] ","color":"#C9A646","bold":true,"italic":false},{"selector":"@s"},{"text":" 被圣灵从死亡里拉了回来。","color":"#E6DFCF","bold":false,"italic":false}]
execute at @s run summon minecraft:text_display ~ ~2.3 ~ {Tags:["rpg.fo.xh","rpg.fo.xhnew"],text:{text:"",font:"rpg:michael_vfx",color:"white"},background:0,billboard:"center",brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f],right_rotation:[0f,0f,0f,1f]}}
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_life 24
scoreboard players set @e[tag=rpg.fo.xhnew] rpg_fo_kd 20
tag @e[tag=rpg.fo.xhnew] remove rpg.fo.xhnew
