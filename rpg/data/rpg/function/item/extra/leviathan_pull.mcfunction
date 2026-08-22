# 每刻：把 7 格内的一切拖向锚心，并铺开漩涡的水纹。
# 漩涡要转满 5~8 秒，所以每刻的粒子必须省着用：
# 原本每刻 36 粒 × 100 刻 ≈ 3600 粒，客户端明显吃不消。现在每刻 13 粒。
particle dust_color_transition{from_color:532802,to_color:1195644,scale:2} ~ ~0.3 ~ 3.5 0.25 3.5 0.02 9
particle bubble_column_up ~ ~ ~ 0.8 0.1 0.8 0.03 3
particle dust_color_transition{from_color:1195644,to_color:16559622,scale:1} ~ ~1.4 ~ 0.2 0.5 0.2 0.02 1
execute as @e[distance=1.2..7,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker] at @s facing entity @e[tag=rpg.levi.anchor,limit=1,sort=nearest] feet run tp @s ^ ^ ^0.55
execute as @e[distance=..7,type=!player,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:marker] run effect give @s minecraft:slowness 2 2 true
