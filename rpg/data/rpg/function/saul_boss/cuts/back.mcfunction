# 在中心现身（as 他），朝最近的人
tp @s @e[type=minecraft:marker,tag=rpg.slb.center,limit=1]
tag @s remove rpg.slb.hidden
execute at @s run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
data merge entity @s {Invulnerable:0b,NoGravity:0b}
function rpg:saul/anim/enter/land
execute at @s run particle minecraft:flash{color:15660282} ~ ~1.4 ~ 0 0 0 0 1 force
execute at @s run particle minecraft:sweep_attack ~ ~1 ~ 1 0.6 1 0 8 force
execute at @s run playsound minecraft:entity.breeze.wind_burst hostile @a[distance=..40] ~ ~ ~ 1 0.8
