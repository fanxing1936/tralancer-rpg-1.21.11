tag @s remove rpg.seal.aura_target
execute at @s if entity @e[type=#rpg:seal_hostile,type=!minecraft:player,distance=..8] run tag @s add rpg.seal.aura_target
execute at @s if entity @e[tag=rpg.demon,distance=..8] run tag @s add rpg.seal.aura_target
execute at @s if entity @e[tag=rpg.demon.minion,distance=..8] run tag @s add rpg.seal.aura_target
execute if entity @s[tag=rpg.seal.aura_target] run function rpg:inquest/seal/ability/abaddon
tag @s remove rpg.seal.aura_target
