scoreboard players set @s rpg_ex_wave 20
scoreboard players set @s rpg_ex_wave_kind 63
particle flash{color:14252761} ~ ~1.2 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.85,0.48,0.85],to_color:[0.36,0.17,0.44],scale:1.8} ~ ~0.25 ~ 5 0.08 5 0.025 48 force
particle dust_color_transition{from_color:[0.85,0.48,0.85],to_color:[0.36,0.17,0.44],scale:2.5} ~ ~0.50 ~ 11 0.14 11 0.045 72 force
particle portal ~ ~1.15 ~ 12 1.8 12 0.07 80 force
particle reverse_portal ~ ~1.55 ~ 8 1.2 8 0.045 40 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~4 ~0.15 ~0 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~3.696 ~0.15 ~1.531 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~2.828 ~0.15 ~2.828 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~1.531 ~0.15 ~3.696 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~0 ~0.15 ~4 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~-1.531 ~0.15 ~3.696 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~-2.828 ~0.15 ~2.828 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~-3.696 ~0.15 ~1.531 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~-4 ~0.15 ~0 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~-3.696 ~0.15 ~-1.531 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~-2.828 ~0.15 ~-2.828 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~-1.531 ~0.15 ~-3.696 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~0 ~0.15 ~-4 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~1.531 ~0.15 ~-3.696 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~2.828 ~0.15 ~-2.828 0 0 0 0 1 force
particle dust_color_transition{from_color:[1.0,0.95,0.66],to_color:[1.0,0.85,0.35],scale:1.3} ~3.696 ~0.15 ~-1.531 0 0 0 0 1 force
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"〖罪域・贝利尔〗","color":"#A057A9","bold":true,"italic":false},{"text":" 𝔇𝔬𝔪𝔦𝔫𝔦𝔬𝔫","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"欲障迷宫 · 三重罪域爆发，退入法阵四格庇护圈。","color":"#9C9A94","italic":false}]
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle portal ~ ~1 ~ 0.65 0.95 0.65 0.06 16 normal
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle heart ~ ~1 ~ 0.38 0.60 0.38 0.04 10 normal
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 10 minecraft:magic
playsound minecraft:entity.illusioner.prepare_mirror hostile @a[distance=..32] ~ ~ ~ 0.95 0.96
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:darkness 7 0 true
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:levitation 3 0 true
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:nausea 8 0 true
