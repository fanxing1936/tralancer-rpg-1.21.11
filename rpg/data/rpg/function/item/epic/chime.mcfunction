# 晶啸［共振］—— 命中的震荡沿晶体传开，波及目标身边的敌人。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.chime_tag1] run tag @s add rpg.epic.chime
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.epic.chime,distance=..8] run particle dust_color_transition{from_color:4066619,to_color:11121336,scale:2} ~ ~1 ~ 0.4 0.5 0.4 0.05 24
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.epic.chime,distance=..8] run playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..16] ~ ~ ~ 1 1.2
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.epic.chime,distance=..8] run function rpg:item/epic/chime_wave
tag @a[tag=rpg.epic.chime] remove rpg.epic.chime
