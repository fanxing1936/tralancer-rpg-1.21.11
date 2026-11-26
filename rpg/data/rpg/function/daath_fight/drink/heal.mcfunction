scoreboard players operation #h rpg_dt = @s rpg_dt_mx
scoreboard players set #k rpg_dt 60
scoreboard players operation #h rpg_dt *= #k rpg_dt
scoreboard players operation #h rpg_dt /= #100 rpg_dt
scoreboard players operation #h rpg_dt += @s rpg_dt_h
scoreboard players operation #k rpg_dt = @s rpg_dt_mx
scoreboard players operation #k rpg_dt *= #10 rpg_dt
execute if score #h rpg_dt > #k rpg_dt run scoreboard players operation #h rpg_dt = #k rpg_dt
scoreboard players operation @s rpg_dt_h = #h rpg_dt
particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 6
playsound minecraft:entity.witch.drink hostile @a[distance=..48] ~ ~ ~ 1 0.8
