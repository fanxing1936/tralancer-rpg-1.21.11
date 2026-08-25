execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:diamond"}] run particle trial_spawner_detection_ominous ~ ~1 ~ 0.4 0.4 0.4 0.05 12
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:diamond"}] run effect give @e[tag=rpg.legacy.advanced_target,limit=1] slowness 2 2 true
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:iron"}] run particle dust_pillar{block_state:{Name:iron_block}} ~ ~1 ~ 0.5 0.5 0.5 0.1 18
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:iron"}] run effect give @s resistance 2 0 true
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:gold"}] run particle dust_color_transition{from_color:[1.0,0.84,0.0],to_color:[1.0,0.64,0.0],scale:3} ~ ~1 ~ 0.5 0.5 0.5 0.1 14
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:gold"}] run damage @e[tag=rpg.legacy.advanced_target,limit=1] 3 minecraft:in_fire by @s
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:quartz"}] run particle sweep_attack ~ ~1 ~ 0.4 0.4 0.4 0.1 10
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:quartz"}] run effect give @e[tag=rpg.legacy.advanced_target,limit=1] wither 2 1 true
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:netherite"}] run particle squid_ink ~ ~1 ~ 0.4 0.4 0.4 0.15 12
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:netherite"}] run effect give @e[tag=rpg.legacy.advanced_target,limit=1] darkness 3 0 true
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:redstone"}] run particle dust_pillar{block_state:{Name:redstone_block}} ~ ~1 ~ 0.5 0.5 0.5 0.1 14
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:redstone"}] run effect give @s instant_health 1 0 true
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:copper"}] run particle dust_color_transition{from_color:[0.9,0.47,0.32],to_color:[0.31,0.72,0.59],scale:3} ~ ~1 ~ 0.4 0.4 0.4 0.05 12
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:copper"}] run effect give @e[tag=rpg.legacy.advanced_target,limit=1] weakness 2 2 true
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:emerald"}] run particle dust_color_transition{from_color:[0.09,0.85,0.38],to_color:[0.0,0.48,0.09],scale:3} ~ ~1 ~ 0.4 0.4 0.4 0.05 12
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:emerald"}] run effect give @s speed 2 1 true
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:lapis"}] run particle ominous_spawning ~ ~1 ~ 0.4 0.4 0.4 0.05 10
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:lapis"}] run effect give @e[tag=rpg.legacy.advanced_target,limit=1] glowing 3 0 true
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:amethyst"}] run particle dust_color_transition{from_color:[0.55,0.41,0.79],to_color:[0.33,0.22,0.53],scale:3} ~ ~1 ~ 0.4 0.4 0.4 0.05 12
execute if items entity @s weapon.mainhand *[minecraft:trim~{material:"minecraft:amethyst"}] run effect give @e[tag=rpg.legacy.advanced_target,limit=1] levitation 1 1 true
scoreboard players reset @s axe
