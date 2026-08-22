# 熔岩链锯［熔锯］—— 右键起锯。与藤蔓之鞭同一形状：
# 起手只挂一个倒计时，之后每刻由 saw 函数按节拍落刀。
advancement revoke @s only rpg:item/lavasaw
execute if entity @s[scores={rpg_saw=1..}] run return 0
scoreboard players set @s rpg_saw 60
particle lava ~ ~1 ~ 0.4 0.4 0.4 0 12
playsound minecraft:block.respawn_anchor.charge player @a[distance=..18] ~ ~ ~ 1 1.4
playsound minecraft:entity.blaze.ambient player @a[distance=..18] ~ ~ ~ 0.8 1.8
