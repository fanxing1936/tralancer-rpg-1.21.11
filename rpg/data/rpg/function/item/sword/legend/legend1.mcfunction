


##恶魔词缀
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g0


scoreboard players reset * devil_weapon

##天使词缀
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g1


scoreboard players reset * holy


##别西卜

execute as @a[scores={ashes=0..},tag=rpg.h.ashes_tag1] at @s run scoreboard players add @s ashes_level 1
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g2
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
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g3
scoreboard players reset * blil

##链锯
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g4
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
execute as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run summon minecraft:creeper ~ ~ ~ {Silent:1b,"ExplosionRadius":1,ignited:1b}
execute as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run kill @e[type=#minecraft:arrows,distance=..3]
execute as @s[scores={level=1..,night=20..}] at @s run playsound minecraft:entity.ender_dragon.shoot player @s
execute as @s[scores={level=1..,night=20..}] at @s anchored eyes run xp add @s -3 points
execute as @s[scores={night=20..}] at @s run scoreboard players set @s night 0

##高山
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g5
scoreboard players reset * random
scoreboard players reset * montain

execute as @a[tag=rpg.h.montain_tag1] at @s run particle dust_color_transition{from_color:[0.15,0.91,0.76],to_color:[0.9,0.63,0.0],scale:2} ~0.1 ~0.3 ~0.1 -0.2 -0.2 -0.2 0.1 2

##风骨
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={pen=0..},tag=rpg.h.pen_tag1] store result score @s random run random value 1..5
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={pen=0..},tag=rpg.h.pen_tag1] run particle squid_ink ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.2 20
execute as @a[scores={pen_=0..},tag=rpg.h.pen_tag1] at @s on attacker at @s run particle cloud ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 20
execute as @a[scores={pen_=0..},tag=rpg.h.pen_tag1] at @s on attacker at @s run damage @s 3 minecraft:out_of_world
execute as @a[scores={pen_=0..},tag=rpg.h.pen_tag1] at @s run effect give @s instant_health 1 0 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.pen_tag1] run particle enchant ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 1 3
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.pen_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
scoreboard players reset * random
scoreboard players reset * pen
scoreboard players reset * pen_

##剧毒之牙
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g6
scoreboard players reset * random
scoreboard players reset * potion

##无垠星空
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g7

scoreboard players reset * random
scoreboard players reset * saber

##樱怒之日
execute as @a[scores={sakura=0..},tag=rpg.h.sakura_tag1] at @s run scoreboard players add @s sakura_step 1
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g8

scoreboard players reset * random
scoreboard players reset * sakura



execute if entity @e[type=minecraft:spectral_arrow,tag=sakura_tag] run function rpg:item/sword/legend/legend1/g9

##亚巴顿
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g10
execute as @e[scores={random=1}] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0.8d,0.8d,0.8d]}
execute as @e[scores={random=2}] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[-0.8d,0.8d,0.8d]}
execute as @e[scores={random=3}] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0.8d,0.8d,-0.8d]}
execute as @e[scores={random=4}] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[-0.8d,0.8d,-0.8d]}
execute as @e[scores={random=5}] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0d,0.8d,0d]}
scoreboard players reset * soul


##风
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g11
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
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g12

scoreboard players reset * random
scoreboard players reset * wukong

##朗基努斯
effect clear @a[tag=rpg.h.power_tag1] wither 
effect clear @a[tag=rpg.h.power_tag1] darkness
effect clear @a[tag=rpg.h.power_tag1] blindness
execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g13

execute as @a[scores={power_step=20..},tag=rpg.h.power_tag1] at @s run particle dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:1} ~0.25 ~1 ~0.25 -0.5 -0.75 -0.5 0.1 5
execute as @a[scores={power_step=20..},tag=rpg.h.power_tag1] at @s run effect give @s speed 1 2 true
execute as @a[scores={power_step=20},tag=rpg.h.power_tag1] at @s run playsound minecraft:block.trial_spawner.ominous_activate
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={power=0..,power_step=20..},tag=rpg.h.power_tag1] at @s run summon armor_stand ^ ^0.3 ^2 {Invisible:1b,CustomName:[{"text":"power_atk"}],Invulnerable:1b}
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s run tp @s ~ ~ ~ facing entity @p[scores={power_step=20..}]
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={power=0..,power_step=20..},tag=rpg.h.power_tag1] run scoreboard players reset @s power_step



scoreboard players reset * power

execute as @e[name=power_atk,type=armor_stand] anchored eyes at @s run particle sweep_attack ~0.5 ~1.2 ~0.5 -1 -1 -1 1 10 force
execute as @e[name=power_atk,type=armor_stand] anchored eyes at @s run particle dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:2} ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 10 force
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^-0.8  
execute as @e[name=power_atk,type=armor_stand] anchored feet at @s run data merge entity @e[limit=1,sort=nearest,distance=0.1..2.5] {Motion:[0d,1d,0d]}
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.power_tag1] if entity @e[name=power_atk,type=armor_stand,distance=..2] run tp @e[limit=1,sort=nearest] @e[name=power_atk,type=armor_stand,distance=..2,limit=1]
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.power_tag1] if entity @e[name=power_atk,type=armor_stand,distance=..2] run damage @e[limit=1,sort=nearest] 3 minecraft:player_attack by @s

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
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sun=0..},tag=rpg.h.sun_tag1] run effect give @s minecraft:fire_resistance 2 3
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={sun=0..},tag=rpg.h.sun_tag1] run particle dust_color_transition{from_color:[1.0,0.84,0.0],to_color:[1.0,0.64,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
scoreboard players reset * sun

execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g14
scoreboard players reset * ice

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={steel=0..},tag=rpg.h.steel_tag1] run effect give @s minecraft:resistance 2 0
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={steel=0..},tag=rpg.h.steel_tag1] run particle dust_pillar{block_state:{Name:iron_block}} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
scoreboard players reset * steel

execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g15
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

execute if entity @e[tag=rpg.hurt] run function rpg:item/sword/legend/legend1/g16


scoreboard players reset * axe

