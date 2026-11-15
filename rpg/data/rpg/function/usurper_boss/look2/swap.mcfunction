# 换成首席附魔师（as/at 载体）：收掉附魔师的部件，把首席附魔师的部件挪到这个载体上
execute on passengers if entity @s[tag=rpg.usm.part] run kill @s
tag @s remove rpg.usm
tag @s add rpg.usb.s2
tag @s add rpg.prime_enchanter
function rpg:prime_enchanter/summon
execute as @e[type=minecraft:vindicator,tag=rpg.prime_enchanter,tag=!rpg.usb,distance=..1,limit=1] run function rpg:usurper_boss/look2/take
function rpg:prime_enchanter/anim/enter/appear
