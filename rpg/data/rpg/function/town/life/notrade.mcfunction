# 村民的身体是隐形的（外观是城镇模型），职业只决定交易：改成无职业，就不会再生成交易、不会弹交易面板
data merge entity @s {VillagerData:{profession:"minecraft:none"},Offers:{Recipes:[]}}
tag @s add rpg.tl.notrade
