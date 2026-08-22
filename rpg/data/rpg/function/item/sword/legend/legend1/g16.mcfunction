# 20 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:diamond"}.material run particle trial_spawner_detection_ominous ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:diamond"}.material run effect give @e[distance=..1,limit=1] minecraft:slowness 2 2 true

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:iron"}.material run particle dust_pillar{block_state:{Name:iron_block}} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:iron"}.material run effect give @s minecraft:resistance 2 0

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:gold"}.material run particle dust_color_transition{from_color:[1.0,0.84,0.0],to_color:[1.0,0.64,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:gold"}.material run damage @e[distance=..1,limit=1] 2 in_fire

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:quartz"}.material run particle sweep_attack ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0.1 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:quartz"}.material run effect give @e[distance=..1,limit=1] minecraft:wither 2 2 true

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:netherite"}.material run particle squid_ink ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0.2 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:netherite"}.material run effect give @e[distance=..1,limit=1] minecraft:darkness 5 5 true

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:redstone"}.material run particle dust_pillar{block_state:{Name:redstone_block}} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:redstone"}.material run effect give @s instant_health 1 0

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:copper"}.material run particle dust_color_transition{from_color:[0.9,0.47,0.32],to_color:[0.31,0.72,0.59],scale:3} ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:copper"}.material run effect give @e[distance=..1,limit=1] minecraft:slowness 1 5 true

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:emerald"}.material run particle dust_color_transition{from_color:[0.09,0.85,0.38],to_color:[0.0,0.48,0.09],scale:3} ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:emerald"}.material run effect give @e[distance=..1,limit=1] minecraft:speed 2 2 true

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:lapis"}.material run particle ominous_spawning ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:lapis"}.material run particle enchant ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10

execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:amethyst"}.material run particle dust_color_transition{from_color:[0.55,0.41,0.79],to_color:[0.33,0.22,0.53],scale:3} ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] if data entity @s SelectedItem.components.minecraft:trim{"material":"minecraft:amethyst"}.material run data merge entity @e[distance=..1,limit=1,] {Motion:[0d,0.4d,0d]}
