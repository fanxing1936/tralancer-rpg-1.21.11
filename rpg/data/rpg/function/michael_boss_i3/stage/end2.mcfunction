# 二阶段打完：两根肋骨落下，他跪在骨柱前，灵体一层层变淡、散去，留下三根实心的骨头。
function rpg:michael_boss_i3/refill
function rpg:michael_boss_i3/sk/end
function rpg:michael_boss_i3/solid/off
tag @s add rpg.mkb.end
scoreboard players set @s rpg_mk_c 0
data merge entity @s {NoAI:1b,Invulnerable:1b,NoGravity:0b}
kill @e[tag=rpg.mkb.fx,tag=!rpg.mkb.pillar,distance=0..]
execute as @e[type=minecraft:vindicator,tag=rpg.mkb.w,distance=0..] run function rpg:michael_boss_i3/watch/die
execute at @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] facing entity @s feet run tp @s ^ ^ ^1.8 ~ 0
execute at @s facing entity @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..] feet run tp @s ~ ~ ~ ~ 0
function rpg:michael/anim/enter/kneel
playsound minecraft:block.beacon.deactivate hostile @a[distance=..48] ~ ~ ~ 1.4 0.6
bossbar set rpg:michael_boss_i3 value 0
bossbar set rpg:michael_boss_i3 name {"text":"\ue320\ue2f5\ue2f1\ue2f9","font":"rpg:michael_boss"}
