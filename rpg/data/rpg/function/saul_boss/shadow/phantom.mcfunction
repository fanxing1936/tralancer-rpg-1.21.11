# 老战友的幻影（at 他身前 2.6 格，朝他）：只是演出，不参与判定
summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.slg","rpg.slb.ghostnew"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:{"text":"老战友","color":"#E6ECF6","italic":true},active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}],attributes:[{id:"scale",base:1.1f}]}
execute as @e[type=minecraft:vindicator,tag=rpg.slb.ghostnew] run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:vindicator,tag=rpg.slb.ghostnew] remove rpg.slb.ghostnew
particle minecraft:end_rod ~ ~1 ~ 0.3 0.8 0.3 0.02 12
