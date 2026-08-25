function rpg:inquest/stability/hit10
particle trial_omen ~ ~0.45 ~ 7 0.25 7 0.045 70 force
particle large_smoke ~ ~0.65 ~ 9 0.5 9 0.055 55 force
particle reverse_portal ~ ~1.1 ~ 11 0.9 11 0.07 75 force
particle explosion_emitter ~ ~0.4 ~ 0 0 0 0 1 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle trial_omen ~ ~1 ~ 0.45 0.7 0.45 0.04 12 force
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 6 minecraft:magic
playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..36] ~ ~ ~ 1.1 0.65
playsound minecraft:entity.generic.explode hostile @a[distance=..32] ~ ~ ~ 0.9 0.72
