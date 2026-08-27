# 深渊低语：延迟结算；单次总粒子预算不超过 28。
tag @s remove rpg.demon.minion.casting
scoreboard players set @s rpg_mn_cast 0
particle sculk_soul ~ ~1 ~ 0.38 0.55 0.38 0.025 2
playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..14] ~ ~ ~ 0.32 1.05
tag @s add rpg.demon.minion.caster
effect give @a[distance=..8,gamemode=!spectator,gamemode=!creative] minecraft:darkness 3 0 true
effect give @a[distance=..8,gamemode=!spectator,gamemode=!creative] minecraft:slowness 4 0 true
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run function rpg:inquest/seal/ability/record_magic
execute as @a[distance=..8,gamemode=!spectator,gamemode=!creative] run damage @s 2 minecraft:magic by @e[tag=rpg.demon.minion.caster,distance=..10,sort=nearest,limit=1]
tag @s remove rpg.demon.minion.caster
particle reverse_portal ~ ~1 ~ 0.85 0.75 0.85 0.04 10
