execute as @a[scores={ashes=0..},tag=rpg.h.ashes_tag1] at @s run scoreboard players add @s ashes_level 1
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=5..},tag=rpg.h.ashes_tag1] run scoreboard players set @s ashes_level 1

execute as @e at @s on attacker if entity @s[scores={ashes=0..},tag=rpg.h.ashes_tag1] run effect give @e[distance=0..1] minecraft:wither 2 3 true
execute as @e at @s on attacker if entity @s[scores={ashes=0..},tag=rpg.h.ashes_tag1] run effect give @e[distance=0..1] minecraft:glowing 2 3 true
execute as @e at @s on attacker if entity @s[scores={ashes=0..},tag=rpg.h.ashes_tag1] run particle large_smoke ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30

execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=1},tag=rpg.h.ashes_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0d,0.5d,0d]}
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=1},tag=rpg.h.ashes_tag1] run particle dust_pillar{block_state:{Name:deepslate_coal_ore}} ~0.5 ~1.2 ~0.5 -1 -1 -1 1 20
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=1},tag=rpg.h.ashes_tag1] run playsound minecraft:item.mace.smash_air

execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=2},tag=rpg.h.ashes_tag1] run particle minecraft:sweep_attack ~1 ~2 ~1 -2 -2 -2 1 50 
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=2},tag=rpg.h.ashes_tag1] run playsound minecraft:item.mace.smash_ground

execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=3},tag=rpg.h.ashes_tag1] run particle squid_ink ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 100
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=3},tag=rpg.h.ashes_tag1] run playsound minecraft:item.mace.smash_ground_heavy

execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=4},tag=rpg.h.ashes_tag1] run summon firework_rocket ~ ~1 ~ {Life:0,LifeTime:0,FireworksItem:{id:firework_rocket,components:{fireworks:{flight_duration:0,explosions:[{shape:burst,has_twinkle:1b,has_trail:1b,colors:[I;1908001,4673362,10329495,4673362,1908001]}]}}}}
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=4},tag=rpg.h.ashes_tag1] run effect give @s minecraft:wither 2 2 true 


execute as @e at @s on attacker if entity @s[tag=rpg.h.ashes_tag1] run particle large_smoke ~0.25 ~1.5 ~0.25 -0.5 -1 -0.5 0 2
execute as @e at @s on attacker if entity @s[tag=rpg.h.ashes_tag1] run tag @e[distance=0..2] add ashes
scoreboard players reset * ashes

execute as @a[scores={ashes_step=30}] anchored feet at @s run summon armor_stand ^ ^ ^3 {Invisible:1b,CustomName:[{"text":"ashes_fac"}],Invulnerable:1b}
execute as @a[scores={ashes_step=40}] anchored feet at @s run summon armor_stand ^ ^ ^3 {Invisible:1b,CustomName:[{"text":"ashes_fac"}],Invulnerable:1b}
execute as @a[scores={ashes_step=50..}] anchored feet at @s run summon armor_stand ^ ^ ^3 {Invisible:1b,CustomName:[{"text":"ashes_atk"}],Invulnerable:1b}
execute as @a[scores={ashes_step=30}] anchored eyes at @s run playsound minecraft:item.mace.smash_air player @s
execute as @a[scores={ashes_step=40}] anchored eyes at @s run playsound minecraft:item.mace.smash_air player @s
execute as @a[scores={ashes_step=50..}] anchored eyes at @s run playsound minecraft:item.mace.smash_air player @s
execute as @e[name=ashes_atk,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @e[tag=ashes,limit=1]
execute as @e[name=ashes_fac,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @p[scores={ashes_step=30..31}]
execute as @e[name=ashes_fac,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @p[scores={ashes_step=40..41}]
execute as @a[scores={ashes_step=50..}] anchored eyes at @s run scoreboard players set @s ashes_step 0

execute as @e[name=ashes_fac,type=armor_stand] anchored eyes at @s run particle minecraft:sweep_attack ~0.5 ~1.2 ~0.5 -1 -1 -1 0 50 force
execute as @e[name=ashes_fac,type=armor_stand] anchored eyes at @s run particle large_smoke ~0.5 ~1.2 ~0.5 -1 -1 -1 0.1 50 force
execute as @e[name=ashes_fac,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^-1  
execute as @e[name=ashes_fac,type=armor_stand] anchored feet at @s run damage @e[limit=1,sort=nearest,distance=0.1..2.5] 15 minecraft:outside_border
execute as @e[name=ashes_fac,type=armor_stand] anchored feet at @s run data merge entity @e[limit=1,sort=nearest,distance=0.1..2.5] {Motion:[0d,2d,0d]}
execute as @e[name=ashes_fac,type=armor_stand] anchored feet at @s unless entity @a[distance=..50,tag=rpg.h.ashes_tag1] run kill 

execute as @e[name=ashes_atk,type=armor_stand] anchored eyes at @s run particle minecraft:squid_ink ~0.5 ~1.2 ~0.5 -1 -1 -1 0 50 force
execute as @e[name=ashes_atk,type=armor_stand] anchored eyes at @s run particle large_smoke ~0.5 ~1.2 ~0.5 -1 -1 -1 0.2 50 force
execute as @e[name=ashes_atk,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^1  
execute as @e[name=ashes_atk,type=armor_stand] anchored feet at @s run damage @e[limit=1,sort=nearest,distance=0.1..3,tag=ashes] 10 minecraft:outside_border
execute as @e[name=ashes_atk,type=armor_stand] anchored feet at @s run tag @e[limit=1,sort=nearest,distance=..3,tag=ashes,type=!armor_stand] remove ashes
execute as @e[name=ashes_atk,type=armor_stand] anchored feet at @s unless entity @a[distance=..50,tag=rpg.h.ashes_tag1] run kill 