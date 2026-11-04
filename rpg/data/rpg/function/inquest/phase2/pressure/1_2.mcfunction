scoreboard players set @s rpg_ex_wave 20
scoreboard players set @s rpg_ex_wave_kind 12
particle flash{color:6280844} ~ ~1.2 ~ 0 0 0 0 1 force
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:1.8} ~ ~0.25 ~ 5 0.08 5 0.025 48 force
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:2.5} ~ ~0.50 ~ 11 0.14 11 0.045 72 force
particle enchanted_hit ~ ~1.15 ~ 12 1.8 12 0.07 80 force
particle end_rod ~ ~1.55 ~ 8 1.2 8 0.045 40 force
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
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"〖罪域・路西法〗","color":"#34975A","bold":true,"italic":false},{"text":" 𝔇𝔬𝔪𝔦𝔫𝔦𝔬𝔫","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"蛇庭敕令 · 三重罪域爆发，退入法阵四格庇护圈。","color":"#9C9A94","italic":false}]
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle enchanted_hit ~ ~1 ~ 0.65 0.95 0.65 0.06 16 normal
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] at @s run particle crit ~ ~1 ~ 0.38 0.60 0.38 0.04 10 normal
execute as @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] run damage @s 7 minecraft:magic
playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..32] ~ ~ ~ 0.95 0.88
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:poison 6 0 true
effect give @a[distance=4.01..24,gamemode=!spectator,gamemode=!creative] minecraft:slowness 7 1 true
summon minecraft:evoker_fangs ~6 ~ ~ {Tags:["rpg.rite.pressure"]}
summon minecraft:evoker_fangs ~-6 ~ ~ {Tags:["rpg.rite.pressure"]}
summon minecraft:evoker_fangs ~ ~ ~6 {Tags:["rpg.rite.pressure"]}
summon minecraft:evoker_fangs ~ ~ ~-6 {Tags:["rpg.rite.pressure"]}
