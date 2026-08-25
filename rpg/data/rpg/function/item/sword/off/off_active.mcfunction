execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={deep=0..},tag=rpg.h.deep_tag1] store result score @s random run random value 1..5
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={deep=0..,random=1},tag=rpg.h.deep_tag1] run particle sculk_soul ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 50
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={deep=0..,random=1},tag=rpg.h.deep_tag1] run effect give @e[limit=1,sort=nearest] minecraft:darkness 3 1 true
scoreboard players reset * random
scoreboard players reset * deep

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ink=0..},tag=rpg.h.ink_tag1] store result score @s random run random value 1..5
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ink=0..,random=1},tag=rpg.h.ink_tag1] run particle glow_squid_ink ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={ink=0..,random=1},tag=rpg.h.ink_tag1] run particle glow ~0.5 ~1.5 ~0.5 -1 -1 -1 1 50
scoreboard players reset * ink

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={damage=0..},tag=rpg.h.damage_tag1] store result score @s random run random value 1..5
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={damage=0..,random=1},tag=rpg.h.damage_tag1] run particle dust_pillar{block_state:{Name:redstone_block}} ~0.5 ~1.5 ~0.5 -1 -1 -1 1 100
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={damage=0..,random=1},tag=rpg.h.damage_tag1] run effect give @s minecraft:instant_health 1 0 true
scoreboard players reset * random
scoreboard players reset * damage


execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={blow=0..},tag=rpg.h.blow_tag1] store result score @s random run random value 1..3
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={blow=0..,random=1},tag=rpg.h.blow_tag1] run effect give @e[limit=1,sort=nearest] wither 5 10 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={blow=0..,random=1},tag=rpg.h.blow_tag1] run particle end_rod ~0.5 ~1.5 ~0.5 -1 -1 -1 0.2 100
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={blow=0..,random=1},tag=rpg.h.blow_tag1] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 1 100
scoreboard players reset * random
scoreboard players reset * blow
