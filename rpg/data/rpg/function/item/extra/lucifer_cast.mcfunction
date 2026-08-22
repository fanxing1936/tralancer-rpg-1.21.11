# 刺出蛇矛：沿视线一路贯穿，中者种下原罪。
# 长枪本身的攻击范围已是全包最远（+3 格），这一击把它推到 12 格。
xp add @s -2 levels
scoreboard players set @s rpg_luci_use 30
tag @s add rpg.luci.cast
particle dust_color_transition{from_color:9882230,to_color:4895350,scale:1} ~ ~1.1 ~ 0.3 0.3 0.3 0.02 14
playsound minecraft:entity.ender_dragon.flap player @a[distance=..24] ~ ~ ~ 0.7 1.7
playsound minecraft:block.sculk_catalyst.bloom player @a[distance=..24] ~ ~ ~ 1 0.6
execute at @s anchored eyes run function rpg:item/extra/lucifer_lance
execute at @s rotated ~ 0 run function rpg:item/extra/lucifer_fangs
tag @s remove rpg.luci.cast
