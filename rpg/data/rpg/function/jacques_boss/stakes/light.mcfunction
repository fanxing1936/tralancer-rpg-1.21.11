# 第 i 根柱点燃，和下一根之间连起火墙（as/at 这根柱的标记）
tag @s add rpg.jqb.lit
particle minecraft:flame ~ ~1.5 ~ 0.3 1 0.3 0.05 20
particle minecraft:flash{color:16747069} ~ ~2 ~ 0 0 0 0 1 force
function rpg:jacques_boss/stakes/light_fx
playsound minecraft:item.firecharge.use hostile @a[distance=..32] ~ ~ ~ 1 0.8
function rpg:jacques_boss/stakes/wall_show
function rpg:jacques_boss/stakes/wall
