# 一印（at 空中）：光环张开，锁定此刻玩家的位置。
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.more","rpg.pf.sealed"],text:{text:"",font:"rpg:pope_fx"},background:0,billboard:"center",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.0625f,0.0625f,1f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 40
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
execute facing entity @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=random,limit=1] eyes run function rpg:pope_fight/fx/lance_warn
playsound rpg:pope.load_spell hostile @a[distance=..32] ~ ~ ~ 0.6 1.3
