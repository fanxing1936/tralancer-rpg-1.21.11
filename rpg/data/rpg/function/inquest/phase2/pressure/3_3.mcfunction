scoreboard players set @s rpg_ex_wave 20
scoreboard players set @s rpg_ex_wave_kind 33
particle flash{color:10989513} ~ ~1.2 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.65,0.69,0.79],to_color:[0.42,0.42,0.44],scale:1.8} ~ ~0.25 ~ 5 0.08 5 0.025 48 force
particle dust_color_transition{from_color:[0.65,0.69,0.79],to_color:[0.42,0.42,0.44],scale:2.5} ~ ~0.50 ~ 11 0.14 11 0.045 72 force
particle large_smoke ~ ~1.15 ~ 12 1.8 12 0.07 80 force
particle soul ~ ~1.55 ~ 8 1.2 8 0.045 40 force
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
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"〖罪域・亚巴顿〗","color":"#8C90A1","bold":true,"italic":false},{"text":" 𝔇𝔬𝔪𝔦𝔫𝔦𝔬𝔫","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"深渊张口 · 三重罪域爆发，退入法阵四格庇护圈。","color":"#9C9A94","italic":false}]
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle large_smoke ~ ~1 ~ 0.65 0.95 0.65 0.06 16 normal
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle sculk_charge_pop ~ ~1 ~ 0.38 0.60 0.38 0.04 10 normal
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 11 minecraft:magic
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..32] ~ ~ ~ 0.95 0.96
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:darkness 9 0 true
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:levitation 3 0 true
execute as @a[distance=8..24,gamemode=!spectator,gamemode=!creative] run damage @s 4 minecraft:magic
