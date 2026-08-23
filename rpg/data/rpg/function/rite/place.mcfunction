# 图腾落地。此刻它还是熄的 —— 要等圣水浇上去。
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.totem"],item:{id:"minecraft:totem_of_undying",count:1},transformation:{translation:[0f,0.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f],right_rotation:[0f,0f,0f,1f]},billboard:"vertical",brightness:{sky:15,block:15}}
particle dust{color:[0.95,0.86,0.45],scale:1} ~ ~0.6 ~ 0.3 0.4 0.3 0.02 20
playsound minecraft:block.respawn_anchor.set_spawn player @a[distance=..16] ~ ~ ~ 1 1.4
title @a[distance=..6] actionbar ["",{"text":"图腾已立","color":"gold"},{"text":"　以驱魔圣水浇之","color":"gray","italic":true}]
