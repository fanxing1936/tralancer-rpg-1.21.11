execute as @a[scores={sakura=0..},tag=rpg.h.sakura_tag1] at @s run scoreboard players add @s sakura_step 1
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=5..},tag=rpg.h.sakura_tag1] run scoreboard players set @s sakura_step 1


execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=1},tag=rpg.h.sakura_tag1] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 1 50


execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.sakura_tag1] run particle dust_pillar{block_state:{Name:cherry_leaves}} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 75
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.sakura_tag1] run effect give @e[distance=..0.1] minecraft:wind_charged 10 2 true


execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=3},tag=rpg.h.sakura_tag1] run particle dust_color_transition{from_color:[1.0,0.47,0.47],to_color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 50


execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run particle dust_color_transition{from_color:[1.0,0.47,0.47],to_color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 50
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 1 50
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run summon minecraft:creeper ~ ~ ~ {Silent:1b,"ExplosionRadius":1,"Fuse":0}
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run summon minecraft:lightning_bolt
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run effect give @s minecraft:resistance 1 255 true
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run effect give @s minecraft:instant_health 1 3 true

execute as @e at @s on attacker if entity @s[tag=rpg.h.sakura_tag1] run particle cherry_leaves ~0.25 ~2.25 ~0.25 -0.5 -0.5 -0.5 1 5
execute as @e at @s on attacker if entity @s[tag=rpg.h.sakura_tag1] run damage @e[limit=1,sort=nearest] 2 minecraft:player_attack
execute as @e at @s on attacker if entity @s[tag=rpg.h.sakura_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true

execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=1},tag=rpg.h.night_tag1] run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0],scale:3} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 10
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=1},tag=rpg.h.night_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0d,1d,0d]}
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=1},tag=rpg.h.night_tag1] run scoreboard players set @s sakura_step 0


execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.night_tag1] run particle enchant ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 100
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.night_tag1] run effect give @e[limit=1,sort=nearest] minecraft:slowness 3 3 true
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.night_tag1] run scoreboard players set @s sakura_step 0


execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=3},tag=rpg.h.night_tag1] run particle dust_pillar{block_state:{Name:purple_glazed_terracotta}} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 100
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=3},tag=rpg.h.night_tag1] run effect give @s minecraft:instant_health 1 2 true
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=3},tag=rpg.h.night_tag1] run scoreboard players set @s sakura_step 0


execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run summon minecraft:spectral_arrow ~ ~10 ~ {Tags:["sakura_tag"]}
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run summon minecraft:spectral_arrow ~1 ~10 ~ {Tags:["sakura_tag"]}
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run summon minecraft:spectral_arrow ~ ~10 ~1 {Tags:["sakura_tag"]}
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run summon minecraft:spectral_arrow ~-1 ~10 ~ {Tags:["sakura_tag"]}
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run summon minecraft:spectral_arrow ~ ~10 ~-1 {Tags:["sakura_tag"]}
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run scoreboard players set @s sakura_step 0

execute as @e at @s on attacker if entity @s[scores={sakura=0..},tag=rpg.h.night_tag1,tag=rpg.e.offhand_sakura_tag1] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 1 10
execute as @e at @s on attacker if entity @s[scores={sakura=0..},tag=rpg.h.night_tag1,tag=rpg.e.offhand_sakura_tag1] run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0],scale:3} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 10

scoreboard players reset * random
scoreboard players reset * sakura



execute as @e[tag=sakura_tag] at @s run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~0.1 ~0.1 ~0.1 -0.2 -0.2 -0.2 0.2 10
execute as @e[tag=sakura_tag] at @s unless block ~ ~-0.1 ~ air run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~1.5 ~ ~1.5 -3 -0.1 -3 0.2 200
execute as @e[tag=sakura_tag] at @s unless block ~ ~-0.1 ~ air run summon minecraft:creeper ~ ~ ~ {Silent:1b,"ExplosionRadius":3,"Fuse":0}
execute as @e[tag=sakura_tag] at @s unless block ~ ~-0.1 ~ air run kill @s

execute as @e[tag=sakura_tag] at @s if entity @e[distance=0.2..0.4] run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~1.5 ~ ~1.5 -3 -0.1 -3 0.2 200
execute as @e[tag=sakura_tag] at @s if entity @e[distance=0.2..0.4] run summon minecraft:creeper ~ ~ ~ {Silent:1b,"ExplosionRadius":3,"Fuse":0}
execute as @e[tag=sakura_tag] at @s if entity @e[distance=0.2..0.4] run kill @s