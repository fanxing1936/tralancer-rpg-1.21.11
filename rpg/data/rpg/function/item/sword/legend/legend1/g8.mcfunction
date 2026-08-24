# 31 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=5..},tag=rpg.h.sakura_tag1] run scoreboard players set @s sakura_step 1


execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=1},tag=rpg.h.sakura_tag1] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20


execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.sakura_tag1] run particle dust_pillar{block_state:{Name:cherry_leaves}} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.sakura_tag1] run effect give @e[distance=..0.1] minecraft:wind_charged 10 2 true


execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=3},tag=rpg.h.sakura_tag1] run particle dust_color_transition{from_color:[1.0,0.47,0.47],to_color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20


execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run particle dust_color_transition{from_color:[1.0,0.47,0.47],to_color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run summon minecraft:tnt ~ ~ ~ {fuse:0s,explosion_power:1.0f,Silent:1b}
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run summon minecraft:lightning_bolt
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run effect give @s minecraft:resistance 1 255 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run effect give @s minecraft:instant_health 1 3 true

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.sakura_tag1] run particle cherry_leaves ~0.25 ~2.25 ~0.25 -0.5 -0.5 -0.5 1 5
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.sakura_tag1] run damage @e[limit=1,sort=nearest] 2 minecraft:player_attack
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.sakura_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=1},tag=rpg.h.night_tag1] run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0],scale:3} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=1},tag=rpg.h.night_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0d,1d,0d]}
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=1},tag=rpg.h.night_tag1] run scoreboard players set @s sakura_step 0


execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.night_tag1] run particle enchant ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 100
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.night_tag1] run effect give @e[limit=1,sort=nearest] minecraft:slowness 3 3 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.night_tag1] run scoreboard players set @s sakura_step 0


execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=3},tag=rpg.h.night_tag1] run particle dust_pillar{block_state:{Name:purple_glazed_terracotta}} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 100
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=3},tag=rpg.h.night_tag1] run effect give @s minecraft:instant_health 1 2 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=3},tag=rpg.h.night_tag1] run scoreboard players set @s sakura_step 0


execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run summon minecraft:spectral_arrow ~ ~10 ~ {Tags:["sakura_tag"]}
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run summon minecraft:spectral_arrow ~1 ~10 ~ {Tags:["sakura_tag"]}
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run summon minecraft:spectral_arrow ~ ~10 ~1 {Tags:["sakura_tag"]}
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run summon minecraft:spectral_arrow ~-1 ~10 ~ {Tags:["sakura_tag"]}
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run summon minecraft:spectral_arrow ~ ~10 ~-1 {Tags:["sakura_tag"]}
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.night_tag1] run scoreboard players set @s sakura_step 0

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..},tag=rpg.h.night_tag1,tag=rpg.e.offhand_sakura_tag1] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 1 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sakura=0..},tag=rpg.h.night_tag1,tag=rpg.e.offhand_sakura_tag1] run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0],scale:3} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 10
