##恶魔词缀
execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag1] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag1] run particle soul_fire_flame ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10

execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag2] run particle trial_spawner_detection_ominous ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag2] run particle sonic_boom ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 5


execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag3] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e at @s on attacker if entity @s[scores={devil_weapon=0..},tag=rpg.h.devil_weapon_tag3] run particle trial_omen ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10


scoreboard players reset * devil_weapon

##天使词缀
execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag1] run particle dust{color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag1] run particle end_rod ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10

execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag2] run particle firework ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag2] run particle end_rod ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10

execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag3] run particle totem_of_undying ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10
execute as @e at @s on attacker if entity @s[scores={holy=0..},tag=rpg.h.holy_weapon_tag3] run particle dust{color:[1.0,0.78,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 10


scoreboard players reset * holy


##别西卜

execute as @a[scores={ashes=0..},tag=rpg.h.ashes_tag1] at @s run scoreboard players add @s ashes_level 1
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=5..},tag=rpg.h.ashes_tag1] run scoreboard players set @s ashes_level 1

execute as @e at @s on attacker if entity @s[scores={ashes=0..},tag=rpg.h.ashes_tag1] run effect give @e[distance=0..1] minecraft:wither 2 3 true
execute as @e at @s on attacker if entity @s[scores={ashes=0..},tag=rpg.h.ashes_tag1] run effect give @e[distance=0..1] minecraft:glowing 2 3 true
execute as @e at @s on attacker if entity @s[scores={ashes=0..},tag=rpg.h.ashes_tag1] run particle large_smoke ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 15

execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=1},tag=rpg.h.ashes_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0d,0.5d,0d]}
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=1},tag=rpg.h.ashes_tag1] run particle dust_pillar{block_state:{Name:deepslate_coal_ore}} ~0.5 ~1.2 ~0.5 -1 -1 -1 1 10
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=1},tag=rpg.h.ashes_tag1] run playsound minecraft:item.mace.smash_air

execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=2},tag=rpg.h.ashes_tag1] run particle minecraft:sweep_attack ~1 ~2 ~1 -2 -2 -2 1 20 
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=2},tag=rpg.h.ashes_tag1] run playsound minecraft:item.mace.smash_ground

execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=3},tag=rpg.h.ashes_tag1] run particle squid_ink ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=3},tag=rpg.h.ashes_tag1] run playsound minecraft:item.mace.smash_ground_heavy

execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=4},tag=rpg.h.ashes_tag1] run summon firework_rocket ~ ~1 ~ {Life:0,LifeTime:0,FireworksItem:{id:firework_rocket,components:{fireworks:{flight_duration:0,explosions:[{shape:burst,has_twinkle:1b,has_trail:1b,colors:[I;1908001,4673362,10329495,4673362,1908001]}]}}}}
execute as @e at @s on attacker if entity @s[scores={ashes=0..,ashes_level=4},tag=rpg.h.ashes_tag1] run effect give @s minecraft:wither 2 2 true 


execute as @e at @s on attacker if entity @s[tag=rpg.h.ashes_tag1] run particle large_smoke ~0.1 ~1.5 ~0.1 -0.2 -1 -0.2 0.2 1
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

##贝利尔
execute as @e at @s on attacker if entity @s[scores={blil=0..},tag=rpg.h.blil_tag1] run effect give @e[distance=0..1] minecraft:wither 2 3 true
execute as @e at @s on attacker if entity @s[scores={blil=0..},tag=rpg.h.blil_tag1] run effect give @e[distance=0..1] minecraft:glowing 2 3 true
execute as @e at @s on attacker if entity @s[scores={blil=0..},tag=rpg.h.blil_tag1] run particle dust_color_transition{from_color:[0.4,0.0,0.6],scale:3,to_color:[0.0,0.0,0.0]} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30

execute as @e at @s on attacker if entity @s[tag=rpg.h.blil_tag1] run particle witch ~0.25 ~1.5 ~0.25 -0.5 -1 -0.5 0 2
scoreboard players reset * blil

##链锯
execute as @e at @s on attacker if entity @s[scores={chainsaw=0..},tag=rpg.h.chainsaw_tag1] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={chainsaw=0..},tag=rpg.h.chainsaw_tag1] run summon evoker_fangs ~ ~ ~ {Motion:[0d,0.2d,0d],Health:10,Glowing:1b,attributes:[{id:"scale",base:3f},{id:"max_health",base:10f}]}
execute as @e at @s on attacker if entity @s[tag=rpg.h.chainsaw_tag1] run particle trial_spawner_detection ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 5
execute as @e at @s on attacker if entity @s[tag=rpg.h.chainsaw_tag1] run damage @e[limit=1,sort=nearest] 1 minecraft:player_attack
execute as @e at @s on attacker if entity @s[tag=rpg.h.chainsaw_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
scoreboard players reset * random
scoreboard players reset * chainsaw

##漆黑之日 
advancement revoke @s only rpg:item/night
execute as @s at @s if entity @s[tag=rpg.h.sakura_tag1] run particle enchant ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 10
execute as @s at @s unless entity @s[tag=rpg.h.sakura_tag1] run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 10
execute as @s[scores={level=1..}] at @s run scoreboard players add @s night 1
execute if entity @s[tag=rpg.h.sakura_tag1] as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run particle dust_color_transition{from_color:[1.0,0.47,0.47],to_color:[1,1,1],scale:1} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 500
execute unless entity @s[tag=rpg.h.sakura_tag1] as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 500
execute as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 0 100
execute as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run summon minecraft:creeper ~ ~ ~ {Silent:1b,"ExplosionRadius":1,"Fuse":0}
execute as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run kill @e[type=#minecraft:arrows,distance=..3]
execute as @s[scores={level=1..,night=20..}] at @s run playsound minecraft:entity.ender_dragon.shoot player @s
execute as @s[scores={level=1..,night=20..}] at @s anchored eyes run xp add @s -3 points
execute as @s[scores={night=20..}] at @s run scoreboard players set @s night 0

##高山
execute as @e at @s on attacker if entity @s[scores={montain=0..},tag=rpg.h.montain_tag1] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={montain=0..},tag=rpg.h.montain_tag1] run summon llama_spit ~ ~5 ~ {Motion:[0d,-1d,0d]}
execute as @e at @s on attacker if entity @s[scores={montain=0..},tag=rpg.h.montain_tag1] run particle gust ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 5
execute as @e at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run particle dust_color_transition{from_color:[0.15,0.91,0.76],to_color:[0.9,0.63,0.0],scale:1} ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 3
execute as @e at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run particle dust_color_transition{from_color:[0.15,0.91,0.76],to_color:[0.9,0.63,0.0],scale:2} ~0.1 ~0.7 ~0.1 -0.2 -0.5 -0.2 0.1 5
execute as @e at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run particle dust_color_transition{from_color:[0.9,0.63,0.0],to_color:[0.15,0.91,0.76],scale:1} ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 2
execute as @e at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run damage @e[limit=1,sort=nearest] 1 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
scoreboard players reset * random
scoreboard players reset * montain

execute as @a[tag=rpg.h.montain_tag1] at @s run particle dust_color_transition{from_color:[0.15,0.91,0.76],to_color:[0.9,0.63,0.0],scale:2} ~0.1 ~0.3 ~0.1 -0.2 -0.2 -0.2 0.1 2

##风骨
execute as @e at @s on attacker if entity @s[scores={pen=0..},tag=rpg.h.pen_tag1] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={pen=0..},tag=rpg.h.pen_tag1] run particle squid_ink ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.2 20
execute as @a[scores={pen_=0..},tag=rpg.h.pen_tag1] at @s on attacker at @s run particle cloud ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 20
execute as @a[scores={pen_=0..},tag=rpg.h.pen_tag1] at @s on attacker at @s run damage @s 3 minecraft:out_of_world
execute as @a[scores={pen_=0..},tag=rpg.h.pen_tag1] at @s run effect give @s instant_health 1 0 true
execute as @e at @s on attacker if entity @s[tag=rpg.h.pen_tag1] run particle enchant ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 1 3
execute as @e at @s on attacker if entity @s[tag=rpg.h.pen_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
scoreboard players reset * random
scoreboard players reset * pen
scoreboard players reset * pen_

##剧毒之牙
execute as @e at @s on attacker if entity @s[scores={potion=0..},tag=rpg.h.potion_tag1] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={potion=0..},tag=rpg.h.potion_tag1] run summon llama_spit ~ ~5 ~ {Motion:[0d,-1d,0d]}
execute as @e at @s on attacker if entity @s[scores={potion=0..},tag=rpg.h.potion_tag1] run particle crit ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.5 30
execute as @e at @s on attacker if entity @s[tag=rpg.h.potion_tag1] run particle dust_color_transition{from_color:[0.52,0.8,0.0],to_color:[0.98,0.98,0.98],scale:2} ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 3
execute as @e at @s on attacker if entity @s[tag=rpg.h.potion_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
scoreboard players reset * random
scoreboard players reset * potion

##无垠星空
execute as @e at @s on attacker if entity @s[scores={saber=0..},tag=rpg.h.saber_tag1] store result score @s random run random value 1..10
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=1},tag=rpg.h.saber_tag1] run effect give @e[limit=1,sort=nearest] wither 10 40 true
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=1},tag=rpg.h.saber_tag1] run summon minecraft:creeper ~ ~ ~ {"ExplosionRadius":2,"Fuse":0}
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=1},tag=rpg.h.saber_tag1] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/flame
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=1},tag=rpg.h.saber_tag1] run effect give @s resistance 5 10 false
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=1},tag=rpg.h.saber_tag1] run particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[1.0,1.0,1.0],scale:1} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20


execute as @e at @s on attacker if entity @s[scores={saber=0..,random=2},tag=rpg.h.saber_tag1] run effect give @e[limit=1,sort=nearest] minecraft:wither 20 40 true
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=2},tag=rpg.h.saber_tag1] run particle minecraft:soul_fire_flame ~1 ~1.5 ~1 -2 -2 -2 0.5 100
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=2},tag=rpg.h.saber_tag1] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/particle
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=2},tag=rpg.h.saber_tag1] run effect give @s resistance 1 10 false
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=2},tag=rpg.h.saber_tag1] run playsound minecraft:item.mace.smash_ground_heavy 


execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] run effect give @e[distance=0..1] minecraft:slowness 5 255 true
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] run particle wax_off ~1 ~1.5 ~1 -2 -2 -2 1 100
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/spark
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] run effect give @e[distance=0..1] minecraft:glowing 5 255 true
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] run effect give @s resistance 1 10 false
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=3},tag=rpg.h.saber_tag1] run playsound minecraft:item.mace.smash_ground_heavy 


execute as @e at @s on attacker if entity @s[scores={saber=0..,random=4},tag=rpg.h.saber_tag1] at @e[limit=1,sort=nearest] run summon lightning_bolt
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=4},tag=rpg.h.saber_tag1] run particle minecraft:soul ~1 ~1.5 ~1 -2 -2 -2 0.5 100
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=4},tag=rpg.h.saber_tag1] run effect give @s resistance 1 10 false
execute as @e at @s on attacker if entity @s[scores={saber=0..,random=4},tag=rpg.h.saber_tag1] positioned ~ ~2 ~ run function rpg:item/sword/legend/saber/sweep


execute as @e at @s on attacker if entity @s[scores={saber=0..},tag=rpg.h.saber_tag1] run effect give @e[distance=0..2,limit=1,sort=nearest] minecraft:weakness 10 5 true
execute as @e at @s on attacker if entity @s[scores={saber=0..},tag=rpg.h.saber_tag1] run particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[0.0,0.98,1.0],scale:2} ~0.5 ~1 ~0.5 -1 -1 -1 1 20
execute as @e at @s on attacker if entity @s[scores={saber=0..},tag=rpg.h.saber_tag1] run particle dust_color_transition{from_color:[1.0,0.36,0.83],to_color:[1.0,1.0,1.0],scale:2} ~0.5 ~1 ~0.5 -1 -1 -1 1 20

scoreboard players reset * random
scoreboard players reset * saber

##樱怒之日
execute as @a[scores={sakura=0..},tag=rpg.h.sakura_tag1] at @s run scoreboard players add @s sakura_step 1
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=5..},tag=rpg.h.sakura_tag1] run scoreboard players set @s sakura_step 1


execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=1},tag=rpg.h.sakura_tag1] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20


execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.sakura_tag1] run particle dust_pillar{block_state:{Name:cherry_leaves}} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=2},tag=rpg.h.sakura_tag1] run effect give @e[distance=..0.1] minecraft:wind_charged 10 2 true


execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=3},tag=rpg.h.sakura_tag1] run particle dust_color_transition{from_color:[1.0,0.47,0.47],to_color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20


execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run particle dust_color_transition{from_color:[1.0,0.47,0.47],to_color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20
execute as @e at @s on attacker if entity @s[scores={sakura=0..,sakura_step=4},tag=rpg.h.sakura_tag1] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 1 20
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



execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~0.1 ~0.1 ~0.1 -0.2 -0.2 -0.2 0.2 10
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s unless block ~ ~-0.1 ~ air run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~1.5 ~ ~1.5 -3 -0.1 -3 0.2 200
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s unless block ~ ~-0.1 ~ air run summon minecraft:creeper ~ ~ ~ {Silent:1b,"ExplosionRadius":3,"Fuse":0}
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s unless block ~ ~-0.1 ~ air run kill @s

execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s if entity @e[distance=0.2..0.4] run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~1.5 ~ ~1.5 -3 -0.1 -3 0.2 200
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s if entity @e[distance=0.2..0.4] run summon minecraft:creeper ~ ~ ~ {Silent:1b,"ExplosionRadius":3,"Fuse":0}
execute as @e[type=minecraft:spectral_arrow,tag=sakura_tag] at @s if entity @e[distance=0.2..0.4] run kill @s

##亚巴顿
execute as @e at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] store result score @e[limit=1,sort=nearest] random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,sort=nearest] 2 minecraft:player_attack by @s
execute as @e at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run effect give @e[distance=0..2] wither 5 1 true
execute as @e at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run particle sculk_soul ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50
execute as @e at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run particle trial_spawner_detection_ominous ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50
execute as @e[scores={random=1}] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0.8d,0.8d,0.8d]}
execute as @e[scores={random=2}] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[-0.8d,0.8d,0.8d]}
execute as @e[scores={random=3}] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0.8d,0.8d,-0.8d]}
execute as @e[scores={random=4}] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[-0.8d,0.8d,-0.8d]}
execute as @e[scores={random=5}] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0d,0.8d,0d]}
scoreboard players reset * soul


##风
execute as @e at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run effect give @e[distance=0..2] minecraft:wind_charged 20 40 true
execute as @e at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run particle dust_color_transition{from_color:[0.53,0.78,0.37],to_color:[1.0,1.0,1.0],scale:3} ~1 ~2 ~1 -2 -2 -2 1 50
execute as @e at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run particle minecraft:gust_emitter_small ~0.5 ~1.2 ~0.5 -1 -1 -1 1 2
execute as @e at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0d,0.8d,0d]}
scoreboard players reset * typhoon

execute as @a[scores={typhoon_step=50..}] anchored feet at @s run summon armor_stand ^ ^ ^2 {Invisible:1b,CustomName:[{"text":"typhoon_atk"}],Invulnerable:1b}
execute as @a[scores={typhoon_step=50..}] anchored feet at @s run summon armor_stand ^2 ^ ^2 {Invisible:1b,CustomName:[{"text":"typhoon_atk"}],Invulnerable:1b}
execute as @a[scores={typhoon_step=50..}] anchored feet at @s run summon armor_stand ^-2 ^ ^2 {Invisible:1b,CustomName:[{"text":"typhoon_atk"}],Invulnerable:1b}

execute as @a[scores={typhoon_step=50..}] anchored eyes at @s run playsound minecraft:item.trident.throw player @s
execute as @e[name=typhoon_atk,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @p[scores={typhoon_step=50..}]
execute as @a[scores={typhoon_step=50..}] anchored eyes at @s run scoreboard players set @s typhoon_step 0
execute as @e[name=typhoon_atk,type=armor_stand] anchored eyes at @s run particle minecraft:gust_emitter_small ~0.5 ~1.2 ~0.5 -1 -1 -1 1 2 force
execute as @e[name=typhoon_atk,type=armor_stand] anchored eyes at @s run particle dust_color_transition{from_color:[0.53,0.78,0.37],to_color:[1.0,1.0,1.0],scale:3} ~1 ~2 ~1 -2 -2 -2 1 10 force
execute as @e[name=typhoon_atk,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^-1  
execute as @e[name=typhoon_atk,type=armor_stand] anchored feet at @s run data merge entity @e[limit=1,sort=nearest,distance=0.1..2.5] {Motion:[0d,2.5d,0d]}
execute as @e[name=typhoon_atk,type=armor_stand] anchored feet at @s unless entity @a[distance=..50,tag=rpg.h.typhoon_tag1] run kill 

##悟空
execute as @e at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run effect give @e[limit=1,sort=nearest] wither 5 10 true
execute as @e at @s on attacker if entity @s[scores={wukong=0..,random=1},tag=rpg.h.wukong_tag1] run summon minecraft:creeper ~ ~ ~ {"ExplosionRadius":5,"Fuse":0}
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

##朗基努斯
effect clear @a[tag=rpg.h.power_tag1] wither 
effect clear @a[tag=rpg.h.power_tag1] darkness
effect clear @a[tag=rpg.h.power_tag1] blindness
execute as @e at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] as @e[distance=0.1..2] at @s run damage @s 2 minecraft:player_attack 
execute as @e at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run effect give @e[distance=0..2] glowing 5 3 true
execute as @e at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run particle dust_color_transition{from_color:[1.0,0.2,0.0],to_color:[1.0,1.0,1.0],scale:3} ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 0.1 20
execute as @e at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run particle dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:2} ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20
execute as @e at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run particle enchant ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20

execute as @a[scores={power_step=20..},tag=rpg.h.power_tag1] at @s run particle dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:1} ~0.25 ~1 ~0.25 -0.5 -0.75 -0.5 0.1 5
execute as @a[scores={power_step=20..},tag=rpg.h.power_tag1] at @s run effect give @s speed 1 2 true
execute as @a[scores={power_step=20},tag=rpg.h.power_tag1] at @s run playsound minecraft:block.trial_spawner.ominous_activate
execute as @e at @s on attacker if entity @s[scores={power=0..,power_step=20..},tag=rpg.h.power_tag1] at @s run summon armor_stand ^ ^0.3 ^2 {Invisible:1b,CustomName:[{"text":"power_atk"}],Invulnerable:1b}
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s run tp @s ~ ~ ~ facing entity @p[scores={power_step=20..}]
execute as @e at @s on attacker if entity @s[scores={power=0..,power_step=20..},tag=rpg.h.power_tag1] run scoreboard players reset @s power_step



scoreboard players reset * power

execute as @e[name=power_atk,type=armor_stand] anchored eyes at @s run particle sweep_attack ~0.5 ~1.2 ~0.5 -1 -1 -1 1 10 force
execute as @e[name=power_atk,type=armor_stand] anchored eyes at @s run particle dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:2} ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 10 force
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^-0.8  
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s run data merge entity @e[limit=1,sort=nearest,distance=0.1..2.5] {Motion:[0d,1d,0d]}
execute as @e at @s on attacker if entity @s[tag=rpg.h.power_tag1] if entity @e[name=power_atk,type=armor_stand,distance=..2] run tp @e[limit=1,sort=nearest] @e[name=power_atk,type=armor_stand,distance=..2,limit=1]
execute as @e at @s on attacker if entity @s[tag=rpg.h.power_tag1] if entity @e[name=power_atk,type=armor_stand,distance=..2] run damage @e[limit=1,sort=nearest] 3 minecraft:player_attack by @s

execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless entity @a[distance=..50,tag=rpg.h.power_tag1] run kill 
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-2 air run kill
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run summon lightning_bolt
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s unless block ^ ^ ^-1 air run kill


##史诗武器
execute as @e at @s on attacker if entity @s[scores={sun=0..},tag=rpg.h.sun_tag1] run effect give @s minecraft:fire_resistance 2 3
execute as @e at @s on attacker if entity @s[scores={sun=0..},tag=rpg.h.sun_tag1] run particle dust_color_transition{from_color:[1.0,0.84,0.0],to_color:[1.0,0.64,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
scoreboard players reset * sun

execute as @e at @s on attacker if entity @s[scores={ice=0..},tag=rpg.h.ice_tag1] run effect give @e[distance=..1,limit=1] minecraft:slowness 2 255 true
execute as @e at @s on attacker if entity @s[tag=rpg.h.ice_tag1] run damage @e[distance=..1,limit=1] 1 freeze
execute as @e at @s on attacker if entity @s[scores={ice=0..},tag=rpg.h.ice_tag1] run particle dust_color_transition{from_color:[0.58,0.92,1.0],to_color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
scoreboard players reset * ice

execute as @e at @s on attacker if entity @s[scores={steel=0..},tag=rpg.h.steel_tag1] run effect give @s minecraft:resistance 2 0
execute as @e at @s on attacker if entity @s[scores={steel=0..},tag=rpg.h.steel_tag1] run particle dust_pillar{block_state:{Name:iron_block}} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
scoreboard players reset * steel

execute as @e at @s on attacker if entity @s[scores={sea=0..},tag=rpg.h.sea_tag1] run effect give @e[distance=..1,limit=1] minecraft:wither 2 3 true
execute as @e at @s on attacker if entity @s[scores={sea=0..},tag=rpg.h.sea_tag1] run effect give @e[distance=..1,limit=1] minecraft:glowing 2 3 true
execute as @e at @s on attacker if entity @s[scores={sea=0..},tag=rpg.h.sea_tag1] run particle dust_color_transition{from_color:[1.0,0.38,0.92],to_color:[1.0,0.78,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute as @e at @s on attacker if entity @s[tag=rpg.h.sea_tag1] run particle raid_omen ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 3
scoreboard players reset * sea


execute as @a[scores={ice_step=45..}] anchored eyes at @s run playsound minecraft:entity.player.hurt_freeze player @s
execute as @a[scores={ice_step=45..}] anchored eyes at @s run data merge entity @e[distance=0.1..5,limit=1,sort=arbitrary,type=!item] {Motion:[0d,2.5d,0d]}
execute as @a[scores={ice_step=45..}] anchored eyes at @s at @e[distance=0.1..5] run particle dust_pillar{block_state:{Name:blue_ice}} ~0.5 ~1 ~0.5 -1 -1 -1 1 10
execute as @a[scores={ice_step=50..}] anchored eyes at @s run scoreboard players set @s ice_step 0


execute as @a[scores={sea_step=10..}] anchored feet at @s run summon armor_stand ^ ^ ^2 {Invisible:1b,CustomName:[{"text":"sea_atk"}],Invulnerable:1b}
execute as @a[scores={sea_step=10..}] anchored eyes at @s run playsound minecraft:weather.rain player @s
execute as @e[name=sea_atk,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @p[scores={sea_step=10..}]
execute as @a[scores={sea_step=10..}] anchored eyes at @s run scoreboard players set @s sea_step 0
execute as @e[name=sea_atk,type=armor_stand] anchored eyes at @s run particle dust_color_transition{from_color:[1.0,0.38,0.92],to_color:[1.0,0.78,0.0],scale:3} ~0.125 ~0.5 ~0.125 -0.25 -0.25 -0.25 0.1 20
execute as @e[name=sea_atk,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^-1  
execute as @e[name=sea_atk,type=armor_stand] anchored feet at @s as @e[distance=0.1..1.5] run damage @s 5 minecraft:drown

##铁斧不同攻击效果

execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:diamond"}.material run particle trial_spawner_detection_ominous ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:diamond"}.material run effect give @e[distance=..1,limit=1] minecraft:slowness 2 2 true

execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:iron"}.material run particle dust_pillar{block_state:{Name:iron_block}} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:iron"}.material run effect give @s minecraft:resistance 2 0

execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:gold"}.material run particle dust_color_transition{from_color:[1.0,0.84,0.0],to_color:[1.0,0.64,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 10
execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:gold"}.material run damage @e[distance=..1,limit=1] 2 in_fire

execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:quartz"}.material run particle sweep_attack ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0.1 10
execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:quartz"}.material run effect give @e[distance=..1,limit=1] minecraft:wither 2 2 true

execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:netherite"}.material run particle squid_ink ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0.2 10
execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:netherite"}.material run effect give @e[distance=..1,limit=1] minecraft:darkness 5 5 true

execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:redstone"}.material run particle dust_pillar{block_state:{Name:redstone_block}} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:redstone"}.material run effect give @s instant_health 1 0 

execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:copper"}.material run particle dust_color_transition{from_color:[0.9,0.47,0.32],to_color:[0.31,0.72,0.59],scale:3} ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:copper"}.material run effect give @e[distance=..1,limit=1] minecraft:slowness 1 5 true

execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:emerald"}.material run particle dust_color_transition{from_color:[0.09,0.85,0.38],to_color:[0.0,0.48,0.09],scale:3} ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:emerald"}.material run effect give @e[distance=..1,limit=1] minecraft:speed 2 2 true

execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:lapis"}.material run particle ominous_spawning ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:lapis"}.material run particle enchant ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10

execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:amethyst"}.material run particle dust_color_transition{from_color:[0.55,0.41,0.79],to_color:[0.33,0.22,0.53],scale:3} ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute as @e at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:amethyst"}.material run data merge entity @e[distance=..1,limit=1,] {Motion:[0d,0.4d,0d]}


scoreboard players reset * axe

