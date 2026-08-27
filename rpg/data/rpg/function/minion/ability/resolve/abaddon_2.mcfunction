# 疫矢猎印：延迟结算；单次总粒子预算不超过 28。
tag @s remove rpg.demon.minion.casting
scoreboard players set @s rpg_mn_cast 0
particle sculk_soul ~ ~1 ~ 0.38 0.55 0.38 0.025 2
playsound minecraft:item.crossbow.shoot hostile @a[distance=..14] ~ ~ ~ 0.32 1.05
tag @s add rpg.demon.minion.caster
effect give @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] minecraft:poison 4 0 true
effect give @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] minecraft:glowing 3 0 true
execute as @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run function rpg:inquest/seal/ability/record_magic
execute as @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run damage @s 3 minecraft:magic by @e[tag=rpg.demon.minion.caster,distance=..12,sort=nearest,limit=1]
execute at @a[distance=..10,sort=nearest,limit=1,gamemode=!spectator,gamemode=!creative] run particle crit ~ ~1 ~ 0.35 0.55 0.35 0.05 10
tag @s remove rpg.demon.minion.caster
