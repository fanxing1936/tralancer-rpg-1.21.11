# 15 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..,ashes_level=5..},tag=rpg.h.ashes_tag1] run scoreboard players set @s ashes_level 1

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..},tag=rpg.h.ashes_tag1] run effect give @e[distance=0..1] minecraft:wither 2 3 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..},tag=rpg.h.ashes_tag1] run effect give @e[distance=0..1] minecraft:glowing 2 3 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..},tag=rpg.h.ashes_tag1] run particle large_smoke ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 15

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..,ashes_level=1},tag=rpg.h.ashes_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0d,0.5d,0d]}
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..,ashes_level=1},tag=rpg.h.ashes_tag1] run particle dust_pillar{block_state:{Name:deepslate_coal_ore}} ~0.5 ~1.2 ~0.5 -1 -1 -1 1 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..,ashes_level=1},tag=rpg.h.ashes_tag1] run playsound minecraft:item.mace.smash_air

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..,ashes_level=2},tag=rpg.h.ashes_tag1] run particle minecraft:sweep_attack ~1 ~2 ~1 -2 -2 -2 1 20
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..,ashes_level=2},tag=rpg.h.ashes_tag1] run playsound minecraft:item.mace.smash_ground

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..,ashes_level=3},tag=rpg.h.ashes_tag1] run particle squid_ink ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..,ashes_level=3},tag=rpg.h.ashes_tag1] run playsound minecraft:item.mace.smash_ground_heavy

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..,ashes_level=4},tag=rpg.h.ashes_tag1] run summon firework_rocket ~ ~1 ~ {Life:0,LifeTime:0,FireworksItem:{id:firework_rocket,components:{fireworks:{flight_duration:0,explosions:[{shape:burst,has_twinkle:1b,has_trail:1b,colors:[I;1908001,4673362,10329495,4673362,1908001]}]}}}}
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ashes=0..,ashes_level=4},tag=rpg.h.ashes_tag1] run effect give @s minecraft:wither 2 2 true


execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.ashes_tag1] run particle large_smoke ~0.1 ~1.5 ~0.1 -0.2 -1 -0.2 0.2 1
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[tag=rpg.h.ashes_tag1] run tag @e[distance=0..2] add ashes
