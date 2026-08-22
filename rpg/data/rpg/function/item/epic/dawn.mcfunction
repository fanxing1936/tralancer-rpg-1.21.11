# 破晓［曦光］—— 对亡灵是白昼，对其余是刺目的强光。
# 走 rpg.hurt + on attacker，不新增任何全场遍历。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.dawn_tag1] run tag @s add rpg.epic.dawn
execute as @e[tag=rpg.hurt,type=#minecraft:undead] at @s if entity @a[tag=rpg.epic.dawn,distance=..8] run damage @s 6 minecraft:magic by @a[tag=rpg.epic.dawn,limit=1,sort=nearest]
execute as @e[tag=rpg.hurt,type=#minecraft:undead] at @s if entity @a[tag=rpg.epic.dawn,distance=..8] run particle dust_color_transition{from_color:16575098,to_color:8005632,scale:2} ~ ~1 ~ 0.35 0.5 0.35 0.06 26
execute as @e[tag=rpg.hurt,type=#minecraft:undead] at @s if entity @a[tag=rpg.epic.dawn,distance=..8] run particle minecraft:flash{color:16575098} ~ ~1 ~ 0 0 0 0 1
execute as @e[tag=rpg.hurt,type=#minecraft:undead] at @s if entity @a[tag=rpg.epic.dawn,distance=..8] run playsound minecraft:item.firecharge.use hostile @a[distance=..16] ~ ~ ~ 0.7 1.5
execute as @e[tag=rpg.hurt,type=!#minecraft:undead] at @s if entity @a[tag=rpg.epic.dawn,distance=..8] run effect give @s minecraft:blindness 4 0 true
execute as @e[tag=rpg.hurt,type=!#minecraft:undead] at @s if entity @a[tag=rpg.epic.dawn,distance=..8] run particle end_rod ~ ~1.2 ~ 0.3 0.4 0.3 0.03 14
tag @a[tag=rpg.epic.dawn] remove rpg.epic.dawn
