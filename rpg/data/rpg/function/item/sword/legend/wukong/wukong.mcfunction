execute as @e at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run effect give @e[limit=1,sort=nearest] wither 5 10 true
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run summon minecraft:tnt ~ ~ ~ {fuse:0s,explosion_power:5.0f}
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run effect give @s resistance 5 10 false
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run particle gust_emitter_small ~0.5 ~1.5 ~0.5 -1 -1 -1 1 10
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run function rpg:item/sword/legend/wukong/particle


execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=2},tag=rpg.h.wukong_tag1] run effect give @s minecraft:instant_health 1 1 true
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=2},tag=rpg.h.wukong_tag1] run particle minecraft:totem_of_undying ~1 ~1.5 ~1 -2 -2 -2 1 50
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=2},tag=rpg.h.wukong_tag1] run playsound minecraft:item.mace.smash_ground_heavy 


execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=3},tag=rpg.h.wukong_tag1] run effect give @e[distance=0..1] minecraft:slowness 3 255 true
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=3},tag=rpg.h.wukong_tag1] run particle enchant ~1 ~1.5 ~1 -2 -2 -2 1 50
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=3},tag=rpg.h.wukong_tag1] run effect give @e[distance=0..1] minecraft:glowing 3 255 true
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=3},tag=rpg.h.wukong_tag1] run playsound minecraft:item.mace.smash_ground_heavy 


execute as @e at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run effect give @e[distance=0..2] minecraft:wind_charged 10 10 true
execute as @e at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run particle dust_color_transition{from_color:[1.0,0.35,0.0],to_color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20
execute as @e at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run particle dust_color_transition{from_color:[1.0,0.87,0.0],to_color:[1.0,1.0,1.0],scale:2} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20
execute as @e at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s

scoreboard players reset * random
scoreboard players reset * wukong

