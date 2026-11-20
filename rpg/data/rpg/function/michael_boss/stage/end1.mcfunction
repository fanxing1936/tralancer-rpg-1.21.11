# 一阶段打完：骨中之骨。无敌、站定，约 6 秒后进入二阶段。
function rpg:michael_boss/refill
function rpg:michael_boss/sk/end
function rpg:michael_boss/solid/off
tag @s add rpg.mkb.morph
scoreboard players set @s rpg_mk_c 0
kill @e[tag=rpg.mkb.fx]
data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}
tp @s @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1]
execute at @s run execute facing entity @e[tag=rpg.unit.f,distance=..40,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s run tp @s ^ ^ ^2
function rpg:michael/anim/enter/kneel
bossbar set rpg:michael_boss value 1200
bossbar set rpg:michael_boss name {"text":"\ue300\ue2f4\ue2f0\ue2f8","font":"rpg:michael_boss"}
