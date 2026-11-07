# 落地光柱（at 落点）。
summon minecraft:text_display ~ ~ ~ {Tags:["rpg.pope.fx","rpg.pf.new","rpg.pf.pillar"],text:{text:"",font:"rpg:pope_fx"},background:0,billboard:"vertical",brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,18f,0f],scale:[0.125f,11.25f,1f]}}
scoreboard players set @e[tag=rpg.pf.new,distance=..1] rpg_pf_l 30
tag @e[tag=rpg.pf.new,distance=..1] remove rpg.pf.new
particle end_rod ~ ~0.5 ~ 0.4 2 0.4 0.03 24 normal
particle dust{color:[1.000f,0.847f,0.353f],scale:1.0} ~ ~1 ~ 0.6 1 0.6 0.04 24 normal
playsound minecraft:block.beacon.activate hostile @a[distance=..32] ~ ~ ~ 0.8 1.6
