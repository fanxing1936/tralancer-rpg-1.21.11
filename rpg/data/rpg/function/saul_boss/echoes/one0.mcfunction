summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.slg","rpg.slb.echo","rpg.slb.ghostnew","rpg.slb.echo0"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,CustomName:{"text":"残影","color":"#E6ECF6","italic":true},active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[type=minecraft:vindicator,tag=rpg.slb.ghostnew] run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:vindicator,tag=rpg.slb.ghostnew] remove rpg.slb.ghostnew
particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~ ~1 ~ 0.3 0.7 0.3 0 12
particle minecraft:end_rod ~ ~1 ~ 0.25 0.6 0.25 0.02 6
