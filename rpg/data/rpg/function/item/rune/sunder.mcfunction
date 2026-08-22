# 裂甲［被动］—— 破开护甲：虚弱削弱其输出，发光让它无处可藏。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.sunder_tag1] run tag @s add rpg.rune.sunder
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run effect give @s minecraft:weakness 6 1 true
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run effect give @s minecraft:glowing 6 0 true
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run particle crit ~ ~1 ~ 0.35 0.4 0.35 0.25 18
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run playsound minecraft:item.shield.break hostile @a[distance=..14] ~ ~ ~ 0.6 1.4
tag @a[tag=rpg.rune.sunder] remove rpg.rune.sunder
