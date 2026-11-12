# 枯萎［被动］—— 攻击时四分之一的概率让目标凋零。
# 走 rpg.hurt + on attacker，与包里其余被动同一形状。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.wilt_tag1] run scoreboard players set @s rpg_rune_roll 0
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.wilt_tag1] store result score @s rpg_rune_roll run random value 1..4
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.wilt_tag1,scores={rpg_rune_roll=1}] run tag @s add rpg.rune.wilt
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.wilt,distance=..8] run effect give @s minecraft:wither 5 1 true
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.wilt,distance=..8] run particle dust_color_transition{from_color:[0.16,0.16,0.16],to_color:[0.05,0.22,0.05],scale:2} ~ ~1 ~ 0.3 0.5 0.3 0.04 24
execute as @e[tag=rpg.hurt] at @s if entity @a[tag=rpg.rune.wilt,distance=..8] run playsound minecraft:entity.wither.shoot hostile @a[distance=..16] ~ ~ ~ 0.5 1.6
tag @a[tag=rpg.rune.wilt] remove rpg.rune.wilt
